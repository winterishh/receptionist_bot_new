import sqlite3

from config import DATABASE_PATH
from ai.query_analyzer import analyze_question


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# =========================================================
# FAQ SEARCH
# =========================================================

def search_faq(keyword, intent, original_question):
    """
    Search FAQ using the analyzer's keyword and intent.

    The important part is that we score matching FAQ rows
    instead of simply taking the first matching row.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, answer
        FROM faq
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    keyword = (keyword or "").lower()
    original_question = original_question.lower()

    best_answer = None
    best_score = 0

    # -----------------------------------------------------
    # Words that indicate different intents
    # -----------------------------------------------------

    location_words = [
        "where",
        "location",
        "located",
        "find",
        "place",
        "floor",
        "room",
        "situated",
        "office"
    ]

    existence_words = [
        "is there",
        "are there",
        "do you have",
        "does the college have",
        "available"
    ]

    hours_words = [
        "office hours",
        "opening hours",
        "opening time",
        "closing time",
        "open",
        "close"
    ]

    admission_words = [
        "admission",
        "apply",
        "application",
        "enroll",
        "enrollment",
        "register"
    ]

    # -----------------------------------------------------
    # Search every FAQ
    # -----------------------------------------------------

    for faq_question, answer in rows:

        faq_lower = faq_question.lower()

        score = 0

        # -------------------------------------------------
        # Keyword match
        # -------------------------------------------------

        if keyword and keyword in faq_lower:
            score += 5

        # -------------------------------------------------
        # Original question word matching
        # -------------------------------------------------

        original_words = original_question.split()

        for word in original_words:

            if len(word) > 2 and word in faq_lower:
                score += 1

        # -------------------------------------------------
        # Intent matching
        # -------------------------------------------------

        if intent == "location":

            if any(word in faq_lower for word in location_words):
                score += 6

        elif intent == "office_hours":

            if any(word in faq_lower for word in hours_words):
                score += 8

        elif intent == "admission":

            if any(word in faq_lower for word in admission_words):
                score += 8

        elif intent == "general":

            # If the user asks whether something exists,
            # prefer an existence FAQ.
            if any(word in faq_lower for word in existence_words):
                score += 4

        # -------------------------------------------------
        # Prevent "is there a canteen?" from winning
        # when the user actually asks for a location.
        # -------------------------------------------------

        if intent == "location":

            if any(word in faq_lower for word in existence_words):
                score -= 5

        # -------------------------------------------------
        # Keep the best result
        # -------------------------------------------------

        if score > best_score:
            best_score = score
            best_answer = answer

    # -----------------------------------------------------
    # Require a reasonable match
    # -----------------------------------------------------

    if best_score >= 5:
        return best_answer

    return None


# =========================================================
# COLLEGE INFORMATION SEARCH
# =========================================================

def search_college_info(keyword, intent, original_question):
    """
    Search college_info table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, answer
        FROM college_info
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    keyword = (keyword or "").lower()
    original_question = original_question.lower()

    best_answer = None
    best_score = 0

    for question, answer in rows:

        question_lower = question.lower()

        score = 0

        if keyword and keyword in question_lower:
            score += 5

        for word in original_question.split():

            if len(word) > 2 and word in question_lower:
                score += 1

        if intent == "location":

            location_words = [
                "where",
                "location",
                "located",
                "place"
            ]

            if any(
                word in question_lower
                for word in location_words
            ):
                score += 5

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score >= 5:
        return best_answer

    return None


# =========================================================
# DEPARTMENT SEARCH
# =========================================================

