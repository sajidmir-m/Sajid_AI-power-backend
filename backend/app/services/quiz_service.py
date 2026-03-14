from __future__ import annotations

import json
from typing import Iterable

from sqlalchemy.orm import Session

from ..models import ContentChunk, QuizQuestion
from ..schemas import Difficulty, QuizQuestionOut
from .chunk_selector import select_best_chunk
from .llm_fallback import build_fallback_quiz
from .llm_service import get_llm_provider


def _to_public_id(db_id: int) -> str:
    return f"Q{db_id}"


def ensure_public_id(db: Session, question: QuizQuestion) -> None:
    """
    Ensures a stable public_id for clients.
    """
    if not question.public_id:
        question.public_id = _to_public_id(question.id)


def generate_questions_for_chunks(
    db: Session,
    *,
    chunks: Iterable[ContentChunk],
    default_difficulty: Difficulty = "easy",
) -> int:
    """
    Generate questions via LLM (or fallback) from the best content chunk and persist them.

    Returns count of questions stored.
    """
    provider = get_llm_provider()
    created = 0

    best_chunk = select_best_chunk(chunks)
    if best_chunk is None:
        return 0

    try:
        llm_resp = provider.generate_quiz_questions(
            chunk_text=best_chunk.text,
            source_chunk_id=best_chunk.chunk_id,
        )
    except Exception:
        # Any LLM failure (quota, API error, invalid JSON) falls back to a simple quiz.
        llm_resp = build_fallback_quiz(
            chunk_text=best_chunk.text,
            source_chunk_id=best_chunk.chunk_id,
            default_difficulty=default_difficulty,
        )

    for q in llm_resp.questions:
        difficulty: Difficulty = q.difficulty if q.difficulty in ("easy", "medium", "hard") else default_difficulty
        options_json = json.dumps(q.options) if q.options is not None else None

        db_q = QuizQuestion(
            public_id="TEMP",  # set after flush when id is known
            question=q.question,
            type=q.type,
            options=options_json,
            answer=q.answer,
            difficulty=difficulty,
            source_chunk_id=q.source_chunk_id,
        )
        db.add(db_q)
        db.flush()
        db_q.public_id = _to_public_id(db_q.id)
        created += 1

    db.commit()
    return created


def fetch_quiz(
    db: Session,
    *,
    topic: str,
    difficulty: Difficulty,
    limit: int = 5,
) -> list[QuizQuestionOut]:
    """
    Fetch questions filtered by topic (via chunks) and difficulty.
    """
    q = (
        db.query(QuizQuestion)
        .join(ContentChunk, ContentChunk.chunk_id == QuizQuestion.source_chunk_id)
        .filter(ContentChunk.topic.ilike(topic))
        .filter(QuizQuestion.difficulty == difficulty)
        .order_by(QuizQuestion.id.desc())
        .limit(limit)
    )
    rows: list[QuizQuestion] = q.all()

    out: list[QuizQuestionOut] = []
    for r in rows:
        options = json.loads(r.options) if r.options else None
        out.append(
            QuizQuestionOut(
                id=r.id,
                question_id=r.public_id,
                question=r.question,
                type=r.type,  # type: ignore[arg-type]
                options=options,
                difficulty=r.difficulty,  # type: ignore[arg-type]
                source_chunk_id=r.source_chunk_id,
            )
        )
    return out

