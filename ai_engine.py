from google import genai

from config import (
    GEMINI_API_KEY,
    AI_MODEL
)


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# AI ANSWER
# =========================================================

def ask_ai(question):

    response = client.models.generate_content(
        model=AI_MODEL,
        contents=question
    )

    return response.text