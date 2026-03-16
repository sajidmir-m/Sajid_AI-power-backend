from __future__ import annotations

from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import ContentChunk


def _save_chunks_to_db(db: Session, source_id: int, chunks: list[dict[str, Any]]) -> int:
    """
    Inserts chunk rows for a given source document.

    Returns number of chunks successfully inserted.
    """
    inserted = 0

    for ch in chunks:
        topic = ch.get("topic")
        text = ch.get("text")
        chunk_index = ch.get("chunk_index")

        if topic is None or text is None or chunk_index is None:
            continue

        try:
            idx_int = int(chunk_index)
        except (TypeError, ValueError):
            continue

        chunk_id = f"SRC_{source_id:03d}_CH_{idx_int + 1:02d}"

        try:
            # Use a SAVEPOINT so one bad row doesn't rollback all inserts.
            with db.begin_nested():
                db.add(
                    ContentChunk(
                        chunk_id=chunk_id,
                        source_id=source_id,
                        topic=str(topic),
                        text=str(text),
                        chunk_index=idx_int,
                    )
                )
                db.flush()
            inserted += 1
        except SQLAlchemyError:
            # begin_nested() rolls back to savepoint; keep going
            continue

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return 0

    return inserted


def save_chunks_to_db(source_id: int, chunks: list[dict[str, Any]]) -> int:
    """
    Public API requested: open a DB session and insert chunks.
    """
    db = SessionLocal()
    try:
        return _save_chunks_to_db(db, source_id=source_id, chunks=chunks)
    finally:
        db.close()

