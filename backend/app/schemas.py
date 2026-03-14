from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


Difficulty = Literal["easy", "medium", "hard"]
QuestionType = Literal["MCQ", "TF", "FIB"]


class SourceCreate(BaseModel):
    grade: int = Field(ge=1, le=12)
    subject: str = Field(min_length=1, max_length=100)
    topic: str = Field(min_length=1, max_length=200)


class SourceOut(BaseModel):
    id: int
    filename: str
    grade: int
    subject: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChunkOut(BaseModel):
    source_id: str
    chunk_id: str
    grade: int
    subject: str
    topic: str
    text: str


class IngestResponse(BaseModel):
    source_document: SourceOut
    source_id: str
    chunks_stored: int


class LLMQuestion(BaseModel):
    question: str
    type: QuestionType
    options: list[str] | None = None
    answer: str
    difficulty: Difficulty
    source_chunk_id: str


class LLMQuizResponse(BaseModel):
    questions: list[LLMQuestion]


class QuizQuestionOut(BaseModel):
    id: int
    question_id: str
    question: str
    type: QuestionType
    options: list[str] | None
    difficulty: Difficulty
    source_chunk_id: str


class QuizResponse(BaseModel):
    topic: str
    difficulty: Difficulty
    questions: list[QuizQuestionOut]


class SubmitAnswerIn(BaseModel):
    student_id: str = Field(min_length=1, max_length=64)
    question_id: str = Field(min_length=1, max_length=32, description='Accepts "Q12" or "12".')
    selected_answer: str
    current_difficulty: Difficulty = "easy"


class SubmitAnswerOut(BaseModel):
    is_correct: bool
    correct_answer: str
    recommended_difficulty: Difficulty
    explanation: str | None = None
    stored_answer_id: int


class ErrorOut(BaseModel):
    detail: str
    meta: dict[str, Any] | None = None

