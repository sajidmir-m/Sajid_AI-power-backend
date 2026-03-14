from __future__ import annotations

from typing import Literal


Difficulty = Literal["easy", "medium", "hard"]


def recommend_difficulty(is_correct: bool, current_difficulty: Difficulty) -> Difficulty:
    """
    Adaptive rule:
    - correct -> increase difficulty (easy -> medium -> hard)
    - incorrect -> decrease difficulty (hard -> medium -> easy)
    - stay at the boundary when already at min/max
    """
    order: list[Difficulty] = ["easy", "medium", "hard"]
    try:
        idx = order.index(current_difficulty)
    except ValueError:
        idx = 0

    if is_correct and idx < len(order) - 1:
        idx += 1
    elif not is_correct and idx > 0:
        idx -= 1

    return order[idx]

