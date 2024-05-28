from pydantic import BaseModel
from typing import Optional, List


class CourseInput(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    department: str
    category: str
    pdf: List[dict]


class Course(BaseModel):
    id: int
    course_name: str
    content: str
    summary: Optional[str] = None
    timestamp: str

    department: str
    category: str
    pdf: List[dict]


class SummaryInput(BaseModel):
    content: str
    department: str
    category: str


class QuestionInput(BaseModel):
    count: str


class AdviceInput(BaseModel):
    answer: str
