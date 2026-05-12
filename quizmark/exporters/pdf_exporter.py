from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas

from quizmark.models import MediaReference, QuizData


def export_pdf(quiz: QuizData) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 72

    y = _draw_line(c, y, quiz.title, size=18)

    if quiz.media:
        y = _draw_media_block(c, y, quiz.media, "Quiz media")

    for idx, question in enumerate(quiz.questions, start=1):
        header = f"{idx}. {question.text}"
        if question.points is not None:
            header += f" ({question.points} pts)"
        y = _draw_line(c, y, header, size=14)

        question_media = _combined_media(question.media, question.image)
        if question_media:
            y = _draw_media_block(c, y, question_media, "Question media")

        for answer in question.answers:
            mark = " (correct)" if answer.correct else ""
            text = answer.text or ""
            y = _draw_line(c, y, f"{answer.label}. {text}{mark}")

            answer_media = _combined_media(answer.media, answer.image)
            if answer_media:
                y = _draw_media_block(c, y, answer_media, "Answer media")

    c.showPage()
    c.save()
    return buffer.getvalue()


def _draw_line(c, y: float, text: str, size: int = 11) -> float:
    if y < 72:
        c.showPage()
        y = 720
    c.setFont("Helvetica", size)
    c.drawString(72, y, text)
    return y - (size + 6)


def _draw_media_block(
    c, y: float, media_list: list[MediaReference], prefix: str
) -> float:
    y = _draw_line(c, y, f"{prefix}:")
    for media in media_list:
        if media.kind == "image":
            y = _draw_image(c, y, media.value)
            continue
        if media.kind == "math":
            y = _draw_math(c, y, media.value)
            continue
        label = f"- {media.kind}: {media.value}"
        y = _draw_line(c, y, label)
        if media.kind in {"audio", "video", "attachment"}:
            y = _add_link(c, y + 6, media.value)
    return y


def _combined_media(media_list, image) -> list[MediaReference]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return items


def _draw_image(c, y: float, value: str) -> float:
    path = Path(value)
    if not path.exists():
        return _draw_line(c, y, f"- image (missing): {value}")
    if y < 160:
        c.showPage()
        y = 720
    try:
        image = ImageReader(str(path))
        iw, ih = image.getSize()
        max_width = 6.0 * 72
        scale = min(max_width / iw, 1.0)
        width = iw * scale
        height = ih * scale
        c.drawImage(image, 72, y - height, width=width, height=height)
        return y - height - 12
    except Exception:
        return _draw_line(c, y, f"- image (unreadable): {value}")


def _draw_math(c, y: float, expression: str) -> float:
    if not expression:
        return _draw_line(c, y, "- math: ")
    if y < 160:
        c.showPage()
        y = 720
    try:
        drawing = _math_to_drawing(expression)
        if drawing is None:
            return _draw_line(c, y, f"- math: {expression}")
        max_width = 6.0 * 72
        scale = min(max_width / drawing.width, 1.0)
        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)
        renderPDF.draw(drawing, c, 72, y - drawing.height)
        return y - drawing.height - 12
    except Exception:
        return _draw_line(c, y, f"- math: {expression}")


def _add_link(c, y: float, url: str) -> float:
    if not url:
        return y
    c.linkURL(url, (72, y - 2, 540, y + 10), relative=0)
    return y - 12


def _math_to_drawing(expression: str):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    text = fig.text(0, 0, f"${expression}$", fontsize=12)
    fig.canvas.draw()
    bbox = text.get_window_extent()
    width, height = bbox.size
    fig.set_size_inches(width / fig.dpi, height / fig.dpi)
    fig.canvas.draw()

    buffer = BytesIO()
    fig.savefig(buffer, format="svg", transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buffer.seek(0)
    drawing = svg2rlg(buffer)
    return drawing
