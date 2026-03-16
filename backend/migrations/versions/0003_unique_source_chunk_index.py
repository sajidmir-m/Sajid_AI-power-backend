"""Unique (source_id, chunk_index) on content_chunks.

Revision ID: 0003_unique_source_chunk_index
Revises: 0002_add_chunk_index
Create Date: 2026-03-16
"""

from __future__ import annotations

from alembic import op


revision = "0003_unique_source_chunk_index"
down_revision = "0002_add_chunk_index"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_content_chunks_source_chunk_index",
        "content_chunks",
        ["source_id", "chunk_index"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_content_chunks_source_chunk_index",
        "content_chunks",
        type_="unique",
    )

