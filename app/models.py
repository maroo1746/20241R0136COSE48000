from sqlalchemy import Integer, String, DateTime, ForeignKey
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


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    question = Column(String, nullable=False)
    type = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    choices = Column(String, nullable=False)
    reason = Column(String, nullable=False)
