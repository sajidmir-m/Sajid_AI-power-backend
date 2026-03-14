from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..quiz_generator import generate_for_topic
from ..schemas import Difficulty, QuizResponse
from ..services.quiz_service import fetch_quiz


router = APIRouter(tags=["quiz"])


@router.get("/quiz", response_model=QuizResponse)
def get_quiz(
    topic: str = Query(..., min_length=1),
    difficulty: Difficulty = Query("easy"),
    limit: int = Query(5, ge=1, le=20),
    auto_generate: bool = Query(True, description="If empty, generate questions via LLM."),
    db: Session = Depends(get_db),
):
    """
    Returns quiz questions filtered by topic and difficulty.
    If no questions exist yet (prototype), auto-generates from recent chunks.
    """
    questions = fetch_quiz(db, topic=topic, difficulty=difficulty, limit=limit)
    if not questions and auto_generate:
        try:
            created = generate_for_topic(db, topic=topic, difficulty=difficulty)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Quiz generation failed: {e}")
        if created:
            questions = fetch_quiz(db, topic=topic, difficulty=difficulty, limit=limit)

    return QuizResponse(topic=topic, difficulty=difficulty, questions=questions)

