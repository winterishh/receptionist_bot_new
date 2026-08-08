import os
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# Gemini
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================================================
# Database
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "college.db"
)

# =========================================================
# Server
# =========================================================

HOST = "0.0.0.0"
PORT = 8000

# =========================================================
# Gemini Models
# =========================================================

AI_MODEL = "gemini-flash-latest"

ANALYZER_MODEL = "gemini-2.5-flash"