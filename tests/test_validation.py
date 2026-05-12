from quizmark.parser import QuizMarkParser
from quizmark.validators import validate_quiz


def test_validation_requires_correct_answer():
    text = """
QUIZ: Sample
QUESTION: What is 2+2?
A: 3
B: 4
""".strip()
    quiz = QuizMarkParser().parse_text(text)
    errors = validate_quiz(quiz)
    assert any("correct answer" in e.message for e in errors)
