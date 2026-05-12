from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ImageReference:
    path: str
    line: int | None = None


@dataclass(slots=True)
class MediaReference:
    kind: str
    value: str
    line: int | None = None


@dataclass(slots=True)
class Answer:
    label: str
    text: str | None
    image: ImageReference | None
    correct: bool
    media: list[MediaReference] = field(default_factory=list)
    line: int | None = None


@dataclass(slots=True)
class Question:
    text: str
    points: float | None
    image: ImageReference | None
    media: list[MediaReference] = field(default_factory=list)
    answers: list[Answer] = field(default_factory=list)
    line: int | None = None


@dataclass(slots=True)
class Theme:
    properties: dict[str, Any] = field(default_factory=dict)
    styles: dict[str, dict[str, Any]] = field(default_factory=dict)
    line: int | None = None


@dataclass(slots=True)
class Metadata:
    time_limit: float | None = None
    pass_mark: float | None = None
    shuffle: bool | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QuizData:
    title: str
    theme: Theme | None
    metadata: Metadata
    media: list[MediaReference]
    questions: list[Question]
    line: int | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "theme": _theme_to_dict(self.theme),
            "metadata": _metadata_to_dict(self.metadata),
            "media": [_media_to_dict(m) for m in self.media],
            "questions": [_question_to_dict(q) for q in self.questions],
            "source": self.source,
        }


def _image_to_dict(image: ImageReference | None) -> dict[str, Any] | None:
    if image is None:
        return None
    return {"path": image.path, "line": image.line}


def _answer_to_dict(answer: Answer) -> dict[str, Any]:
    return {
        "label": answer.label,
        "text": answer.text,
        "image": _image_to_dict(answer.image),
        "media": _media_list_to_dict(answer.media, answer.image),
        "correct": answer.correct,
        "line": answer.line,
    }


def _question_to_dict(question: Question) -> dict[str, Any]:
    return {
        "text": question.text,
        "points": question.points,
        "image": _image_to_dict(question.image),
        "media": _media_list_to_dict(question.media, question.image),
        "answers": [_answer_to_dict(a) for a in question.answers],
        "line": question.line,
    }


def _theme_to_dict(theme: Theme | None) -> dict[str, Any] | None:
    if theme is None:
        return None
    return {
        "properties": theme.properties,
        "styles": theme.styles,
        "line": theme.line,
    }


def _metadata_to_dict(metadata: Metadata) -> dict[str, Any]:
    return {
        "time_limit": metadata.time_limit,
        "pass_mark": metadata.pass_mark,
        "shuffle": metadata.shuffle,
        "extras": metadata.extras,
    }


def _media_to_dict(media: MediaReference) -> dict[str, Any]:
    return {
        "kind": media.kind,
        "value": media.value,
        "line": media.line,
    }


def _media_list_to_dict(
    media_list: list[MediaReference], image: ImageReference | None
) -> list[dict[str, Any]]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return [_media_to_dict(m) for m in items]
