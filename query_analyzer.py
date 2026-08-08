import json
import re
import sqlite3

from google import genai

from config import GEMINI_API_KEY, ANALYZER_MODEL, DATABASE_PATH


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):
    """
    Converts text into a simple searchable format.
    """

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# =========================================================
# KNOWN TOPIC ALIASES
# =========================================================

ALIASES = {

    # -----------------------------------------------------
    # CANTEEN
    # -----------------------------------------------------

    "canteen": "canteen",
    "cafeteria": "canteen",
    "food area": "canteen",
    "eating area": "canteen",
    "food place": "canteen",
    "lunch area": "canteen",
    "place to eat": "canteen",
    "somewhere to eat": "canteen",


    # -----------------------------------------------------
    # ADMINISTRATION
    # -----------------------------------------------------

    "administration": "administration",
    "admin": "administration",
    "administrative": "administration",
    "admin block": "administration",
    "administration block": "administration",


    # -----------------------------------------------------
    # FINANCE
    # -----------------------------------------------------

    "finance": "finance",
    "finance section": "finance",
    "finance office": "finance",
    "accounts": "finance",
    "accounts section": "finance",
    "accounts office": "finance",


    # -----------------------------------------------------
    # INFORMATION TECHNOLOGY
    # -----------------------------------------------------

    "information technology": "information technology",
    "it department": "information technology",
    "it department": "information technology",


    # -----------------------------------------------------
    # BUSINESS / HOSPITALITY
    # -----------------------------------------------------

    "business management": (
        "business management & hospitality"
    ),

    "hospitality management": (
        "business management & hospitality"
    ),

    "business management and hospitality": (
        "business management & hospitality"
    ),

    "hm": (
        "business management & hospitality"
    ),


    # -----------------------------------------------------
    # PRINCIPAL
    # -----------------------------------------------------

    "principal": "principal",
    "college principal": "principal",


    # -----------------------------------------------------
    # VICE PRINCIPAL
    # -----------------------------------------------------

    "vice principal": "vice_principal",
    "vice-principal": "vice_principal",


    # -----------------------------------------------------
    # COURSES
    # -----------------------------------------------------

    "bit": (
        "Bachelor of Information Technology"
    ),

    "b i t": (
        "Bachelor of Information Technology"
    ),

    "bachelor of information technology": (
        "Bachelor of Information Technology"
    ),


    "bcs": (
        "Bachelor of Computer Science"
    ),

    "b c s": (
        "Bachelor of Computer Science"
    ),

    "bachelor of computer science": (
        "Bachelor of Computer Science"
    ),


    "mcs": (
        "Masters of Computer Science"
    ),

    "m c s": (
        "Masters of Computer Science"
    ),

    "masters of computer science": (
        "Masters of Computer Science"
    ),


    "bba": (
        "Bachelor of Business Administration"
    ),

    "b b a": (
        "Bachelor of Business Administration"
    ),

    "bachelor of business administration": (
        "Bachelor of Business Administration"
    ),


    "bhm": (
        "Bachelor of Hospitality Management"
    ),

    "b h m": (
        "Bachelor of Hospitality Management"
    ),

    "bachelor of hospitality management": (
        "Bachelor of Hospitality Management"
    ),


    "mba": (
        "Masters of Business Administration"
    ),

    "m b a": (
        "Masters of Business Administration"
    ),

    "masters of business administration": (
        "Masters of Business Administration"
    ),

}


# =========================================================
# FIND LOCAL TOPIC
# =========================================================

