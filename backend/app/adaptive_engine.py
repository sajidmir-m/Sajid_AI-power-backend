from __future__ import annotations

from typing import Literal


Difficulty = Literal["easy", "medium", "hard"]


def recommend_next_difficulty(current: Difficulty, is_correct: bool) -> Difficulty:
    """
    Adaptive rule:
    - correct -> increase difficulty
    - incorrect -> decrease difficulty
    """
    order: list[Difficulty] = ["easy", "medium", "hard"]
    idx = order.index(current)
    if is_correct:
        idx = min(idx + 1, len(order) - 1)
    else:
        idx = max(idx - 1, 0)
    return order[idx]

