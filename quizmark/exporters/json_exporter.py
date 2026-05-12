from __future__ import annotations

import json

from quizmark.models import QuizData


def export_json(quiz: QuizData) -> str:
    return json.dumps(quiz.to_dict(), indent=2)
