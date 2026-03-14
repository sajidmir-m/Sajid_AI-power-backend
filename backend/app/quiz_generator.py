from __future__ import annotations

from sqlalchemy.orm import Session

from .models import ContentChunk
from .schemas import Difficulty
from .services.quiz_service import generate_questions_for_chunks


def generate_for_topic(
    db: Session,
    *,
    topic: str,
    difficulty: Difficulty = "easy",
    max_chunks: int = 3,
) -> int:
    """
    Generate questions for the newest chunks matching the topic.
    """
    chunks = (
        db.query(ContentChunk)
        .filter(ContentChunk.topic.ilike(topic))
        .order_by(ContentChunk.id.desc())
        .limit(max_chunks)
        .all()
    )
    if not chunks:
        return 0
    return generate_questions_for_chunks(db, chunks=chunks, default_difficulty=difficulty)

