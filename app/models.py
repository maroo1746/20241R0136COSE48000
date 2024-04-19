from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.schema import Column

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Chapter(Base):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False)
    updated_date = Column(DateTime(timezone=True), nullable=False)
    questions = Column(Integer, ForeignKey("question.id"))
    summary = Column(String, nullable=False, default="")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    question = Column(String, nullable=False)
    type = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    choices = Column(String, nullable=False)
    reason = Column(String, nullable=False)
