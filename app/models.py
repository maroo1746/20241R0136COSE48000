from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    course_name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    summary = Column(String, nullable=False, default="")

    department = Column(String, nullable=False)
    category = Column(String, nullable=False)

    modified = Column(Boolean, default=True)
    pdf = Column(JSONB, nullable=False, default=[])


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    advice = Column(String, nullable=False)
    embedding_id = Column(String, nullable=False)
