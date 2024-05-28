from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app import schema, config
from app.database import get_vectorstore
from app.prompt import correction_prompt, summary_prompt, summary_notice_prompt

from openai import OpenAI
import os
from pathlib import Path

CHUNK_SIZE = 20

splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )"],
    add_start_index=True,
)


def make_base_doc(course: schema.Course, user_id: int):
    return Document(
        page_content=course.content,
        metadata={
            "id": f"{course.id}:0",
            "course_id": course.id,
            "created_date": str(course.timestamp),
            "user_id": user_id,
        },
    )


def make_splits(doc: Document) -> list[Document]:
    splits = splitter.split_documents([doc])

    for split in splits:
        split.metadata["id"] = f'{split.metadata["id"]}:{split.metadata["start_index"]}'

    return splits


def update_embeddings(
    course: schema.Course,
    user_id: int,
):
    vdb = get_vectorstore()
    emb_ids = vdb.get(where={"course_id": course.id})["ids"]
    if emb_ids:
        vdb.delete(emb_ids)

    create_embeddings(course, user_id)


def create_embeddings(course: schema.Course, user_id: int):
    vdb = get_vectorstore()

    emb_ids = vdb.get(where={"course_id": course.id})["ids"]
    if emb_ids:
        vdb.delete(emb_ids)

    doc = make_base_doc(course, user_id)
    splits = make_splits(doc)

    for i in range(0, len(splits), CHUNK_SIZE):
        vdb.add_documents(splits[i : i + CHUNK_SIZE])


def get_embeddings(course_id: int):
    vdb = get_vectorstore()
    return vdb.get(where={"course_id": course_id})


def transcribe_audio(file_path, department, category):
    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
        transcription = (
            client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": correction_prompt.format(
                            department=department, category=category
                        ),
                    },
                    {
                        "role": "system",
                        "content": transcription,
                    },
                ],
            )
            .choices[0]
            .message.content
        )
        print(transcription)
    return transcription


def summarize_text(content, department, category):
    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )
    summary = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": summary_prompt.format(
                    department=department, category=category
                ),
            },
            {"role": "system", "content": content},
            {"role": "system", "content": summary_notice_prompt},
        ],
    )
    return summary.choices[0].message.content


def split_text(text):
    return RecursiveCharacterTextSplitter(
        chunk_size=6000,
        chunk_overlap=1000,
        separators=["\n\n", "\n", "(?<=\. )"],
        add_start_index=True,
    ).split_text(text)


def split_mp3(input_file_path, chunk_size_mb=2):
    # 파일 경로에서 파일명(확장자 제외) 추출
    file_name = Path(input_file_path).stem
    output_dir = "media/" + file_name

    # 출력 디렉터리 생성 (이미 존재하는 경우 무시)
    os.makedirs(output_dir, exist_ok=True)

    # 파일을 바이트로 계산된 크기로 분할
    chunk_size = chunk_size_mb * 1024 * 1024  # MB to bytes

    with open(input_file_path, "rb") as f:
        chunk = f.read(chunk_size)
        part_num = 1

        while chunk:
            output_file_path = os.path.join(
                output_dir, f"{file_name}_{part_num:03d}.mp3"
            )
            with open(output_file_path, "wb") as chunk_file:
                chunk_file.write(chunk)
            part_num += 1
            chunk = f.read(chunk_size)


def get_embedding_from_id(embedding_id):
    vdb = get_vectorstore()
    print(embedding_id)
    print(vdb.get(ids=embedding_id))
    return vdb.get(ids=embedding_id)["documents"][0]
