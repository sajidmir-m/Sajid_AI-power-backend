from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import QuizQuestion, StudentAnswer
from ..schemas import Difficulty
from .adaptive_engine import recommend_difficulty


def parse_question_id(question_id: str) -> int:
    """
    Accepts "Q12" or "12".
    """
    qid = question_id.strip()
    if qid.lower().startswith("q"):
        qid = qid[1:]
    if not qid.isdigit():
        raise ValueError('question_id must be like "Q12" or "12"')
    return int(qid)


def submit_answer(
    db: Session,
    *,
    student_id: str,
    question_id_raw: str,
    selected_answer: str,
    current_difficulty: Difficulty,
) -> tuple[StudentAnswer, QuizQuestion, Difficulty]:
    qid = parse_question_id(question_id_raw)
    question = db.query(QuizQuestion).filter(QuizQuestion.id == qid).first()
    if not question:
        raise LookupError(f"Question not found: {question_id_raw}")

    is_correct = selected_answer.strip() == (question.answer or "").strip()
    rec = recommend_difficulty(is_correct=is_correct, current_difficulty=current_difficulty)

    row = StudentAnswer(
        student_id=student_id,
        question_id=question.id,
        selected_answer=selected_answer,
        is_correct=is_correct,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return row, question, rec

