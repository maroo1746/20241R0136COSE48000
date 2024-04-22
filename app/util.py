from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app import schema
from app.database import get_vectorstore

CHUNK_SIZE = 20

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""],
    add_start_index=True,
)


def make_base_doc(course: schema.Course, user_id: int):
    print(course)

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


def create_embeddings(course: schema.Course, user_id: int):
    doc = make_base_doc(course, user_id)
    splits = make_splits(doc)

    for i in range(0, len(splits), CHUNK_SIZE):
        vdb = get_vectorstore()
        print(splits[i : i + CHUNK_SIZE])
        vdb.add_documents(splits[i : i + CHUNK_SIZE])


def transcribe_audio(file_path):
    clients = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )
    with open(file_path, "rb") as audio_file:
        transcription = clients.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="text"
        )
    return transcription


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
