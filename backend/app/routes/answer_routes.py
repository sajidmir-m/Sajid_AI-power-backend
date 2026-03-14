from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import SubmitAnswerIn, SubmitAnswerOut
from ..services.student_service import submit_answer


router = APIRouter(tags=["answers"])


@router.post("/submit-answer", response_model=SubmitAnswerOut)
def submit_answer_route(payload: SubmitAnswerIn, db: Session = Depends(get_db)):
    try:
        row, question, rec = submit_answer(
            db,
            student_id=payload.student_id,
            question_id_raw=payload.question_id,
            selected_answer=payload.selected_answer,
            current_difficulty=payload.current_difficulty,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {e}")

    return SubmitAnswerOut(
        is_correct=row.is_correct,
        correct_answer=question.answer,
        recommended_difficulty=rec,
        explanation=None,
        stored_answer_id=row.id,
    )