def find_topic(question):

    normalized = normalize_text(question)

    matches = []

    # Check longer phrases first
    sorted_aliases = sorted(
        ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, topic in sorted_aliases:

        alias_normalized = normalize_text(alias)

        pattern = (
            r"\b"
            + re.escape(alias_normalized)
            + r"\b"
        )

        if re.search(
            pattern,
            normalized
        ):

            if topic not in matches:
                matches.append(topic)

    if matches:
        return matches[0]

    return ""


# =========================================================
# DETECT INTENT
# =========================================================

def detect_intent(question):

    normalized = normalize_text(question)


    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    location_phrases = [
        "where",
        "where is",
        "where are",
        "where can i find",
        "where can we find",
        "location",
        "located",
        "find",
        "floor",
        "room",
        "office",
        "situated",
        "place"
    ]

    if any(
        phrase in normalized
        for phrase in location_phrases
    ):

        return "location"


    # -----------------------------------------------------
    # AVAILABILITY
    # -----------------------------------------------------

    availability_phrases = [
        "is there",
        "are there",
        "do you have",
        "does the college have",
        "does college have",
        "available",
        "availability"
    ]

    if any(
        phrase in normalized
        for phrase in availability_phrases
    ):

        return "availability"


    # -----------------------------------------------------
    # HOD
    # -----------------------------------------------------

    hod_phrases = [
        "hod",
        "head of department",
        "department head",
        "who is the head",
        "who heads",
        "who leads",
        "who is in charge",
        "responsible for the department"
    ]

    if any(
        phrase in normalized
        for phrase in hod_phrases
    ):

        return "hod"


    # -----------------------------------------------------
    # VICE PRINCIPAL
    # -----------------------------------------------------

    if "vice principal" in normalized:

        return "vice_principal"


    # -----------------------------------------------------
    # PRINCIPAL
    # -----------------------------------------------------

    if "principal" in normalized:

        return "principal"


    # -----------------------------------------------------
    # DURATION
    # -----------------------------------------------------

    duration_phrases = [
        "how long",
        "duration",
        "how many years",
        "how many year",
        "years",
        "year"
    ]

    if any(
        phrase in normalized
        for phrase in duration_phrases
    ):

        return "duration"


    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    email_phrases = [
        "email",
        "e mail",
        "email address",
        "mail address",
        "contact email"
    ]

    if any(
        phrase in normalized
        for phrase in email_phrases
    ):

        return "email"


    # -----------------------------------------------------
    # ADMISSION
    # -----------------------------------------------------

    admission_phrases = [
        "admission",
        "apply",
        "application",
        "enroll",
        "enrollment",
        "join",
        "register"
    ]

    if any(
        phrase in normalized
        for phrase in admission_phrases
    ):

        return "admission"


    # -----------------------------------------------------
    # OFFICE HOURS
    # -----------------------------------------------------

    office_hours_phrases = [
        "office hours",
        "opening hours",
        "opening time",
        "closing time",
        "when does the office open",
        "when does the office close",
        "when is the office open",
        "when is the college open"
    ]

    if any(
        phrase in normalized
        for phrase in office_hours_phrases
    ):

        return "office_hours"


    # -----------------------------------------------------
    # DESCRIPTION
    # -----------------------------------------------------

    description_phrases = [
        "what is",
        "what are",
        "tell me about",
        "describe",
        "description",
        "information about"
    ]

    if any(
        phrase in normalized
        for phrase in description_phrases
    ):

        return "description"


    return "general"


# =========================================================
# GET FAQ QUESTIONS DIRECTLY FROM DATABASE
# =========================================================

def get_database_questions():

    try:

        conn = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT question
            FROM faq
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            row[0]
            for row in rows
        ]

    except Exception as e:

        print(
            "Could not load FAQ questions:",
            e
        )

        return []


# =========================================================
# DETERMINE CATEGORY
# =========================================================

def determine_category(
    topic,
    intent
):

    if intent in [
        "location",
        "availability",
        "office_hours",
        "admission"
    ]:

        return "faq"


    if intent in [
        "hod",
        "principal",
        "vice_principal",
        "email"
    ]:

        return "faculty"


    if intent == "duration":

        return "courses"


    if topic in [
        "information technology",
        "business management & hospitality"
    ]:

        return "departments"


    if topic in [
        "Bachelor of Information Technology",
        "Bachelor of Computer Science",
        "Masters of Computer Science",
        "Bachelor of Business Administration",
        "Bachelor of Hospitality Management",
        "Masters of Business Administration"
    ]:

        return "courses"


    return "general"


