# filename: backend/routers/autocurriculum_rl.py

from fastapi import APIRouter
from models import CurriculumRequest, CurriculumResponse
from core.rl_engine import suggest_next_topic
from db import log_event, save_student_state, get_student_state

router = APIRouter()

@router.post("/next", response_model=CurriculumResponse)
def get_next_curriculum(req: CurriculumRequest):
    prev_state = get_student_state(req.student_id)

    result = suggest_next_topic(
        history=req.history or prev_state.get("history", {}),
        recent_performance=[
            p.dict() for p in (req.recent_performance or [])
        ],
    )

    new_state = {
        "history": {
            "last_topic": result["next_topic"],
            "last_difficulty": result["difficulty"],
        }
    }
    save_student_state(req.student_id, new_state)

    payload = {
        "student_id": req.student_id,
        "request_history": req.history,
        "result": result,
    }
    log_event("autocurriculum_next", payload)

    return CurriculumResponse(
        student_id=req.student_id,
        next_topic=result["next_topic"],
        difficulty=result["difficulty"],
        recommended_exercises=result["recommended_exercises"],
        rationale=result["rationale"],
    )
