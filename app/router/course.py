from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from typing import Optional
from datetime import datetime, timedelta, timezone

from app import models, schema, util
from app.prompt import question_system_prompt, question_response_prompt
from app.dependencies import get_db

router = APIRouter(prefix="/course", tags=["course"])


@router.get("/")
def read_course(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@router.get("/{course_id}")
def read_course(course_id: str, db: Session = Depends(get_db)):
    course_id = int(course_id)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course is None:
        return {"error": "Course not found"}
    return course


@router.post("/")
def create_course(
    title: str, content: str, summary: str = None, db: Session = Depends(get_db)
):
    now = datetime.now(timezone(timedelta(hours=9)))
    if summary is None:
        summary = ""
    course = models.Course(
        course_name=title,
        content=content,
        summary=summary,
        timestamp=now,
    )
    db.add(course)
    db.flush()

    util.create_embeddings(course, user_id=1)
    return course


@router.patch("/{course_id}")
def update_course(
    course_id: str,
    course: schema.CourseInput,
    db: Session = Depends(get_db),
):
    print(course)
    course_id = int(course_id)
    found_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if found_course is None:
        return {"error": "Course not found"}
    if course.title is not None:
        found_course.course_name = course.title
    if course.content is not None:
        found_course.content = course.content
    if course.summary is not None:
        found_course.summary = course.summary

    db.query(models.Course).filter(models.Course.id == course_id).update(
        {
            models.Course.course_name: found_course.course_name,
            models.Course.content: found_course.content,
            models.Course.summary: found_course.summary,
        }
    )

    db.flush()

    util.create_embeddings(found_course, user_id=1)
    return found_course


@router.post("/{course_id}/question")
def create_question(course_id: int, count: Optional[int] = 5):
    contents = "This is a test."
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": question_system_prompt % count
                + contents
                + question_response_prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
