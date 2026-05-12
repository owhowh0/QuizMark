from __future__ import annotations

from quizmark.models import MediaReference, QuizData


def export_text(quiz: QuizData) -> str:
    lines: list[str] = [f"Quiz: {quiz.title}"]
    if quiz.media:
        lines.extend(_render_media_text(quiz.media, indent=""))
    for idx, question in enumerate(quiz.questions, start=1):
        header = f"{idx}. {question.text}"
        if question.points is not None:
            header += f" ({question.points} pts)"
        lines.append(header)
        question_media = _combined_media(question.media, question.image)
        if question_media:
            lines.extend(_render_media_text(question_media, indent="   "))
        for answer in question.answers:
            mark = "*" if answer.correct else ""
            content = answer.text or ""
            lines.append(f"   {answer.label}. {content} {mark}".rstrip())
            answer_media = _combined_media(answer.media, answer.image)
            if answer_media:
                lines.extend(_render_media_text(answer_media, indent="      "))
    return "\n".join(lines)


def _render_media_text(media_list, indent: str) -> list[str]:
    lines: list[str] = []
    for media in media_list:
        label = media.kind
        lines.append(f"{indent}[{label}: {media.value}]")
    return lines


def _combined_media(media_list, image) -> list[MediaReference]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return items
