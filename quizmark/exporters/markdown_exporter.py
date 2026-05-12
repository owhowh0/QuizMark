from __future__ import annotations

from quizmark.models import MediaReference, QuizData


def export_markdown(quiz: QuizData) -> str:
    lines: list[str] = [f"# {quiz.title}"]
    if quiz.media:
        lines.extend(_render_media_markdown(quiz.media))
    for idx, question in enumerate(quiz.questions, start=1):
        header = f"## {idx}. {question.text}"
        if question.points is not None:
            header += f" ({question.points} pts)"
        lines.append(header)
        question_media = _combined_media(question.media, question.image)
        if question_media:
            lines.extend(_render_media_markdown(question_media))
        for answer in question.answers:
            mark = " **(correct)**" if answer.correct else ""
            text = answer.text or ""
            spacer = " " if text else ""
            lines.append(f"- {answer.label}. {text}{spacer}{mark}".rstrip())
            answer_media = _combined_media(answer.media, answer.image)
            if answer_media:
                for media_line in _render_media_markdown(answer_media):
                    lines.append(f"  {media_line}")
    return "\n".join(lines)


def _render_media_markdown(media_list) -> list[str]:
    lines: list[str] = []
    for media in media_list:
        if media.kind == "image":
            lines.append(f"![Image]({media.value})")
        elif media.kind == "audio":
            lines.append(f"[Audio]({media.value})")
        elif media.kind == "video":
            lines.append(f"[Video]({media.value})")
        elif media.kind == "attachment":
            lines.append(f"[Attachment]({media.value})")
        elif media.kind == "math":
            lines.append(f"${media.value}$")
    return lines


def _combined_media(media_list, image) -> list[MediaReference]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return items
