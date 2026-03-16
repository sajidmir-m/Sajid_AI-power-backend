from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..chunking import chunk_text
from ..database import get_db
from ..models import ContentChunk, SourceDocument
from ..pdf_ingest import clean_text, extract_text_from_pdf
from ..schemas import IngestResponse
from ..services.chunk_service import _save_chunks_to_db
from ..services.quiz_service import generate_questions_for_chunks


router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest_pdf(
    grade: int = Form(...),
    subject: str = Form(...),
    topic: str = Form(...),
    generate_quiz: bool = Form(True),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Accepts PDF upload, extracts + cleans text, chunks into 150–300 words, stores chunks.
    Optionally generates quiz questions immediately.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    try:
        raw = extract_text_from_pdf(pdf_bytes)
        cleaned = clean_text(raw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {e}")

    chunks = chunk_text(cleaned)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text could be extracted from PDF.")

    src = SourceDocument(filename=file.filename, grade=grade, subject=subject)
    db.add(src)
    db.flush()  # assigns src.id

    source_id = f"SRC_{src.id:03d}"
    inserted = _save_chunks_to_db(
        db,
        source_id=src.id,
        chunks=[
            {"topic": topic, "text": ch_text, "chunk_index": idx}
            for idx, ch_text in enumerate(chunks)
        ],
    )
    db.refresh(src)

    if generate_quiz:
        # Generate for all newly-created chunks for this source.
        new_chunks = (
            db.query(ContentChunk).filter(ContentChunk.source_id == src.id).order_by(ContentChunk.id.asc()).all()
        )
        try:
            generate_questions_for_chunks(db, chunks=new_chunks, default_difficulty="easy")
        except Exception:
            # Ingestion succeeded; quiz generation is best-effort. We swallow the error here
            # so the client still receives a successful ingest response.
            pass

    return IngestResponse(source_document=src, source_id=source_id, chunks_stored=inserted)

