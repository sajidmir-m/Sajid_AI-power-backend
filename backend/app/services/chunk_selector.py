from __future__ import annotations

import random
from typing import Iterable, Optional

from ..models import ContentChunk


PREFERRED_MIN_WORDS = 100
PREFERRED_MAX_WORDS = 350


def _word_count(text: str) -> int:
    return len(text.split())


def select_best_chunk(chunks: Iterable[ContentChunk]) -> Optional[ContentChunk]:
    """
    Select a "best" chunk for quiz generation.

    Preference:
    - First try to find chunks within [100, 350] words.
    - If none exist, fall back to a random chunk from the list.
    """
    material = list(chunks)
    if not material:
        return None

    in_range = [c for c in material if PREFERRED_MIN_WORDS <= _word_count(c.text) <= PREFERRED_MAX_WORDS]
    if in_range:
        # Deterministic choice for now: pick the first suitable chunk.
        return in_range[0]

    return random.choice(material)

