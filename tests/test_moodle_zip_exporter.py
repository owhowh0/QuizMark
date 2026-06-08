import zipfile
from io import BytesIO
from pathlib import Path

from quizmark.exporters import export_moodle_zip
from quizmark.parser import QuizMarkParser


def test_moodle_zip_includes_referenced_media(tmp_path):
    image = tmp_path / "images" / "board.png"
    image.parent.mkdir()
    image.write_bytes(b"png")

    qm = tmp_path / "quiz.qm"
    qm.write_text(
        """
QUIZ: Sample
QUESTION: What is shown?
IMAGE: "images/board.png"
AUDIO: "audio/clip.mp3"
VIDEO: "video/tour.mp4"

A: One
B: Two *
""".strip(),
        encoding="utf-8",
    )

    audio = tmp_path / "audio" / "clip.mp3"
    audio.parent.mkdir()
    audio.write_bytes(b"mp3")

    video = tmp_path / "video" / "tour.mp4"
    video.parent.mkdir()
    video.write_bytes(b"mp4")

    quiz = QuizMarkParser().parse_text(qm.read_text(encoding="utf-8"), source=str(qm))
    archive_bytes = export_moodle_zip(quiz, qm)

    with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
        names = set(archive.namelist())

    assert "quiz.qm" in names
    assert "images/board.png" in names
    assert "audio/clip.mp3" in names
    assert "video/tour.mp4" in names


def test_moodle_zip_skips_external_urls(tmp_path):
    qm = tmp_path / "quiz.qm"
    qm.write_text(
        """
QUIZ: Sample
QUESTION: Remote media
IMAGE: "https://example.com/picture.jpg"

A: Yes *
B: No
""".strip(),
        encoding="utf-8",
    )

    quiz = QuizMarkParser().parse_text(qm.read_text(encoding="utf-8"), source=str(qm))
    archive_bytes = export_moodle_zip(quiz, qm)

    with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
        names = set(archive.namelist())

    assert names == {"quiz.qm"}
