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


@dataclass
class ThemeData:
    properties: dict = field(default_factory=dict)  # key -> value
    styles: dict = field(default_factory=dict)       # selector -> {attr: value}


@dataclass
class QuizData:
    title: str
    theme: Optional[ThemeData]
    metadata: dict = field(default_factory=dict)
    questions: list = field(default_factory=list)
