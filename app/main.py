from openai import OpenAI

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

import os
from pathlib import Path
import concurrent.futures
import time


from app import config, router, util, schema
from app.prompt import summary_prompt

client = OpenAI(
    api_key=config.OPENAI_API_KEY,
)


app = FastAPI()


@app.post("/upload-media")
async def upload_media(
    file: UploadFile = File(...),
    department: str = Form(...),
    category: str = Form(...),
):
    """
    Upload media file endpoint.
    """
    filename = file.filename
    content_type = file.content_type
    file_content = await file.read()

    timeA = time.time()
    os.makedirs("media", exist_ok=True)
    with open(f"media/{filename}", "wb") as f:
        f.write(file_content)
    timeB = time.time()
    util.split_mp3(f"media/{filename}")
    timeC = time.time()
    file_name = Path(filename).stem
    transcriptions = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_file_path = {
            executor.submit(
                util.transcribe_audio,
                f"media/{file_name}/{file_path}",
                department,
                category,
            ): file_path
            for file_path in os.listdir(f"media/{file_name}")
            if file_path.endswith(".mp3")
        }

        for future in concurrent.futures.as_completed(future_to_file_path):
            try:
                file_path = future_to_file_path[future]
                transcription = future.result()
                transcriptions.append(
                    (file_path, transcription)
                )  # Store file path with transcript
            except Exception as e:
                print(f"Error transcribing file: {file_path} - {e}")

    # Sort transcriptions based on file paths for order preservation
    transcriptions.sort(key=lambda x: x[0])  # Sort by the first element (file path)

    # Extract sorted transcripts (remove file paths if not needed)
    sorted_transcripts = [t for t in transcriptions]  # Extract only transcripts

    timeD = time.time()
    print(f"Time to save file: {timeB - timeA}")
    print(f"Time to split file: {timeC - timeB}")
    print(f"Time to transcribe file: {timeD - timeC}")

    return sorted_transcripts


@app.post("/summary")
def create_summary(
    summaryInput: schema.SummaryInput,
):
    contents = util.split_text(summaryInput.content)

    for content in contents:
        print(len(content))

    summaries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_content = {
            executor.submit(
                util.summarize_text,
                content,
                summaryInput.department,
                summaryInput.category,
            ): content
            for content in contents
        }

        for future in concurrent.futures.as_completed(future_to_content):
            try:
                content = future_to_content[future]
                summary = future.result()
                summaries.append(summary)
            except Exception as e:
                print(f"Error summarizing content: {content} - {e}")

    summaries.sort(key=lambda x: x[0])

    return {"summaries": summaries}


origins = [
    "http://localhost:4123",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookie  (JWT)
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.course)
