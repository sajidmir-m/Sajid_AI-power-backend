from __future__ import annotations

from dataclasses import dataclass

from .pdf_ingest import iter_words


@dataclass(frozen=True)
class ChunkSpec:
    min_words: int = 150
    max_words: int = 300


def chunk_text(text: str, spec: ChunkSpec = ChunkSpec()) -> list[str]:
    """
    Split text into chunks of 150–300 words.

    Implementation notes:
    - We greedily accumulate up to max_words.
    - If the final chunk is too small, we merge it into the previous chunk.
    """
    words = list(iter_words(text))
    if not words:
        return []

    chunks: list[list[str]] = []
    i = 0
    n = len(words)
    while i < n:
        end = min(i + spec.max_words, n)
        chunk = words[i:end]
        chunks.append(chunk)
        i = end

    if len(chunks) >= 2 and len(chunks[-1]) < spec.min_words:
        chunks[-2].extend(chunks[-1])
        chunks.pop()

    return [" ".join(c).strip() for c in chunks if c]

