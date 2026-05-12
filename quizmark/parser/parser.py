from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from quizmark.models import Answer, ImageReference, MediaReference, Metadata, Question, QuizData, Theme
from quizmark.parser.errors import ParserError


_THEME_SELECTORS = {"quiz", "question", "answer", "correct", "wrong"}
_MEDIA_KINDS = {
    "IMAGE": "image",
    "AUDIO": "audio",
    "VIDEO": "video",
    "ATTACH": "attachment",
    "MATH": "math",
}


@dataclass
class _Line:
    number: int
    text: str


class _LineStream:
    def __init__(self, text: str):
        self._lines = [
            _Line(i + 1, line.rstrip("\n")) for i, line in enumerate(text.splitlines())
        ]
        self._index = 0

    def peek(self) -> _Line | None:
        idx = self._skip_blanks(self._index)
        if idx >= len(self._lines):
            return None
        return self._lines[idx]

    def next(self) -> _Line | None:
        idx = self._skip_blanks(self._index)
        if idx >= len(self._lines):
            return None
        self._index = idx + 1
        return self._lines[idx]

    def _skip_blanks(self, idx: int) -> int:
        while idx < len(self._lines):
            line = self._lines[idx].text.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                idx += 1
                continue
            break
        return idx


class QuizMarkParser:
    def parse_text(self, text: str, source: str | None = None) -> QuizData:
        stream = _LineStream(text)
        quiz_line = stream.next()
        if quiz_line is None:
            raise ParserError("Expected QUIZ header", line=1, source=source)
        if not quiz_line.text.strip().startswith("QUIZ:"):
            raise ParserError("Expected QUIZ header", line=quiz_line.number, source=source)

        title = quiz_line.text.split(":", 1)[1].strip()
        if not title:
            raise ParserError("Quiz title cannot be empty", line=quiz_line.number, source=source)

        theme = None
        metadata = Metadata()
        media: list[MediaReference] = []
        questions: list[Question] = []

        while True:
            next_line = stream.peek()
            if next_line is None:
                break
            stripped = next_line.text.strip()
            if stripped.startswith("QUESTION"):
                break
            if stripped.startswith("THEME"):
                if theme is not None:
                    raise ParserError(
                        "Duplicate THEME block", line=next_line.number, source=source
                    )
                theme = self._parse_theme(stream, source)
                continue
            if self._is_media_line(stripped):
                stream.next()
                media_ref, media_correct = self._parse_media_line(
                    stripped, next_line.number, source
                )
                if media_correct:
                    raise ParserError(
                        "Correct marker not allowed on quiz media",
                        line=next_line.number,
                        source=source,
                    )
                media.append(media_ref)
                continue
            key, value, line_no = self._parse_metadata(stream, source)
            if key == "TIME_LIMIT":
                metadata.time_limit = self._ensure_number(value, key, line_no, source)
            elif key == "PASS_MARK":
                metadata.pass_mark = self._ensure_number(value, key, line_no, source)
            elif key == "SHUFFLE":
                if not isinstance(value, bool):
                    raise ParserError("SHUFFLE must be true or false", line=line_no, source=source)
                metadata.shuffle = value
            else:
                metadata.extras[key] = value

        while True:
            next_line = stream.peek()
            if next_line is None:
                break
            if not next_line.text.strip().startswith("QUESTION"):
                raise ParserError(
                    "Expected QUESTION block", line=next_line.number, source=source
                )
            questions.append(self._parse_question(stream, source))

        return QuizData(
            title=title,
            theme=theme,
            metadata=metadata,
            media=media,
            questions=questions,
            line=quiz_line.number,
            source=source,
        )

    def _parse_theme(self, stream: _LineStream, source: str | None) -> Theme:
        theme_line = stream.next()
        if theme_line is None:
            raise ParserError("Expected THEME block", source=source)
        theme = Theme(line=theme_line.number)
        line_text = theme_line.text.strip()
        if "{" in line_text:
            if not line_text.endswith("{"):
                raise ParserError("Unexpected content after '{'", line=theme_line.number, source=source)
        else:
            brace_line = stream.next()
            if brace_line is None or brace_line.text.strip() != "{":
                raise ParserError("Expected '{' after THEME", line=theme_line.number, source=source)

        while True:
            line = stream.next()
            if line is None:
                raise ParserError("Unclosed THEME block", source=source)
            stripped = line.text.strip()
            if stripped == "}":
                break
            if "[" in stripped and "]" in stripped:
                selector, rest = stripped.split("[", 1)
                selector = selector.strip()
                if selector not in _THEME_SELECTORS:
                    raise ParserError(
                        f"Unknown theme selector '{selector}'",
                        line=line.number,
                        source=source,
                    )
                attr_text = rest.rsplit("]", 1)[0]
                attrs = self._parse_attributes(attr_text, line.number, source)
                theme.styles.setdefault(selector, {}).update(attrs)
            elif "=" in stripped:
                key, value = stripped.split("=", 1)
                theme.properties[key.strip()] = self._parse_value(value.strip())
            else:
                raise ParserError(
                    "Invalid theme statement", line=line.number, source=source
                )
        return theme

    def _parse_attributes(self, text: str, line: int, source: str | None) -> dict[str, Any]:
        attrs: dict[str, Any] = {}
        for part in [p.strip() for p in text.split(",") if p.strip()]:
            if "=" not in part:
                raise ParserError("Invalid theme attribute", line=line, source=source)
            key, value = part.split("=", 1)
            attrs[key.strip()] = self._parse_value(value.strip())
        return attrs

    def _parse_metadata(self, stream: _LineStream, source: str | None) -> tuple[str, Any, int]:
        line = stream.next()
        if line is None:
            raise ParserError("Expected metadata entry", source=source)
        if ":" not in line.text:
            raise ParserError("Invalid metadata entry", line=line.number, source=source)
        key, value = line.text.split(":", 1)
        key = key.strip().upper()
        if not key:
            raise ParserError("Metadata key cannot be empty", line=line.number, source=source)
        return key, self._parse_value(value.strip()), line.number

    def _parse_question(self, stream: _LineStream, source: str | None) -> Question:
        line = stream.next()
        if line is None:
            raise ParserError("Expected QUESTION", source=source)
        match = re.match(r"^QUESTION\s*(?:\(([^)]*)\))?\s*:\s*(.*)$", line.text.strip())
        if not match:
            raise ParserError("Invalid QUESTION syntax", line=line.number, source=source)
        points = None
        attrs = match.group(1)
        if attrs:
            for part in [p.strip() for p in attrs.split(",") if p.strip()]:
                if part.startswith("points="):
                    points = float(part.split("=", 1)[1])
                else:
                    raise ParserError(
                        f"Unknown question attribute '{part}'",
                        line=line.number,
                        source=source,
                    )
        text = match.group(2).strip()
        if not text:
            raise ParserError("Question text cannot be empty", line=line.number, source=source)
        question = Question(
            text=text,
            points=points,
            image=None,
            media=[],
            answers=[],
            line=line.number,
        )

        while True:
            next_line = stream.peek()
            if next_line is None:
                break
            stripped = next_line.text.strip()
            if self._is_media_line(stripped):
                stream.next()
                media_ref, media_correct = self._parse_media_line(
                    stripped, next_line.number, source
                )
                if media_correct:
                    raise ParserError(
                        "Correct marker not allowed on question media",
                        line=next_line.number,
                        source=source,
                    )
                question.media.append(media_ref)
                if media_ref.kind == "image" and question.image is None:
                    question.image = ImageReference(
                        path=media_ref.value, line=media_ref.line
                    )
                continue
            if self._is_answer_line(stripped) or stripped.startswith("QUESTION"):
                break
            raise ParserError("Unexpected content after question", line=next_line.number, source=source)

        while True:
            next_line = stream.peek()
            if next_line is None or next_line.text.strip().startswith("QUESTION"):
                break
            stripped = next_line.text.strip()
            if not self._is_answer_line(stripped):
                raise ParserError("Expected answer label", line=next_line.number, source=source)
            question.answers.append(self._parse_answer(stream, source))

        return question

    def _parse_answer(self, stream: _LineStream, source: str | None) -> Answer:
        line = stream.next()
        if line is None:
            raise ParserError("Expected answer", source=source)
        label, rest = line.text.split(":", 1)
        label = label.strip()
        rest = rest.strip()
        correct = False
        if rest.endswith("*"):
            correct = True
            rest = rest[:-1].strip()

        text = None
        image = None
        media: list[MediaReference] = []

        if rest:
            if self._is_media_line(rest):
                media_ref, media_correct = self._parse_media_line(rest, line.number, source)
                correct = correct or media_correct
                media.append(media_ref)
                if media_ref.kind == "image" and image is None:
                    image = ImageReference(path=media_ref.value, line=media_ref.line)
            else:
                text = rest
        else:
            next_line = stream.peek()
            if next_line is not None:
                stripped = next_line.text.strip()
                if self._is_media_line(stripped):
                    stream.next()
                    media_ref, media_correct = self._parse_media_line(
                        stripped, next_line.number, source
                    )
                    correct = correct or media_correct
                    media.append(media_ref)
                    if media_ref.kind == "image" and image is None:
                        image = ImageReference(path=media_ref.value, line=media_ref.line)
                elif stripped and not self._is_answer_line(stripped) and not stripped.startswith("QUESTION"):
                    stream.next()
                    text = stripped.rstrip("*").strip()
                    if stripped.endswith("*"):
                        correct = True

        while True:
            next_line = stream.peek()
            if next_line is None:
                break
            stripped = next_line.text.strip()
            if not self._is_media_line(stripped):
                break
            stream.next()
            media_ref, media_correct = self._parse_media_line(
                stripped, next_line.number, source
            )
            correct = correct or media_correct
            media.append(media_ref)
            if media_ref.kind == "image" and image is None:
                image = ImageReference(path=media_ref.value, line=media_ref.line)

        if text is None and not media:
            raise ParserError("Answer requires text or media", line=line.number, source=source)

        return Answer(
            label=label,
            text=text,
            image=image,
            media=media,
            correct=correct,
            line=line.number,
        )

    def _parse_media_line(
        self, text: str, line: int, source: str | None
    ) -> tuple[MediaReference, bool]:
        key, raw_value = text.split(":", 1)
        kind = _MEDIA_KINDS.get(key.strip().upper())
        if kind is None:
            raise ParserError("Unknown media type", line=line, source=source)
        value = raw_value.strip()
        correct = False
        if value.endswith("*"):
            correct = True
            value = value[:-1].strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if not value:
            raise ParserError("Media value cannot be empty", line=line, source=source)
        return MediaReference(kind=kind, value=value, line=line), correct

    def _parse_value(self, value: str) -> Any:
        if not value:
            return ""
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.lower() in {"true", "false"}:
            return value.lower() == "true"
        if value.endswith("%"):
            number = value[:-1]
            if self._is_number(number):
                return float(number)
        if self._is_number(value):
            return float(value) if "." in value else int(value)
        return value

    def _ensure_number(self, value: Any, key: str, line: int, source: str | None) -> float:
        if not isinstance(value, (int, float)):
            raise ParserError(f"{key} must be a number", line=line, source=source)
        return float(value)

    def _is_number(self, value: str) -> bool:
        try:
            float(value)
        except ValueError:
            return False
        return True

    def _is_answer_line(self, text: str) -> bool:
        match = re.match(r"^[A-Z]\s*:", text)
        if not match:
            return False
        label = text.split(":", 1)[0].strip()
        return len(label) == 1 and label.isalpha()

    def _is_media_line(self, text: str) -> bool:
        for key in _MEDIA_KINDS:
            if text.upper().startswith(f"{key}:"):
                return True
        return False
