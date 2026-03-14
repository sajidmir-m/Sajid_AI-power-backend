"""Initial schema: source_documents, content_chunks, quiz_questions, student_answers."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("grade", sa.Integer(), nullable=False),
        sa.Column("subject", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "content_chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("chunk_id", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("source_documents.id"), nullable=False),
        sa.Column("topic", sa.String(length=200), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
    )
    op.create_index("ix_content_chunks_chunk_id", "content_chunks", ["chunk_id"])
    op.create_index("ix_content_chunks_source_id", "content_chunks", ["source_id"])
    op.create_index("ix_content_chunks_topic", "content_chunks", ["topic"])
    op.create_unique_constraint("uq_content_chunks_chunk_id", "content_chunks", ["chunk_id"])

    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("public_id", sa.String(length=32), nullable=False, unique=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("options", sa.Text(), nullable=True),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(length=16), nullable=False),
        sa.Column("source_chunk_id", sa.String(length=64), nullable=False),
    )
    op.create_index("ix_quiz_questions_id", "quiz_questions", ["id"])
    op.create_index("ix_quiz_questions_public_id", "quiz_questions", ["public_id"])
    op.create_index("ix_quiz_questions_difficulty", "quiz_questions", ["difficulty"])
    op.create_index("ix_quiz_questions_source_chunk_id", "quiz_questions", ["source_chunk_id"])

    op.create_table(
        "student_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.String(length=64), nullable=False),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("quiz_questions.id"), nullable=False),
        sa.Column("selected_answer", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_student_answers_id", "student_answers", ["id"])
    op.create_index("ix_student_answers_student_id", "student_answers", ["student_id"])
    op.create_index("ix_student_answers_question_id", "student_answers", ["question_id"])


def downgrade() -> None:
    op.drop_index("ix_student_answers_question_id", table_name="student_answers")
    op.drop_index("ix_student_answers_student_id", table_name="student_answers")
    op.drop_index("ix_student_answers_id", table_name="student_answers")
    op.drop_table("student_answers")

    op.drop_index("ix_quiz_questions_source_chunk_id", table_name="quiz_questions")
    op.drop_index("ix_quiz_questions_difficulty", table_name="quiz_questions")
    op.drop_index("ix_quiz_questions_public_id", table_name="quiz_questions")
    op.drop_index("ix_quiz_questions_id", table_name="quiz_questions")
    op.drop_table("quiz_questions")

    op.drop_index("ix_content_chunks_topic", table_name="content_chunks")
    op.drop_index("ix_content_chunks_source_id", table_name="content_chunks")
    op.drop_index("ix_content_chunks_chunk_id", table_name="content_chunks")
    op.drop_constraint("uq_content_chunks_chunk_id", "content_chunks", type_="unique")
    op.drop_table("content_chunks")

    op.drop_table("source_documents")

