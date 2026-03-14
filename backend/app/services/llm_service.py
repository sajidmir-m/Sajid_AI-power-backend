from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Protocol

from google import genai
from pydantic import ValidationError

from ..config import settings
from ..schemas import LLMQuizResponse


class LLMProvider(Protocol):
    def generate_quiz_questions(self, *, chunk_text: str, source_chunk_id: str) -> LLMQuizResponse:
        raise NotImplementedError


_json_fence_re = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)


def _extract_json(text: str) -> str:
    """
    Accept plain JSON or JSON wrapped in ```json fences.
    """
    m = _json_fence_re.search(text)
    if m:
        return m.group(1).strip()
    return text.strip()


@dataclass
class GeminiQuizProvider:
    model: str = settings.gemini_model

    def __post_init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to backend/.env.")
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def generate_quiz_questions(self, *, chunk_text: str, source_chunk_id: str) -> LLMQuizResponse:
        prompt = f"""
You are an educational quiz generator.

Rules:
- Use ONLY the provided text. Do not add outside facts.
- Create a mix of question types: MCQ, TF, FIB.
- Output MUST be valid JSON with this schema:
  {{
    "questions": [
      {{
        "question": "...",
        "type": "MCQ" | "TF" | "FIB",
        "options": ["..."] | null,
        "answer": "...",
        "difficulty": "easy" | "medium" | "hard",
        "source_chunk_id": "{source_chunk_id}"
      }}
    ]
  }}
- Ensure traceability: every question must include source_chunk_id exactly as given.
- Avoid hallucinations: every question must be answerable from the text.

Provided text:
\"\"\"{chunk_text}\"\"\"
""".strip()

        # Ask Gemini for JSON and validate with Pydantic.
        resp = self._client.models.generate_content(
            model=self.model,
            contents=[
                "You output only valid JSON. No extra text.",
                prompt,
            ],
            config={"temperature": 0.2},
        )

        content = resp.text or ""
        json_str = _extract_json(content)
        try:
            payload = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"LLM returned invalid JSON: {e}") from e

        try:
            parsed = LLMQuizResponse.model_validate(payload)
        except ValidationError as e:
            raise RuntimeError(f"LLM JSON did not match schema: {e}") from e

        # Hard-enforce traceability.
        for q in parsed.questions:
            q.source_chunk_id = source_chunk_id
        return parsed


def get_llm_provider() -> LLMProvider:
    # Swap provider here later (Anthropic, OpenAI, Azure, local models, etc.)
    return GeminiQuizProvider()

