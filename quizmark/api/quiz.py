from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quizmark.exporters import (
    export_docx,
    export_html,
    export_json,
    export_markdown,
    export_moodle_xml,
    export_pdf,
    export_text,
    export_web_package,
)
from quizmark.models import QuizData
from quizmark.parser import QuizMarkParser
from quizmark.parser.errors import ParserError, ValidationError
from quizmark.validators import validate_quiz


@dataclass
class Quiz:
    data: QuizData

    @classmethod
    def load(cls, path: str | Path) -> "Quiz":
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        parser = QuizMarkParser()
        data = parser.parse_text(text, source=str(path))
        return cls(data=data)

    @classmethod
    def parse(cls, text: str, source: str | None = None) -> "Quiz":
        parser = QuizMarkParser()
        data = parser.parse_text(text, source=source)
        return cls(data=data)

    def validate(self, raise_on_error: bool = True) -> list[ValidationError]:
        errors = validate_quiz(self.data)
        if errors and raise_on_error:
            raise ValidationError("Validation failed", line=errors[0].line)
        return errors

    def to_json(self) -> str:
        return export_json(self.data)

    def render_html(self) -> str:
        return export_html(self.data)

    def render_markdown(self) -> str:
        return export_markdown(self.data)

    def render_text(self) -> str:
        return export_text(self.data)

    def render_moodle_xml(self) -> str:
        return export_moodle_xml(self.data)

    def render_docx(self) -> bytes:
        return export_docx(self.data)

    def render_pdf(self) -> bytes:
        return export_pdf(self.data)

    def render_web_package(self) -> dict[str, str]:
        return export_web_package(self.data)

    def export(self, format_name: str) -> str | dict[str, str]:
        format_name = format_name.lower()
        if format_name == "json":
            return self.to_json()
        if format_name == "html":
            return self.render_html()
        if format_name == "markdown":
            return self.render_markdown()
        if format_name == "text":
            return self.render_text()
        if format_name == "moodle":
            return self.render_moodle_xml()
        if format_name == "docx":
            return self.render_docx()
        if format_name == "pdf":
            return self.render_pdf()
        if format_name == "web":
            return self.render_web_package()
        raise ParserError(f"Unknown export format '{format_name}'")

    def to_dict(self) -> dict[str, Any]:
        return self.data.to_dict()
