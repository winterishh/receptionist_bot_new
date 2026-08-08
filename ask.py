from fastapi import APIRouter
from pydantic import BaseModel

from database.database import search_database
from ai.ai_engine import ask_ai

from utils import shared_state


router = APIRouter()


# =========================================================
# REQUEST MODEL
# =========================================================

class Query(BaseModel):

    message: str


# =========================================================
# ASK ENDPOINT
# =========================================================

@router.post("/ask")
def ask_question(query: Query):

    question = query.message

    print("\n==========================")
    print("Question Received:")
    print(question)

    shared_state.latest_question = question

    # =====================================================
    # DATABASE
    # =====================================================

    answer = search_database(question)

    # =====================================================
    # GEMINI FALLBACK
    # =====================================================

    if answer:

        print("Answer source: DATABASE")

    else:

        print(
            "Database could not answer."
        )

        print(
            "Generating answer with Gemini..."
        )

        answer = ask_ai(question)

        print(
            "Answer source: GEMINI"
        )

    # =====================================================
    # UPDATE DISPLAY
    # =====================================================

    shared_state.latest_answer = answer

    print("\nAnswer:")
    print(answer)

    print("==========================\n")

    return {
        "question": shared_state.latest_question,
        "answer": shared_state.latest_answer
    }