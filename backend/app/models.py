from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    chunks: Mapped[list["ContentChunk"]] = relationship(
        back_populates="source_document",
        cascade="all, delete-orphan",
    )


class ContentChunk(Base):
    __tablename__ = "content_chunks"
    __table_args__ = (UniqueConstraint("chunk_id", name="uq_content_chunks_chunk_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chunk_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    source_document: Mapped[SourceDocument] = relationship(back_populates="chunks")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Convenient public-facing identifier like "Q12" for clients.
    public_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)

    question: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # MCQ | TF | FIB

    # Stored as JSON string for portability (SQLite) and simple querying.
    options: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(16), nullable=False, index=True)  # easy|medium|hard

    source_chunk_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("quiz_questions.id"), nullable=False, index=True)
    selected_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    question: Mapped[QuizQuestion] = relationship()

