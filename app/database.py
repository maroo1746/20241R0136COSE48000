from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import chromadb
from langchain_community.vectorstores import Chroma
from app import config
from langchain_openai import OpenAIEmbeddings

engine = create_engine(
    config.DB_URL,
    pool_size=config.DB_POOL_SIZE,
    max_overflow=config.DB_MAX_OVERFLOW,
    connect_args={"options": "-c timezone=Asia/Seoul"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

embedding = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY, chunk_size=1)

client = chromadb.HttpClient(host="chroma", port=8000)
vectorstore_config = {"embedding_function": embedding, "client": client}


def get_vectorstore():
    return Chroma(**vectorstore_config)
