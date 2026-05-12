from quizmark.parser import QuizMarkParser


def test_parse_basic_quiz():
    text = """
QUIZ: Sample
IMAGE: "images/cover.png"
QUESTION: What is 2+2?
VIDEO: "video/clip.mp4"
A: 3
B: 4 *
C: 5
""".strip()
    quiz = QuizMarkParser().parse_text(text)
    assert quiz.title == "Sample"
    assert quiz.media[0].kind == "image"
    assert len(quiz.questions) == 1
    assert quiz.questions[0].media[0].kind == "video"
    assert quiz.questions[0].answers[1].correct is True
