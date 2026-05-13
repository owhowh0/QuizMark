from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AnswerData:
    label: str
    text: Optional[str]
    image: Optional[str]
    correct: bool


@dataclass
class QuestionData:
    text: str
    points: Optional[float]
    image: Optional[str]
    answers: list = field(default_factory=list)

    @property
    def correct_answers(self) -> list["AnswerData"]:  # ← новое
        """Return only the answers marked as correct."""
        return [a for a in self.answers if a.correct]

@dataclass
class ThemeData:
    properties: dict = field(default_factory=dict)  # key -> value
    styles: dict = field(default_factory=dict)       # selector -> {attr: value}


@dataclass
class QuizData:
    title: str
    theme: Optional[ThemeData]
    metadata: dict = field(default_factory=dict)
    questions: list["QuestionData"] = field(default_factory=list)  # ← уточнён тип

    def to_dict(self) -> dict:  # ← новое
        """Serialize the quiz to a plain dict (useful for JSON export)."""
        return {
            "title": self.title,
            "metadata": self.metadata,
            "questions": [
                {
                    "text": q.text,
                    "points": q.points,
                    "image": q.image,
                    "answers": [
                        {
                            "label": a.label,
                            "text": a.text,
                            "image": a.image,
                            "correct": a.correct,
                        }
                        for a in q.answers
                    ],
                }
                for q in self.questions
            ],
        }
