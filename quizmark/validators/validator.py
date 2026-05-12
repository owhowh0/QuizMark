from __future__ import annotations

from quizmark.models import Answer, MediaReference, Question, QuizData
from quizmark.parser.errors import ValidationError

_ALLOWED_THEME_PROPERTIES = {
    "background",
    "foreground",
    "accent",
    "font",
    "spacing",
    "radius",
}
_ALLOWED_THEME_ATTRIBUTES = {"font", "size", "color", "weight", "spacing"}
_ALLOWED_MEDIA_KINDS = {"image", "audio", "video", "attachment", "math"}


def validate_quiz(quiz: QuizData) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if not quiz.questions:
        errors.append(ValidationError("Quiz must contain at least one question", line=quiz.line))

    if quiz.metadata.time_limit is not None and quiz.metadata.time_limit <= 0:
        errors.append(ValidationError("TIME_LIMIT must be positive"))
    if quiz.metadata.pass_mark is not None:
        if not (0 <= quiz.metadata.pass_mark <= 100):
            errors.append(ValidationError("PASS_MARK must be between 0 and 100"))

    if quiz.theme:
        for key in quiz.theme.properties:
            if key not in _ALLOWED_THEME_PROPERTIES:
                errors.append(ValidationError(f"Unknown theme property '{key}'", line=quiz.theme.line))
        for selector, attrs in quiz.theme.styles.items():
            for key in attrs:
                if key not in _ALLOWED_THEME_ATTRIBUTES:
                    errors.append(
                        ValidationError(
                            f"Unknown theme attribute '{key}' for '{selector}'",
                            line=quiz.theme.line,
                        )
                    )

    for question in quiz.questions:
        errors.extend(_validate_question(question))

    errors.extend(_validate_media_list(quiz.media, "quiz", quiz.line))

    return errors


def _validate_question(question: Question) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if question.points is not None and question.points <= 0:
        errors.append(ValidationError("Question points must be positive", line=question.line))
    if question.image and not question.image.path:
        errors.append(ValidationError("Question image path cannot be empty", line=question.line))
    if len(question.answers) < 2:
        errors.append(ValidationError("Each question needs at least two answers", line=question.line))
    correct = [a for a in question.answers if a.correct]
    if not correct:
        errors.append(ValidationError("Each question needs a correct answer", line=question.line))
    labels = set()
    for answer in question.answers:
        errors.extend(_validate_answer(answer, labels))
    errors.extend(_validate_media_list(question.media, "question", question.line))
    return errors


def _validate_answer(answer: Answer, labels: set[str]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if answer.label in labels:
        errors.append(ValidationError("Duplicate answer label", line=answer.line))
    labels.add(answer.label)
    if answer.image and not answer.image.path:
        errors.append(ValidationError("Answer image path cannot be empty", line=answer.line))
    if not answer.text and not answer.media:
        errors.append(ValidationError("Answer requires text or media", line=answer.line))
    errors.extend(_validate_media_list(answer.media, "answer", answer.line))
    return errors


def _validate_media_list(
    media_list: list[MediaReference], scope: str, line: int | None
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for media in media_list:
        if media.kind not in _ALLOWED_MEDIA_KINDS:
            errors.append(
                ValidationError(
                    f"Unknown media type '{media.kind}' on {scope}", line=media.line or line
                )
            )
        if not media.value:
            errors.append(
                ValidationError(
                    f"Media value cannot be empty on {scope}", line=media.line or line
                )
            )
    return errors
