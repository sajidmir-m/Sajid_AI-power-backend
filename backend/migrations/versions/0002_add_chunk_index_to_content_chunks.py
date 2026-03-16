"""Add chunk_index to content_chunks.

Revision ID: 0002_add_chunk_index
Revises: 0001_initial
Create Date: 2026-03-16
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002_add_chunk_index"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("content_chunks", sa.Column("chunk_index", sa.Integer(), nullable=True))
    op.execute("UPDATE content_chunks SET chunk_index = 0 WHERE chunk_index IS NULL")
    op.alter_column("content_chunks", "chunk_index", existing_type=sa.Integer(), nullable=False)
    op.create_index("ix_content_chunks_chunk_index", "content_chunks", ["chunk_index"])


def downgrade() -> None:
    op.drop_index("ix_content_chunks_chunk_index", table_name="content_chunks")
    op.drop_column("content_chunks", "chunk_index")