# =========================================================
# LOCAL ANALYSIS
# =========================================================

def analyze_locally(question):

    normalized = normalize_text(
        question
    )

    topic = find_topic(
        question
    )

    intent = detect_intent(
        question
    )

    category = determine_category(
        topic,
        intent
    )

    return {

        "category": category,

        "keyword": topic,

        "intent": intent,

        "normalized_question": normalized,

        "source": "local"

    }


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(question):

    database_questions = (
        get_database_questions()
    )

    faq_list = "\n".join(
        f"- {q}"
        for q in database_questions
    )


    prompt = f"""
You are a query analyzer for a college
receptionist.

DO NOT answer the user's question.

Your job is ONLY to understand what
information the visitor is requesting.

The visitor may use completely different
wording from the database question.

Identify:

1. category
2. keyword
3. intent

Possible categories:

faq
college_info
departments
faculty
courses
general

Possible intents:

location
availability
hod
principal
vice_principal
description
duration
email
office_hours
admission
general

Known FAQ questions currently in the database:

{faq_list}

Known topics include:

canteen
administration
finance
information technology
business management & hospitality
principal
vice principal
BIT
BCS
MCS
BBA
BHM
MBA

Examples:

User:
"Where is the cafeteria?"

Return:

{{
    "category": "faq",
    "keyword": "canteen",
    "intent": "location"
}}

User:
"Does the college have somewhere to eat?"

Return:

{{
    "category": "faq",
    "keyword": "canteen",
    "intent": "availability"
}}

User:
"Where can I find the finance office?"

Return:

{{
    "category": "faq",
    "keyword": "finance",
    "intent": "location"
}}

User:
"How many years do I study BIT?"

Return:

{{
    "category": "courses",
    "keyword": "Bachelor of Information Technology",
    "intent": "duration"
}}

User:
"Who is responsible for the IT department?"

Return:

{{
    "category": "departments",
    "keyword": "information technology",
    "intent": "hod"
}}

Return ONLY valid JSON.

User question:

{question}
"""


    try:

        response = client.models.generate_content(
            model=ANALYZER_MODEL,
            contents=prompt
        )

        text = response.text.strip()


        # Remove Markdown code fences
        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```",
            "",
            text
        )

        text = text.strip()


        result = json.loads(
            text
        )


        return {

            "category": result.get(
                "category",
                "general"
            ),

            "keyword": result.get(
                "keyword",
                ""
            ),

            "intent": result.get(
                "intent",
                "general"
            ),

            "normalized_question":
                normalize_text(question),

            "source": "gemini"

        }


    except Exception as e:

        print(
            "Query analyzer error:",
            e
        )

        return {

            "category": "general",

            "keyword": "",

            "intent": "general",

            "normalized_question":
                normalize_text(question),

            "source": "fallback"

        }


# =========================================================
# MAIN ANALYZER
# =========================================================

def analyze_question(question):

    # -----------------------------------------------------
    # First try local analysis
    # -----------------------------------------------------

    local_result = analyze_locally(
        question
    )


    # -----------------------------------------------------
    # If we understand the topic locally,
    # don't use Gemini.
    # -----------------------------------------------------

    if local_result["keyword"]:

        print(
            "Query Analyzer: LOCAL"
        )

        print(
            f"Topic: {local_result['keyword']}"
        )

        print(
            f"Intent: {local_result['intent']}"
        )

        return local_result


    # -----------------------------------------------------
    # Otherwise let Gemini classify it
    # -----------------------------------------------------

    print(
        "Query Analyzer: GEMINI"
    )

    result = analyze_with_gemini(
        question
    )


    print(
        f"Topic: {result['keyword']}"
    )

    print(
        f"Intent: {result['intent']}"
    )

    return result