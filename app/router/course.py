from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone

from openai import OpenAI

from app import models, schema, config
from app.prompt import (
    question_system_prompt,
    question_response_prompt,
    advice_prompt,
)
from app.dependencies import get_db
from app.util import llm

router = APIRouter(prefix="/course", tags=["course"])


client = OpenAI(
    api_key=config.OPENAI_API_KEY,
)


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
def create_course(course: schema.CourseInput, db: Session = Depends(get_db)):
    now = datetime.now(timezone(timedelta(hours=9)))
    if course.summary is None:
        course.summary = ""
    course = models.Course(
        course_name=course.title,
        content=course.content,
        summary=course.summary,
        timestamp=now,
        department=course.department,
        category=course.category,
        pdf=course.pdf,
    )
    db.add(course)
    db.flush()

    # util.create_embeddings(course, user_id=1)
    return course


@router.patch("/{course_id}")
def update_course(
    course_id: str,
    course: schema.CourseInput,
    db: Session = Depends(get_db),
):
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
    # jsonb
    found_course.pdf = course.pdf
    found_course.department = course.department
    found_course.category = course.category
    found_course.modified = True

    db.query(models.Course).filter(models.Course.id == course_id).update(
        {
            models.Course.course_name: found_course.course_name,
            models.Course.content: found_course.content,
            models.Course.summary: found_course.summary,
            models.Course.department: found_course.department,
            models.Course.category: found_course.category,
        }
    )

    db.flush()

    # util.update_embeddings(found_course, user_id=1)
    return found_course


@router.get("/{course_id}/questions")
def get_questions(course_id: str, db: Session = Depends(get_db)):
    course_id = int(course_id)
    questions = db.query(models.Quiz).filter(models.Quiz.course_id == course_id).all()
    return questions


@router.post("/{course_id}/question")
def create_question(
    course_id: int, input: schema.QuestionInput, db: Session = Depends(get_db)
):
    course_id = int(course_id)
    course = db.query(models.Course).filter(models.Course.id == course_id).first()

    if course.modified:
        llm.create_embeddings(course, user_id=1)
        course.modified = False
        db.query(models.Course).filter(models.Course.id == course_id).update(
            {models.Course.modified: course.modified}
        )
        db.flush()
    embeddings = llm.get_embeddings(course_id)

    result = []

    db.query(models.Quiz).filter(models.Quiz.course_id == course_id).delete()

    for index, embedding in enumerate(embeddings["documents"]):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": question_system_prompt.format(
                        count=input.count, content=embedding
                    ),
                },
                {"role": "system", "content": question_response_prompt},
            ],
            model="gpt-4o",
        )
        for message in chat_completion.choices[0].message.content.split("\n"):
            if message.strip() != "":
                quiz = models.Quiz(
                    course_id=course_id,
                    question=message.removeprefix("- "),
                    answer="",
                    advice="",
                    embedding_id=embeddings["ids"][index],
                )
                db.add(quiz)
                db.flush()
                result.append(
                    {
                        "id": quiz.id,
                        "question": message.removeprefix("- "),
                    }
                )

    return result


@router.post("/{course_id}/question/{question_id}/advice")
def create_advice(
    course_id: int,
    question_id: int,
    input: schema.AdviceInput,
    db: Session = Depends(get_db),
):
    course_id = int(course_id)
    question_id = int(question_id)
    question = db.query(models.Quiz).filter(models.Quiz.id == question_id).first()

    embedding = llm.search(question.question, course_id)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": advice_prompt.format(
                    question=question.question,
                    content=embedding,
                ),
            },
            {"role": "user", "content": input.answer},
        ],
        model="gpt-4",
    )

    advice = chat_completion.choices[0].message.content
    db.query(models.Quiz).filter(models.Quiz.id == question_id).update(
        {models.Quiz.advice: advice, models.Quiz.answer: input.answer}
    )
    db.flush()
    return {"advice": advice}