def search_departments(keyword, intent):

    if not keyword:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            department_name,
            hod,
            description
        FROM departments
    """)

    rows = cursor.fetchall()

    conn.close()

    keyword = keyword.lower()

    for department, hod, description in rows:

        department_lower = department.lower()

        # -------------------------------------------------
        # Information Technology
        # -------------------------------------------------

        if (
            keyword == "information technology"
            and "information technology"
            in department_lower
        ):

            if intent == "hod":

                return (
                    f"The HOD of {department} "
                    f"is {hod}."
                )

            return description

        # -------------------------------------------------
        # Business / Hospitality
        # -------------------------------------------------

        if (
            keyword ==
            "business management & hospitality"
            and (
                "business" in department_lower
                or "hospitality" in department_lower
            )
        ):

            if intent == "hod":

                return (
                    f"The HOD of {department} "
                    f"is {hod}."
                )

            return description

    return None


# =========================================================
# FACULTY SEARCH
# =========================================================

def search_faculty(keyword, intent):

    if not keyword:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            department,
            designation,
            email
        FROM faculty
    """)

    rows = cursor.fetchall()

    conn.close()

    keyword = keyword.lower()

    for name, department, designation, email in rows:

        designation_lower = designation.lower()

        # -------------------------------------------------
        # Principal
        # -------------------------------------------------

        if (
            keyword == "principal"
            and "principal" in designation_lower
            and "vice" not in designation_lower
        ):

            if intent == "email":

                return email

            return (
                f"{name} is the Principal "
                f"of the college. "
                f"Email: {email}"
            )

        # -------------------------------------------------
        # Vice Principal
        # -------------------------------------------------

        if (
            keyword == "vice_principal"
            and (
                "vice-principal" in designation_lower
                or "vice principal" in designation_lower
            )
        ):

            if intent == "email":

                return email

            return (
                f"{name} is the Vice-Principal "
                f"of the college. "
                f"Email: {email}"
            )

    return None


# =========================================================
# COURSE SEARCH
# =========================================================

def search_courses(keyword, intent):

    if not keyword:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            course_name,
            duration,
            description
        FROM courses
    """)

    rows = cursor.fetchall()

    conn.close()

    keyword = keyword.lower()

    for course, duration, description in rows:

        if course.lower() == keyword:

            # -------------------------------------------------
            # Duration question
            # -------------------------------------------------

            if intent == "duration":

                return (
                    f"{course} is a {duration} program."
                )

            # -------------------------------------------------
            # Normal course question
            # -------------------------------------------------

            return (
                f"{course}\n\n"
                f"Duration: {duration}\n\n"
                f"{description}"
            )

    return None


# =========================================================
# MAIN DATABASE SEARCH
# =========================================================

def search_database(question):

    # -----------------------------------------------------
    # Analyze the question
    # -----------------------------------------------------

    analysis = analyze_question(question)

    keyword = analysis.get("keyword", "")
    intent = analysis.get("intent", "general")
    source = analysis.get("source", "unknown")

    print(
        f"\nDatabase search:"
        f"\n  Keyword: {keyword}"
        f"\n  Intent: {intent}"
        f"\n  Analyzer: {source}"
    )

    # -----------------------------------------------------
    # FAQ
    # -----------------------------------------------------

    answer = search_faq(
        keyword,
        intent,
        question
    )

    if answer:

        print("Answer source: DATABASE / FAQ")

        return answer

    # -----------------------------------------------------
    # College Information
    # -----------------------------------------------------

    answer = search_college_info(
        keyword,
        intent,
        question
    )

    if answer:

        print(
            "Answer source: "
            "DATABASE / COLLEGE INFO"
        )

        return answer

    # -----------------------------------------------------
    # Departments
    # -----------------------------------------------------

    answer = search_departments(
        keyword,
        intent
    )

    if answer:

        print(
            "Answer source: "
            "DATABASE / DEPARTMENT"
        )

        return answer

    # -----------------------------------------------------
    # Faculty
    # -----------------------------------------------------

    answer = search_faculty(
        keyword,
        intent
    )

    if answer:

        print(
            "Answer source: "
            "DATABASE / FACULTY"
        )

        return answer

    # -----------------------------------------------------
    # Courses
    # -----------------------------------------------------

    answer = search_courses(
        keyword,
        intent
    )

    if answer:

        print(
            "Answer source: "
            "DATABASE / COURSE"
        )

        return answer

    # -----------------------------------------------------
    # Nothing found
    # -----------------------------------------------------

    print("Database: No matching answer")

    return None