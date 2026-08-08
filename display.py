from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from utils import shared_state

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================================================
# DISPLAY PAGE
# =========================================================

@router.get("/display")
def display(request: Request):

    context = {
        "request": request
    }

    return templates.TemplateResponse(
        request=request,
        name="display.html",
        context=context
    )


# =========================================================
# DISPLAY DATA API
# =========================================================

@router.get("/display_data")
def get_display_data():

    return {
        "question": shared_state.latest_question,
        "answer": shared_state.latest_answer
    }