from __future__ import annotations

from xml.etree.ElementTree import Element, SubElement, tostring

from quizmark.models import MediaReference, QuizData


def export_moodle_xml(quiz: QuizData) -> str:
    root = Element("quiz")
    for question in quiz.questions:
        q_el = SubElement(root, "question", {"type": "multichoice"})
        name_el = SubElement(q_el, "name")
        SubElement(name_el, "text").text = question.text

        questiontext_el = SubElement(q_el, "questiontext", {"format": "html"})
        question_media = _combined_media(question.media, question.image)
        question_html = _html_text(question.text, question_media)
        SubElement(questiontext_el, "text").text = question_html

        single = SubElement(q_el, "single")
        single.text = "true"
        shuffle = SubElement(q_el, "shuffleanswers")
        shuffle.text = "true"

        for answer in question.answers:
            fraction = "100" if answer.correct else "0"
            answer_el = SubElement(q_el, "answer", {"fraction": fraction, "format": "html"})
            answer_media = _combined_media(answer.media, answer.image)
            answer_html = _html_text(answer.text, answer_media)
            SubElement(answer_el, "text").text = answer_html
            feedback = SubElement(answer_el, "feedback", {"format": "html"})
            SubElement(feedback, "text").text = ""

        if question.points is not None:
            defaultgrade = SubElement(q_el, "defaultgrade")
            defaultgrade.text = str(question.points)

    xml_bytes = tostring(root, encoding="utf-8")
    return xml_bytes.decode("utf-8")


def _html_text(text: str | None, media_list) -> str:
    parts = [text or ""]
    for media in media_list or []:
        parts.append(_media_html(media))
    joined = "<br>".join(p for p in parts if p)
    return f"<![CDATA[{joined}]]>"


def _media_html(media) -> str:
    if media.kind == "image":
        return f"<img src=\"{media.value}\">"
    if media.kind == "audio":
        return f"<audio controls src=\"{media.value}\"></audio>"
    if media.kind == "video":
        return f"<video controls src=\"{media.value}\"></video>"
    if media.kind == "attachment":
        return f"<a href=\"{media.value}\">Attachment</a>"
    if media.kind == "math":
        return f"\\({media.value}\\)"
    return ""


def _combined_media(media_list, image) -> list[MediaReference]:
    items = list(media_list)
    if image and not any(m.kind == "image" and m.value == image.path for m in items):
        items.append(MediaReference(kind="image", value=image.path, line=image.line))
    return items
