from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_all_users, get_db, get_latest_plan, get_user, save_plan, save_user, update_plan
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(username=username, user_id=user_id, age=age, weight=weight, goal=goal, intensity=intensity)
        workout_plan = generate_workout_gemini(data)
        nutrition_tip = generate_nutrition_tip_with_flash(data)
        user = save_user(db, **data.model_dump())
        plan = save_plan(db, user, workout_plan, nutrition_tip)
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={"user": user, "plan": plan, "error": None},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=400,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        request_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, request_data.user_id)
        plan = get_latest_plan(db, request_data.user_id)
        if not user or not plan:
            raise ValueError("No saved plan was found for that User ID.")
        updated = update_workout_plan(plan.original_plan, request_data.feedback)
        update_plan(db, plan, updated, request_data.feedback)
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={"user": user, "plan": plan, "message": "Your plan was updated successfully.", "error": None},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={"user": None, "plan": None, "message": None, "error": str(exc)},
            status_code=400,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse(request=request, name="all_users.html", context={"users": users})


@router.get("/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}
