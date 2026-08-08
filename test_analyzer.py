from ai.query_analyzer import analyze_question


questions = [
    "Where is the canteen?",
    "Where can I find the cafeteria?",
    "Where can I get food?",
    "Who is the IT HOD?",
    "Who heads the IT department?",
    "How many years is BIT?",
    "What is the duration of BBA?",
    "Where is the administration block?",
    "What are the office hours?",
    "How do I apply for admission?"
]


print("\n======================================")
print("       QUERY ANALYZER TEST")
print("======================================\n")


for question in questions:

    result = analyze_question(question)

    print("Question:")
    print(question)

    print("\nAnalyzer result:")
    print(result)

    print("\n--------------------------------------\n")