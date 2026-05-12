from __future__ import annotations

from quizmark.models import MediaReference, QuizData


def export_html(quiz: QuizData) -> str:
    theme = quiz.theme
    background = theme.properties.get("background") if theme else None
    foreground = theme.properties.get("foreground") if theme else None
    accent = theme.properties.get("accent") if theme else None
    base_font = theme.properties.get("font") if theme else None
    spacing = theme.properties.get("spacing") if theme else None
    radius = theme.properties.get("radius") if theme else None
    question_style = _style_from_theme(theme, "question")
    correct_style = _style_from_theme(theme, "correct")

    html = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        f"<title>{quiz.title}</title>",
        "<style>",
        "body { font-family: serif; margin: 2rem; }",
    ]
    if background:
        html.append(f"body {{ background: {background}; }}")
    if foreground:
        html.append(f"body {{ color: {foreground}; }}")
    if base_font:
        html.append(f"body {{ font-family: {base_font}; }}")
    if spacing:
        html.append(f"body {{ margin: {spacing}; }}")
    if question_style:
        html.append(f".qm-question {{ {question_style} }}")
    if correct_style:
        html.append(f".qm-correct {{ {correct_style} }}")
    html.extend(
        [
            ".qm-media { margin: 0.5rem 0; }",
            ".qm-media a { color: inherit; text-decoration: underline; }",
            ".qm-media img, .qm-media video { max-width: 100%; border-radius: 8px; }",
            ".qm-media audio { width: 100%; }",
            ".qm-math { font-style: italic; }",
            ".qm-answers { list-style: none; padding-left: 0; }",
            ".qm-answers li { margin: 0.25rem 0; }",
            ".qm-answer { padding: 0.5rem 0; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{quiz.title}</h1>",
        ]
    )

    if quiz.media:
        html.extend(_render_media_html(quiz.media))

    for idx, question in enumerate(quiz.questions, start=1):
        html.append(f"<section class=\"qm-question\">")
        html.append(f"<h2>{idx}. {question.text}</h2>")
        question_media = _combined_media(question.media, question.image)
        if question_media:
            html.extend(_render_media_html(question_media))
        html.append("<ul class=\"qm-answers\">")
        for answer in question.answers:
            cls = "qm-correct" if answer.correct else ""
            label = f"<strong>{answer.label}.</strong> "
            text = answer.text or ""
            html.append(f"<li class=\"qm-answer {cls}\">{label}{text}")
            answer_media = _combined_media(answer.media, answer.image)
            if answer_media:
                html.extend(_render_media_html(answer_media))
            html.append("</li>")
        html.append("</ul>")
        html.append("</section>")

    html.extend(["</body>", "</html>"])
    return "\n".join(html)


def _style_from_theme(theme, selector: str) -> str:
    if not theme:
        return ""
    style = theme.styles.get(selector, {})
    parts = []
    if "font" in style:
        parts.append(f"font-family: {style['font']}")
    if "size" in style:
        parts.append(f"font-size: {style['size']}px")
    if "color" in style:
        parts.append(f"color: {style['color']}")
    if "weight" in style:
        parts.append(f"font-weight: {style['weight']}")
    if "spacing" in style:
        parts.append(f"margin-bottom: {style['spacing']}")
    return "; ".join(parts)


def _render_media_html(media_list) -> list[str]:
    html: list[str] = []
    for media in media_list:
        if media.kind == "image":
            html.append(
                f"<div class=\"qm-media\"><img src=\"{media.value}\" alt=\"Image\" /></div>"
            )
        elif media.kind == "audio":
            html.append(
                f"<div class=\"qm-media\"><audio controls src=\"{media.value}\"></audio></div>"
            )
        elif media.kind == "video":
            html.append(
                f"<div class=\"qm-media\"><video controls src=\"{media.value}\"></video></div>"
            )
        elif media.kind == "attachment":
            html.append(
                f"<div class=\"qm-media\"><a href=\"{media.value}\">Attachment</a></div>"
            )
        elif media.kind == "math":
            html.append(f"<div class=\"qm-media qm-math\">\\({media.value}\\)</div>")
    return html


def _combined_media(media_list, image) -> list[MediaReference]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return items
