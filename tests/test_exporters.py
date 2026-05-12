from quizmark.parser import QuizMarkParser
from quizmark.exporters import (
    export_docx,
    export_html,
    export_json,
    export_moodle_xml,
    export_pdf,
)


def test_exporters_output():
    text = """
QUIZ: Sample
QUESTION: What is 2+2?
IMAGE: "images/board.png"
A: 3
B: 4 *
""".strip()
    quiz = QuizMarkParser().parse_text(text)
    assert "<html" in export_html(quiz)
    assert "\"title\": \"Sample\"" in export_json(quiz)
    moodle_xml = export_moodle_xml(quiz)
    assert "<quiz>" in moodle_xml
    assert "images/board.png" in moodle_xml
    assert len(export_docx(quiz)) > 0
    assert len(export_pdf(quiz)) > 0
