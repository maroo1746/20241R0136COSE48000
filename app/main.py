from openai import OpenAI
    
from fastapi import FastAPI, UploadFile, File
from typing import Optional
import os
from pathlib import Path

# from langchain.llms import OpenAI
# from langchain.agents import ConversationalAgent
# from langchain.chains import Chain


openai_api_key = "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"

client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)


# openai_agent = OpenAI(temperature=0.9, api_key=openai_api_key)

# # Create a conversational chatGPT agent
# chat_gpt_agent = ConversationalAgent(openai_agent)

# # Define a chain with the ChatGPT agent
# chat_gpt_chain = Chain(chat_gpt_agent)

app = FastAPI()


@app.get("/")
def read_root():
    test_prompt = "Tell me a story about a dragon and a wizard."
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": test_prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )
     # answer = chat_completion['choices'][0]['message']['content']
    # expected_response = "Once upon a time, in a world of magic and wonder, there lived a powerful dragon..."

    # Run the prompt through the ChatGPT agent and check the response
    # response = chat_gpt_chain.run(test_prompt)
    # print(response)  # Print the generated response

    # completion = chat_completion.parse()  # get the object that `chat.completions.create()` would have returned
    print(chat_completion)
    return {"Hello":chat_completion}



@app.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):
  """
  Upload media file endpoint.
  """
  filename = file.filename
  content_type = file.content_type
  file_content = await file.read()

  # Save the uploaded file (replace with your actual logic)
#   os.mkdir("media")
  with open(f"media/{filename}", "wb") as f:
      f.write(file_content)
  split_mp3(f"media/{filename}")

    

  print(os.listdir("media"))
  return {
      "message": f"File {filename} uploaded successfully!",
      "filename": filename,
      "content_type": content_type,
  }


def split_mp3(input_file_path, chunk_size_mb=24):
    # 파일 경로에서 파일명(확장자 제외) 추출
    file_name = Path(input_file_path).stem
    output_dir = "media/"+file_name

    # 출력 디렉터리 생성 (이미 존재하는 경우 무시)
    os.makedirs(output_dir, exist_ok=True)

    # 파일을 바이트로 계산된 크기로 분할
    chunk_size = chunk_size_mb * 1024 * 1024  # MB to bytes

    with open(input_file_path, 'rb') as f:
        chunk = f.read(chunk_size)
        part_num = 1

        while chunk:
            output_file_path = os.path.join(output_dir, f"{file_name}_{part_num}.mp3")
            with open(output_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            part_num += 1
            chunk = f.read(chunk_size)

@app.get("/home")
def read_home():
    return {"Hello": "Home"}