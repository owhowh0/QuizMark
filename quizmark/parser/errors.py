from __future__ import annotations


class QuizMarkError(Exception):
    def __init__(self, message: str, line: int | None = None, source: str | None = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.source = source

    def __str__(self) -> str:
        if self.line is None:
            return self.message
        location = f"line {self.line}"
        if self.source:
            location = f"{self.source}:{self.line}"
        return f"{location}: {self.message}"


class ParserError(QuizMarkError):
    pass


class ValidationError(QuizMarkError):
    pass
