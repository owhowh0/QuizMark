from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

from quizmark.models import Answer, MediaReference, Question, QuizData


def _is_external_reference(value: str) -> bool:
    lowered = value.lower()
    return lowered.startswith("http://") or lowered.startswith("https://") or lowered.startswith("data:")


def _resolve_media_path(value: str, base_dir: Path) -> Path | None:
    if _is_external_reference(value):
        return None
    raw = value.strip().strip('"').strip("'")
    if not raw:
        return None
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve() if candidate.is_file() else None
    resolved = (base_dir / raw).resolve()
    if resolved.is_file():
        return resolved
    return None


def _collect_media_paths(quiz: QuizData, base_dir: Path) -> dict[str, Path]:
    """Map archive-relative paths to local files referenced by the quiz."""
    found: dict[str, Path] = {}

    def add(value: str) -> None:
        resolved = _resolve_media_path(value, base_dir)
        if resolved is None:
            return
        rel = value.strip().strip('"').strip("'").replace("\\", "/")
        found.setdefault(rel, resolved)

    def add_media_list(media_list: list[MediaReference]) -> None:
        for media in media_list:
            if media.kind in {"image", "audio", "video", "attachment"}:
                add(media.value)

    add_media_list(quiz.media)
    for question in quiz.questions:
        add_media_list(question.media)
        if question.image:
            add(question.image.path)
        for answer in question.answers:
            add_media_list(answer.media)
            if answer.image:
                add(answer.image.path)

    return found


def export_moodle_zip(quiz: QuizData, source_path: Path | str) -> bytes:
    """Create a zip archive containing the .qm file and referenced media files."""
    source_path = Path(source_path).resolve()
    base_dir = source_path.parent
    media_paths = _collect_media_paths(quiz, base_dir)

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(source_path, arcname=source_path.name)
        for rel_path, abs_path in sorted(media_paths.items()):
            archive.write(abs_path, arcname=rel_path)
    return buffer.getvalue()
