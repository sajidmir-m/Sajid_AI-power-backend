from __future__ import annotations

from typing import List

from ..schemas import Difficulty, LLMQuestion, LLMQuizResponse


def _build_phrase_question(chunk_text: str, source_chunk_id: str, difficulty: Difficulty) -> LLMQuestion:
  """
  Build a simple fill‑in‑the‑blank question that directly uses
  a short phrase from the PDF chunk text.
  """
  words = [w for w in chunk_text.split() if w.strip()]
  # If there isn't enough text, fall back to a generic learning prompt.
  if len(words) < 5:
      return LLMQuestion(
          question="This passage is mainly used for ________.",
          type="FIB",
          options=None,
          answer="learning",
          difficulty=difficulty,
          source_chunk_id=source_chunk_id,
      )

  # Take a short snippet from the start of the passage.
  snippet_len = min(10, len(words))
  snippet_words = words[:snippet_len]

  # Hide the last word in the snippet.
  answer = snippet_words[-1].strip(",.?!;:") or snippet_words[-1]
  visible = " ".join(snippet_words[:-1])

  question_text = f'Complete this phrase from the passage: "{visible} ______".'

  return LLMQuestion(
      question=question_text,
      type="FIB",
      options=None,
      answer=answer,
      difficulty=difficulty,
      source_chunk_id=source_chunk_id,
  )


def build_fallback_quiz(
    *,
    chunk_text: str,
    source_chunk_id: str,
    default_difficulty: Difficulty = "easy",
) -> LLMQuizResponse:
    """
    Deterministic fallback quiz when the LLM fails.

    The first question is built directly from the PDF text so that
    even without Gemini, the quiz still feels tied to the uploaded passage.
    """
    questions: List[LLMQuestion] = []

    # Q1: Fill‑in‑the‑blank using a real phrase from the passage.
    questions.append(_build_phrase_question(chunk_text, source_chunk_id, default_difficulty))

    # Q2: Simple comprehension True/False about reading the passage.
    questions.append(
        LLMQuestion(
            question="True or False: You should read the passage carefully to answer questions about it.",
            type="TF",
            options=["True", "False"],
            answer="True",
            difficulty=default_difficulty,
            source_chunk_id=source_chunk_id,
        )
    )

    # Q3: Generic purpose question kept as a backup.
    questions.append(
        LLMQuestion(
            question="The passage is mainly about ________.",
            type="FIB",
            options=None,
            answer="the topic described in the text",
            difficulty=default_difficulty,
            source_chunk_id=source_chunk_id,
        )
    )

    return LLMQuizResponse(questions=questions)

