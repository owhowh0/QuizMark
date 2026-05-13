"""
QuizMark GUI — PyQt6 editor, validator, media-aware previewer, and exporter for .qm files.

Final GUI patch: local image preview fixes, stronger Validate/Lint, safer toolbar actions, and economic classroom design.

Put this file either in the QuizMark project root or in a sibling/front-end folder.
It searches upward for the quizmark package, so PyCharm can run it from Front/Interface.py.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any

# ── PyQt6 ─────────────────────────────────────────────────────────────────
from PyQt6.QtCore import QModelIndex, QObject, QDir, QSize, Qt, QThread, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFileSystemModel,  # PyQt6 / Qt6: QFileSystemModel is in QtGui, not QtWidgets.
    QFont,
    QFontMetrics,
    QKeySequence,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except ImportError:  # Optional dependency: pip install PyQt6-WebEngine
    QWebEngineView = None


# ── QuizMark project discovery ────────────────────────────────────────────
def _find_project_root(start: Path) -> Path:
    """Find the folder that contains the quizmark package.

    Supports both layouts:
      project/quizmark/...
      project/Front/Interface.py + project/QuizMark-main/quizmark/...
    """
    start = start.resolve()
    for folder in (start, *start.parents):
        if (folder / "quizmark").is_dir():
            return folder
        nested = folder / "QuizMark-main"
        if (nested / "quizmark").is_dir():
            return nested
    return start


_HERE = Path(__file__).resolve().parent
PROJECT_ROOT = _find_project_root(_HERE)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

_IMPORT_ERR = ""
try:
    from quizmark.parser.errors import ParserError, ValidationError
    from quizmark.parser.parser import QuizMarkParser
    from quizmark.validators.validator import validate_quiz

    _QUIZMARK_OK = True
except ImportError as exc:
    ParserError = ValidationError = Exception  # type: ignore[assignment]
    QuizMarkParser = None  # type: ignore[assignment]
    validate_quiz = None  # type: ignore[assignment]
    _QUIZMARK_OK = False
    _IMPORT_ERR = str(exc)


# ══════════════════════════════════════════════════════════════════════════
#  Colour palette
# ══════════════════════════════════════════════════════════════════════════
# Professional/economic palette: dark market-blue, economy green, and muted gold.
DARK = "#0f172a"       # editor background
SURFACE = "#162033"    # secondary surfaces
PANEL = "#111827"      # menus / docks / toolbar
BORDER = "#2f3b52"     # separators
FG = "#eef2e6"         # main text
FG_DIM = "#94a3b8"     # secondary text
ACCENT = "#d6a43a"     # gold accent
GREEN = "#70b77e"      # success / economy green
RED = "#ef8181"        # errors
YELLOW = "#f4c95d"     # warnings
PURPLE = "#7cc4b2"     # hover / alternate accent
TEAL = "#8fc6a0"       # lint/info


# ══════════════════════════════════════════════════════════════════════════
#  Export helper
# ══════════════════════════════════════════════════════════════════════════
def export_quiz_data(quiz_data: Any, format_name: str) -> str | bytes | dict[str, str]:
    """Export QuizData without importing every exporter up front."""
    fmt = format_name.lower()
    if fmt == "html":
        from quizmark.exporters.html_exporter import export_html

        return export_html(quiz_data)
    if fmt == "json":
        from quizmark.exporters.json_exporter import export_json

        return export_json(quiz_data)
    if fmt == "markdown":
        from quizmark.exporters.markdown_exporter import export_markdown

        return export_markdown(quiz_data)
    if fmt == "text":
        from quizmark.exporters.text_exporter import export_text

        return export_text(quiz_data)
    if fmt == "moodle":
        from quizmark.exporters.moodle_exporter import export_moodle_xml

        return export_moodle_xml(quiz_data)
    if fmt == "web":
        from quizmark.exporters.web_exporter import export_web_package

        return export_web_package(quiz_data)
    if fmt == "docx":
        from quizmark.exporters.docx_exporter import export_docx

        return export_docx(quiz_data)
    if fmt == "pdf":
        from quizmark.exporters.pdf_exporter import export_pdf

        return export_pdf(quiz_data)
    raise ValueError(f"Unknown export format: {format_name}")


# ══════════════════════════════════════════════════════════════════════════
#  Preview / media-path helpers
# ══════════════════════════════════════════════════════════════════════════
_URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")
_LOCAL_MEDIA_KINDS = {"image", "audio", "video", "attachment"}


def _is_external_media_reference(value: str) -> bool:
    """True for remote/special references that should not be resolved locally."""
    value = value.strip()
    if not value or value.startswith("#"):
        return True
    if _WINDOWS_DRIVE_RE.match(value):
        return False
    return bool(_URL_SCHEME_RE.match(value)) or value.startswith("//")


def _base_dir_for_source(source_path: Path | None) -> Path:
    if source_path is not None:
        return source_path.resolve().parent
    return PROJECT_ROOT.resolve()


def _candidate_media_paths(value: str, source_path: Path | None) -> list[Path]:
    """Possible local filesystem locations for a media path."""
    raw = html.unescape(value).strip().strip('"').strip("'")
    if not raw or _is_external_media_reference(raw):
        return []

    # Browser references may include fragments/query strings; strip them for filesystem checks.
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw:
        return []

    path = Path(raw).expanduser()
    if path.is_absolute():
        return [path]

    bases = [_base_dir_for_source(source_path), PROJECT_ROOT.resolve()]
    candidates: list[Path] = []
    seen: set[str] = set()
    for base_dir in bases:
        candidate = base_dir / raw
        key = str(candidate).lower()
        if key not in seen:
            candidates.append(candidate)
            seen.add(key)
    return candidates


def _resolve_existing_media_path(value: str, source_path: Path | None) -> Path | None:
    for candidate in _candidate_media_paths(value, source_path):
        if candidate.exists():
            return candidate.resolve()
    return None


def _media_path_hint(value: str, source_path: Path | None) -> str:
    candidates = _candidate_media_paths(value, source_path)
    if not candidates:
        return value
    return ", ".join(str(path) for path in candidates[:2])


def _collect_media_refs(quiz_data: Any) -> list[tuple[str, str, int | None, str]]:
    """Collect media refs as (kind, value, line, scope)."""
    refs: list[tuple[str, str, int | None, str]] = []

    def add(kind: str, value: str, line: int | None, scope: str) -> None:
        refs.append((kind, value, line, scope))

    for media in getattr(quiz_data, "media", []) or []:
        add(getattr(media, "kind", ""), getattr(media, "value", ""), getattr(media, "line", None), "quiz")

    for q_index, question in enumerate(getattr(quiz_data, "questions", []) or [], start=1):
        question_media = list(getattr(question, "media", []) or [])
        question_image = getattr(question, "image", None)
        if question_image is not None and not any(
            getattr(m, "kind", "") == "image" and getattr(m, "value", "") == getattr(question_image, "path", "")
            for m in question_media
        ):
            add("image", getattr(question_image, "path", ""), getattr(question_image, "line", None), f"question {q_index}")
        for media in question_media:
            add(getattr(media, "kind", ""), getattr(media, "value", ""), getattr(media, "line", None), f"question {q_index}")

        for answer in getattr(question, "answers", []) or []:
            label = getattr(answer, "label", "?")
            answer_media = list(getattr(answer, "media", []) or [])
            answer_image = getattr(answer, "image", None)
            if answer_image is not None and not any(
                getattr(m, "kind", "") == "image" and getattr(m, "value", "") == getattr(answer_image, "path", "")
                for m in answer_media
            ):
                add("image", getattr(answer_image, "path", ""), getattr(answer_image, "line", None), f"question {q_index}, answer {label}")
            for media in answer_media:
                add(getattr(media, "kind", ""), getattr(media, "value", ""), getattr(media, "line", None), f"question {q_index}, answer {label}")

    return refs


def media_path_warnings(quiz_data: Any, source_path: Path | None) -> list[str]:
    """Return non-blocking warnings for missing local image/audio/video/attachment files."""
    warnings: list[str] = []
    for kind, value, line, scope in _collect_media_refs(quiz_data):
        if kind not in _LOCAL_MEDIA_KINDS or not str(value).strip():
            continue
        if _is_external_media_reference(str(value)):
            continue
        resolved = _resolve_existing_media_path(str(value), source_path)
        if resolved is not None:
            continue
        line_text = f"line {line}: " if line else ""
        warnings.append(
            f"Warning: {line_text}{kind.capitalize()} file not found for {scope}: {value}. "
            f"Looked for {_media_path_hint(str(value), source_path)}."
        )
    return warnings


def line_number_from_message(message: str) -> int | None:
    line_matches = re.findall(r"\bline\s+(\d+)\b", message, flags=re.IGNORECASE)
    if line_matches:
        return int(line_matches[-1])
    source_matches = re.findall(r":(\d+):", message)
    if source_matches:
        return int(source_matches[-1])
    return None


def _file_uri_for_media(value: str, source_path: Path | None) -> str | None:
    resolved = _resolve_existing_media_path(value, source_path)
    if resolved is None:
        return None
    return QUrl.fromLocalFile(str(resolved)).toString()


def _theme_style_css(theme: Any, selector: str) -> str:
    """Convert QuizMark theme selector attributes into CSS for the preview only."""
    if not theme:
        return ""
    style = getattr(theme, "styles", {}).get(selector, {}) or {}
    parts: list[str] = []
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


def _optional_css_rule(selector: str, declaration: str) -> str:
    if not declaration:
        return ""
    return f"{selector} {{ {declaration}; }}\n"


def build_preview_html(quiz_data: Any, source_path: Path | None) -> str:
    """Render preview HTML and convert local media paths into file URLs for Qt."""
    content = str(export_quiz_data(quiz_data, "html"))

    theme = getattr(quiz_data, "theme", None)
    properties = getattr(theme, "properties", {}) if theme else {}
    accent = str(properties.get("accent", "#2e7d32"))
    radius = str(properties.get("radius", "10px"))
    answer_css = _theme_style_css(theme, "answer")
    wrong_css = _theme_style_css(theme, "wrong")

    extra_css = f"""
:root {{ --qm-accent: {accent}; --qm-radius: {radius}; }}
* {{ box-sizing: border-box; }}
body {{ line-height: 1.45; }}
h1 {{ color: var(--qm-accent); border-bottom: 3px solid var(--qm-accent); padding-bottom: .35rem; }}
.qm-question {{
  border-left: 4px solid var(--qm-accent);
  background: rgba(46, 125, 50, .06);
  padding: 1rem;
  margin: 1rem 0;
  border-radius: var(--qm-radius);
}}
.qm-answers li {{
  border: 1px solid rgba(31, 45, 42, .12);
  border-radius: calc(var(--qm-radius) / 1.5);
  padding: .55rem .75rem;
  margin: .45rem 0;
  background: rgba(255, 255, 255, .55);
}}
.qm-correct {{ border-color: var(--qm-accent) !important; background: rgba(46, 125, 50, .12) !important; }}
.qm-media img {{ display: block; max-height: 340px; object-fit: contain; box-shadow: 0 8px 24px rgba(0,0,0,.12); }}
.qm-missing-media {{
  border: 1px dashed #b45309;
  background: #fff7ed;
  color: #7c2d12;
  padding: .75rem;
  border-radius: .5rem;
  margin: .5rem 0;
  font-family: system-ui, sans-serif;
}}
.qm-missing-media code {{ color: #7c2d12; }}
{_optional_css_rule('.qm-answer', answer_css)}{_optional_css_rule('.qm-answer:not(.qm-correct)', wrong_css)}
"""
    if "</style>" in content:
        content = content.replace("</style>", extra_css + "</style>", 1)

    def replace_img(match: re.Match[str]) -> str:
        prefix, quote, url, suffix = match.group(1), match.group(2), match.group(3), match.group(4)
        if _is_external_media_reference(url):
            return match.group(0)
        file_uri = _file_uri_for_media(url, source_path)
        if file_uri:
            return f"{prefix}{quote}{html.escape(file_uri, quote=True)}{quote}{suffix}"
        escaped_url = html.escape(url)
        escaped_hint = html.escape(_media_path_hint(url, source_path))
        return (
            '<div class="qm-media qm-missing-media">'
            '<strong>Image file not found</strong><br>'
            f'<code>{escaped_url}</code><br>'
            f'<small>Looked for: {escaped_hint}</small>'
            '</div>'
        )

    content = re.sub(
        r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])(.*?)(?:\2)([^>]*>)',
        replace_img,
        content,
        flags=re.IGNORECASE,
    )

    def replace_src_href(match: re.Match[str]) -> str:
        attr, quote, url = match.group(1), match.group(2), match.group(3)
        if _is_external_media_reference(url):
            return match.group(0)
        file_uri = _file_uri_for_media(url, source_path)
        if file_uri:
            return f'{attr}={quote}{html.escape(file_uri, quote=True)}{quote}'
        return match.group(0)

    return re.sub(
        r'\b(src|href)\s*=\s*(["\'])(.*?)(?:\2)',
        replace_src_href,
        content,
        flags=re.IGNORECASE,
    )


# ══════════════════════════════════════════════════════════════════════════
#  Syntax highlighter
# ══════════════════════════════════════════════════════════════════════════
class QmHighlighter(QSyntaxHighlighter):
    """Highlight .qm / QuizMark syntax."""

    def __init__(self, doc: QTextDocument):
        super().__init__(doc)

        def fmt(color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
            char_format = QTextCharFormat()
            char_format.setForeground(QColor(color))
            if bold:
                char_format.setFontWeight(700)
            if italic:
                char_format.setFontItalic(True)
            return char_format

        flags = re.IGNORECASE
        self._rules: list[tuple[re.Pattern[str], QTextCharFormat]] = [
            (re.compile(r"(#|//).*$"), fmt(FG_DIM, italic=True)),
            (re.compile(r"\bQUIZ\s*:", flags), fmt(PURPLE, bold=True)),
            (re.compile(r"\bQUESTION\b", flags), fmt(ACCENT, bold=True)),
            (re.compile(r"\bTHEME\b", flags), fmt(TEAL, bold=True)),
            (re.compile(r"\b(IMAGE|AUDIO|VIDEO|ATTACH|MATH)\s*:", flags), fmt(YELLOW, bold=True)),
            (re.compile(r"\b([A-Z_]{2,})\s*:"), fmt(FG, bold=True)),
            (re.compile(r"\*\s*$"), fmt(GREEN, bold=True)),
            (re.compile(r"^[A-Z]\s*:", flags), fmt(ACCENT, bold=True)),
            (re.compile(r'"[^"]*"'), fmt(GREEN)),
            (re.compile(r"\b\d+(\.\d+)?%?\b"), fmt(YELLOW)),
            (re.compile(r"\b(true|false)\b", flags), fmt(PURPLE)),
            (re.compile(r"[{}]"), fmt(TEAL, bold=True)),
            (re.compile(r"\bpoints="), fmt(FG_DIM)),
        ]

    def highlightBlock(self, text: str) -> None:
        for pattern, char_format in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), char_format)


# ══════════════════════════════════════════════════════════════════════════
#  Editor widget
# ══════════════════════════════════════════════════════════════════════════
class Editor(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_font()
        self._highlighter = QmHighlighter(self.document())
        self.setTabStopDistance(QFontMetrics(self.font()).horizontalAdvance(" ") * 4)
        self.setPlaceholderText("QUIZ: My Quiz\nQUESTION: Your question?\nA: Answer one\nB: Answer two *")
        self._apply_style()

    def _setup_font(self) -> None:
        font = QFont()
        for name in ["JetBrains Mono", "Fira Code", "Cascadia Code", "Source Code Pro", "Consolas", "Courier New"]:
            font.setFamily(name)
            if QFont(name).exactMatch():
                break
        font.setPointSize(12)
        self.setFont(font)

    def _apply_style(self) -> None:
        self.setStyleSheet(
            f"""
            QPlainTextEdit {{
                background-color: {DARK};
                color: {FG};
                border: none;
                padding: 8px;
                selection-background-color: {ACCENT}55;
            }}
            """
        )

    def line_col(self) -> tuple[int, int]:
        cursor = self.textCursor()
        return cursor.blockNumber() + 1, cursor.columnNumber() + 1


# ══════════════════════════════════════════════════════════════════════════
#  Preview widget
# ══════════════════════════════════════════════════════════════════════════
class PreviewWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        if QWebEngineView is not None:
            self._view: QWebEngineView | QTextEdit = QWebEngineView(self)
        else:
            text = QTextEdit(self)
            text.setReadOnly(True)
            text.setStyleSheet(
                f"""
                QTextEdit {{
                    background: {SURFACE};
                    color: {FG};
                    border: none;
                    font-family: Georgia, serif;
                    font-size: 13px;
                    padding: 12px;
                }}
                """
            )
            text.setHtml("<p>Preview will appear here after parsing.</p>")
            self._view = text
        layout.addWidget(self._view)

    def show_html(self, content: str, base_dir: Path | None = None) -> None:
        if base_dir is not None:
            base_url = QUrl.fromLocalFile(str(base_dir.resolve()) + "/")
            if QWebEngineView is not None and isinstance(self._view, QWebEngineView):
                self._view.setHtml(content, base_url)
                return
            self._view.document().setBaseUrl(base_url)
        self._view.setHtml(content)

    def show_text(self, text: str) -> None:
        escaped = html.escape(text)
        self._view.setHtml(
            f"<pre style='font-family:monospace;color:{FG};background:{DARK};padding:12px;white-space:pre-wrap'>"
            f"{escaped}</pre>"
        )

    def show_error(self, msg: str) -> None:
        escaped = html.escape(msg).replace("\n", "<br>")
        self._view.setHtml(
            f"<div style='color:{RED};font-family:monospace;padding:12px'>"
            f"<b>⚠ Error</b><br>{escaped}</div>"
        )


# ══════════════════════════════════════════════════════════════════════════
#  Background parse worker
# ══════════════════════════════════════════════════════════════════════════
class ParseWorker(QObject):
    done = pyqtSignal(object, list)
    finished = pyqtSignal()

    def __init__(self, text: str, source: str | None = None):
        super().__init__()
        self._text = text
        self._source = source

    def run(self) -> None:
        if not _QUIZMARK_OK or QuizMarkParser is None or validate_quiz is None:
            self.done.emit(None, [f"QuizMark not importable: {_IMPORT_ERR}"])
            self.finished.emit()
            return

        quiz_data = None
        errors: list[str] = []
        try:
            parser = QuizMarkParser()
            quiz_data = parser.parse_text(self._text, source=self._source)
            errors = [str(e) for e in validate_quiz(quiz_data)]
        except (ParserError, ValidationError) as exc:
            errors = [str(exc)]
        except Exception as exc:
            errors = [f"Unexpected error: {exc}"]

        self.done.emit(quiz_data, errors)
        self.finished.emit()


# ══════════════════════════════════════════════════════════════════════════
#  Editor tab
# ══════════════════════════════════════════════════════════════════════════
class EditorTab(QWidget):
    parse_errors_changed = pyqtSignal(list)
    modified_changed = pyqtSignal()
    path_changed = pyqtSignal()

    def __init__(self, path: Path | None = None, parent: QWidget | None = None):
        super().__init__(parent)
        self.path = path
        self._modified = False
        self._quiz_data: Any = None
        self._errors: list[str] = []
        self._parse_thread: QThread | None = None
        self._parse_worker: ParseWorker | None = None
        self._parse_again_requested = False

        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(500)
        self._debounce.timeout.connect(self._trigger_parse)

        self._setup_ui()

        if path and path.exists():
            self.editor.setPlainText(path.read_text(encoding="utf-8"))
            self.editor.document().setModified(False)
            self._modified = False

        self.editor.textChanged.connect(self._on_text_changed)
        QTimer.singleShot(0, self._trigger_parse)

    @property
    def is_modified(self) -> bool:
        return self._modified

    @property
    def errors(self) -> list[str]:
        return list(self._errors)

    @property
    def display_name(self) -> str:
        return self.path.name if self.path else "untitled.qm"

    def text(self) -> str:
        return self.editor.toPlainText()

    def set_text(self, text: str, modified: bool = True) -> None:
        self.editor.setPlainText(text)
        self.editor.document().setModified(modified)
        self._modified = modified
        self.modified_changed.emit()
        self._debounce.start()

    def save(self) -> bool:
        if not self.path:
            return self.save_as()
        try:
            self.path.write_text(self.text(), encoding="utf-8")
        except OSError as exc:
            QMessageBox.warning(self, "Save failed", str(exc))
            return False
        self.editor.document().setModified(False)
        self._modified = False
        self.modified_changed.emit()
        return True

    def save_as(self) -> bool:
        start = str(self.path or PROJECT_ROOT / "untitled.qm")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QuizMark File",
            start,
            "QuizMark Files (*.qm);;All Files (*)",
        )
        if not file_path:
            return False
        self.path = Path(file_path)
        saved = self.save()
        if saved:
            self.path_changed.emit()
        return saved

    def base_dir(self) -> Path:
        if self.path:
            return self.path.resolve().parent
        return PROJECT_ROOT

    def quiz_data(self) -> Any:
        return self._quiz_data

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        toolbar = QWidget()
        toolbar.setFixedHeight(34)
        toolbar.setStyleSheet(f"background:{PANEL};border-bottom:1px solid {BORDER};")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(6, 0, 6, 0)

        preview_label = QLabel("Preview:")
        preview_label.setStyleSheet(f"color:{FG_DIM};font-size:11px")
        toolbar_layout.addWidget(preview_label)

        self._preview_mode = QComboBox()
        self._preview_mode.addItems(["HTML Preview", "Plain Text Preview", "JSON Preview"])
        self._preview_mode.setStyleSheet(self._combo_style())
        self._preview_mode.currentIndexChanged.connect(self._refresh_preview)
        toolbar_layout.addWidget(self._preview_mode)
        toolbar_layout.addStretch()

        self._parse_indicator = QLabel("●")
        self._parse_indicator.setStyleSheet(f"color:{FG_DIM};font-size:14px")
        toolbar_layout.addWidget(self._parse_indicator)

        root.addWidget(toolbar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.editor = Editor()
        self.preview = PreviewWidget()
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([650, 450])
        splitter.setStyleSheet(f"QSplitter::handle {{ background:{BORDER}; width:2px; }}")
        root.addWidget(splitter)

    def _combo_style(self) -> str:
        return f"""
            QComboBox {{
                background:{SURFACE};color:{FG};border:1px solid {BORDER};
                padding:2px 6px;border-radius:3px;font-size:11px;min-width:130px;
            }}
            QComboBox QAbstractItemView {{
                background:{SURFACE};color:{FG};border:1px solid {BORDER};
            }}
        """

    def _on_text_changed(self) -> None:
        self._modified = True
        self.modified_changed.emit()
        self._parse_indicator.setStyleSheet(f"color:{YELLOW};font-size:14px")
        self._parse_indicator.setToolTip("Parsing soon…")
        self._debounce.start()

    def _trigger_parse(self) -> None:
        if self._parse_thread and self._parse_thread.isRunning():
            self._parse_again_requested = True
            return

        source = str(self.path) if self.path else "untitled"
        worker = ParseWorker(self.text(), source)
        thread = QThread(self)
        self._parse_worker = worker
        self._parse_thread = thread
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.done.connect(self._on_parse_done)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._on_parse_thread_finished)
        thread.start()

    def _on_parse_thread_finished(self) -> None:
        self._parse_thread = None
        self._parse_worker = None
        if self._parse_again_requested:
            self._parse_again_requested = False
            self._debounce.start(50)

    def _on_parse_done(self, quiz_data: Any, errors: list[str]) -> None:
        warnings = media_path_warnings(quiz_data, self.path) if quiz_data is not None and not errors else []
        self._quiz_data = quiz_data
        self._errors = errors + warnings
        self.parse_errors_changed.emit(self._errors)

        if errors:
            self._parse_indicator.setStyleSheet(f"color:{RED};font-size:14px")
            self._parse_indicator.setToolTip("\n".join(errors))
            self.preview.show_error("\n".join(errors))
            return

        if warnings:
            self._parse_indicator.setStyleSheet(f"color:{YELLOW};font-size:14px")
            self._parse_indicator.setToolTip("\n".join(warnings))
        else:
            self._parse_indicator.setStyleSheet(f"color:{GREEN};font-size:14px")
            self._parse_indicator.setToolTip("No errors")
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        if self._quiz_data is None:
            return
        try:
            mode = self._preview_mode.currentIndex()
            if mode == 0:
                self.preview.show_html(build_preview_html(self._quiz_data, self.path), self.base_dir())
            elif mode == 1:
                self.preview.show_text(str(export_quiz_data(self._quiz_data, "text")))
            else:
                self.preview.show_text(str(export_quiz_data(self._quiz_data, "json")))
        except Exception as exc:
            self.preview.show_error(str(exc))


# ══════════════════════════════════════════════════════════════════════════
#  Problems panel
# ══════════════════════════════════════════════════════════════════════════
class ProblemsPanel(QWidget):
    line_requested = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self._list = QListWidget()
        self._list.setStyleSheet(
            f"""
            QListWidget {{
                background:{PANEL};color:{FG};border:none;font-size:12px;
            }}
            QListWidget::item:selected {{background:{ACCENT}33;}}
            """
        )
        self._list.itemDoubleClicked.connect(self._open_problem_line)
        layout.addWidget(self._list)

    def set_errors(self, errors: list[str]) -> None:
        self._list.clear()
        if not errors:
            item = QListWidgetItem("✓  No problems detected")
            item.setForeground(QColor(GREEN))
            self._list.addItem(item)
            return
        for message in errors:
            is_warning = str(message).lower().startswith("warning:")
            prefix = "⚠" if is_warning else "✗"
            item = QListWidgetItem(f"{prefix}  {message}")
            item.setForeground(QColor(YELLOW if is_warning else RED))
            line_no = line_number_from_message(str(message))
            item.setData(Qt.ItemDataRole.UserRole, line_no or 0)
            if line_no:
                item.setToolTip(f"Double-click to jump to line {line_no}")
            self._list.addItem(item)

    def _open_problem_line(self, item: QListWidgetItem) -> None:
        line_no = int(item.data(Qt.ItemDataRole.UserRole) or 0)
        if line_no > 0:
            self.line_requested.emit(line_no)


# ══════════════════════════════════════════════════════════════════════════
#  Export dialog
# ══════════════════════════════════════════════════════════════════════════
class ExportDialog(QDialog):
    FORMATS = ["html", "json", "markdown", "text", "moodle", "web", "docx", "pdf"]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Export Quiz")
        self.setMinimumWidth(430)
        self.setStyleSheet(
            f"""
            QDialog {{ background:{SURFACE}; color:{FG}; }}
            QLabel  {{ color:{FG}; }}
            QComboBox, QLineEdit {{
                background:{DARK};color:{FG};border:1px solid {BORDER};
                padding:4px 8px;border-radius:4px;
            }}
            QPushButton {{
                background:{ACCENT};color:{DARK};border:none;
                padding:6px 16px;border-radius:4px;font-weight:bold;
            }}
            QPushButton:hover {{ background:{PURPLE}; }}
            """
        )

        form = QFormLayout(self)
        self.fmt = QComboBox()
        self.fmt.addItems(self.FORMATS)
        self.out_path = QLineEdit()
        self.out_path.setPlaceholderText("Leave blank to display text exports in the output panel")
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._browse)

        row = QHBoxLayout()
        row.addWidget(self.out_path)
        row.addWidget(browse)
        form.addRow("Format:", self.fmt)
        form.addRow("Output:", row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _browse(self) -> None:
        fmt = self.fmt.currentText()
        if fmt == "web":
            directory = QFileDialog.getExistingDirectory(self, "Choose Web Export Folder", str(PROJECT_ROOT))
            if directory:
                self.out_path.setText(directory)
            return

        ext_map = {
            "html": "*.html",
            "json": "*.json",
            "markdown": "*.md",
            "text": "*.txt",
            "moodle": "*.xml",
            "docx": "*.docx",
            "pdf": "*.pdf",
        }
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export To",
            str(PROJECT_ROOT),
            f"{fmt.upper()} Files ({ext_map.get(fmt, '*.*')});;All Files (*)",
        )
        if file_path:
            self.out_path.setText(file_path)

    def values(self) -> tuple[str, str]:
        return self.fmt.currentText(), self.out_path.text().strip()


# ══════════════════════════════════════════════════════════════════════════
#  New-file wizard dialog
# ══════════════════════════════════════════════════════════════════════════
_BASIC_TEMPLATE = """QUIZ: {title}

# Metadata (optional)
TIME_LIMIT: 60
PASS_MARK: 70%
SHUFFLE: false

QUESTION: {question}
A: First option
B: Second option *
C: Third option
"""

_ECONOMIC_THEME_SNIPPET = """THEME {
    background = "#f7f4ea"
    foreground = "#1f2d2a"
    accent = "#2e7d32"
    font = "Arial"
    spacing = "2rem"
    radius = "8px"

    question [font="Arial", size=17, color="#1f2d2a", weight="bold"]
    answer [font="Arial", size=14, color="#2c3e36"]
    correct [color="#1b5e20", weight="bold"]
    wrong [color="#8b1e1e"]
}
"""

_ECONOMIC_TEMPLATE = """QUIZ: {title}

# Economic classroom theme: green/gold, clear contrast, low visual noise.
{theme}
TIME_LIMIT: 60
PASS_MARK: 70%
SHUFFLE: false

QUESTION: {question}
A: Budget
B: Opportunity cost *
C: Inflation
"""

_IMAGE_QUESTION_SNIPPET = """QUESTION: Name this structure
IMAGE: images/example.jpg
A: First choice
B: Second choice *
C: Third choice
"""



class NewFileDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("New QuizMark File")
        self.setMinimumWidth(360)
        self.setStyleSheet(
            f"""
            QDialog {{ background:{SURFACE};color:{FG}; }}
            QLabel  {{ color:{FG}; }}
            QLineEdit, QComboBox {{
                background:{DARK};color:{FG};border:1px solid {BORDER};
                padding:4px 8px;border-radius:4px;
            }}
            QComboBox QAbstractItemView {{
                background:{DARK};color:{FG};border:1px solid {BORDER};
            }}
            QPushButton {{
                background:{ACCENT};color:{DARK};border:none;
                padding:6px 16px;border-radius:4px;font-weight:bold;
            }}
            """
        )
        form = QFormLayout(self)
        self.title = QLineEdit("My Quiz")
        self.first_q = QLineEdit("What is opportunity cost?")
        self.preset = QComboBox()
        self.preset.addItems(["Simple quiz", "Economic theme quiz"])
        form.addRow("Quiz Title:", self.title)
        form.addRow("First Question:", self.first_q)
        form.addRow("Template:", self.preset)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def template(self) -> str:
        title = self.title.text().strip() or "My Quiz"
        question = self.first_q.text().strip() or "Sample question?"
        if self.preset.currentIndex() == 1:
            return _ECONOMIC_TEMPLATE.format(title=title, question=question, theme=_ECONOMIC_THEME_SNIPPET)
        return _BASIC_TEMPLATE.format(title=title, question=question)


# ══════════════════════════════════════════════════════════════════════════
#  Main window
# ══════════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuizMark Studio — Economics Edition")
        self.resize(1280, 800)
        self._apply_dark_theme()
        self._build_ui()
        self._build_menu()
        self._build_toolbar()
        self._update_title()

        if not _QUIZMARK_OK:
            self._output(
                "⚠  QuizMark package could not be imported.\n"
                f"Import error: {_IMPORT_ERR}\n\n"
                f"Detected project root: {PROJECT_ROOT}\n"
                "In PyCharm, run this file with the repository folder as a Sources Root, "
                "or keep Interface.py inside / next to the repository.",
                warn=True,
            )

    # ── Theme ──────────────────────────────────────────────────────────────
    def _apply_dark_theme(self) -> None:
        self.setStyleSheet(
            f"""
            QMainWindow {{ background:{DARK}; }}
            QMenuBar {{
                background:{PANEL};color:{FG};border-bottom:1px solid {BORDER};
            }}
            QMenuBar::item:selected {{ background:{ACCENT}33; }}
            QMenu {{
                background:{SURFACE};color:{FG};border:1px solid {BORDER};
            }}
            QMenu::item:selected {{ background:{ACCENT}33; }}
            QToolBar {{
                background:{PANEL};border-bottom:1px solid {BORDER};spacing:4px;
                padding:2px 4px;
            }}
            QTabWidget::pane {{ border:none; background:{DARK}; }}
            QTabBar::tab {{
                background:{PANEL};color:{FG_DIM};padding:6px 16px;
                border:1px solid {BORDER};border-bottom:none;margin-right:2px;
            }}
            QTabBar::tab:selected {{ background:{DARK};color:{FG}; }}
            QTabBar::tab:hover {{ background:{SURFACE};color:{FG}; }}
            QDockWidget {{ background:{PANEL};color:{FG}; }}
            QDockWidget::title {{
                background:{PANEL};color:{FG_DIM};padding:4px;
                font-size:11px;letter-spacing:1px;
            }}
            QStatusBar {{ background:{PANEL};color:{FG_DIM};font-size:11px; }}
            QTreeView {{
                background:{PANEL};color:{FG};border:none;
                alternate-background-color:{SURFACE};
            }}
            QTreeView::item:selected {{ background:{ACCENT}33; }}
            QScrollBar:vertical {{ background:{PANEL};width:8px; }}
            QScrollBar::handle:vertical {{
                background:{BORDER};border-radius:4px;min-height:20px;
            }}
            QToolTip {{
                background:{SURFACE};color:{FG};border:1px solid {BORDER};padding:4px;
            }}
            """
        )

    # ── UI layout ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.tabCloseRequested.connect(self._close_tab)
        self._tabs.currentChanged.connect(self._on_tab_switched)
        self.setCentralWidget(self._tabs)

        start_dir = PROJECT_ROOT if (PROJECT_ROOT / "quizmark").is_dir() else Path.home()
        self._fs_model = QFileSystemModel(self)
        self._fs_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self._fs_model.setNameFilters(["*.qm"])
        self._fs_model.setNameFilterDisables(False)
        root_index = self._fs_model.setRootPath(str(start_dir))

        self._tree = QTreeView()
        self._tree.setModel(self._fs_model)
        self._tree.setRootIndex(root_index)
        for column in (1, 2, 3):
            self._tree.hideColumn(column)
        self._tree.doubleClicked.connect(self._tree_open)
        self._tree.setHeaderHidden(True)

        dock_files = QDockWidget("FILES", self)
        dock_files.setWidget(self._tree)
        dock_files.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_files)

        self._problems = ProblemsPanel()
        self._problems.line_requested.connect(self._goto_line)
        dock_probs = QDockWidget("PROBLEMS", self)
        dock_probs.setWidget(self._problems)
        dock_probs.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock_probs)

        self._output_view = QTextEdit()
        self._output_view.setReadOnly(True)
        self._output_view.setStyleSheet(
            f"""
            QTextEdit {{
                background:{DARK};color:{FG};border:none;
                font-family:Consolas,'Courier New',monospace;font-size:12px;
                padding:6px;
            }}
            """
        )
        dock_out = QDockWidget("OUTPUT", self)
        dock_out.setWidget(self._output_view)
        dock_out.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock_out)
        self.tabifyDockWidget(dock_probs, dock_out)
        dock_probs.raise_()

        self._status_path = QLabel("")
        self._status_pos = QLabel("Ln 1, Col 1")
        self._status_state = QLabel("Ready")
        status_bar = self.statusBar()
        status_bar.addPermanentWidget(self._status_path, 1)
        status_bar.addPermanentWidget(self._status_pos)
        status_bar.addPermanentWidget(self._status_state)

    # ── Menu bar ───────────────────────────────────────────────────────────
    def _build_menu(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        self._add_action(file_menu, "&New", "Ctrl+N", self._new_file)
        self._add_action(file_menu, "&Open…", "Ctrl+O", self._open_file)
        self._add_action(file_menu, "Open &Folder…", "", self._open_folder)
        file_menu.addSeparator()
        self._add_action(file_menu, "&Save", "Ctrl+S", self._save)
        self._add_action(file_menu, "Save &As…", "Ctrl+Shift+S", self._save_as)
        file_menu.addSeparator()
        self._add_action(file_menu, "&Close Tab", "Ctrl+W", self._close_current_tab)
        self._add_action(file_menu, "E&xit", "Ctrl+Q", self.close)

        edit_menu = menu_bar.addMenu("&Edit")
        self._add_action(edit_menu, "&Undo", "Ctrl+Z", lambda: self._cur_editor() and self._cur_editor().undo())
        self._add_action(edit_menu, "&Redo", "Ctrl+Y", lambda: self._cur_editor() and self._cur_editor().redo())
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Cu&t", "Ctrl+X", lambda: self._cur_editor() and self._cur_editor().cut())
        self._add_action(edit_menu, "&Copy", "Ctrl+C", lambda: self._cur_editor() and self._cur_editor().copy())
        self._add_action(edit_menu, "&Paste", "Ctrl+V", lambda: self._cur_editor() and self._cur_editor().paste())
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Select &All", "Ctrl+A", lambda: self._cur_editor() and self._cur_editor().selectAll())
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Insert &Image Reference…", "Ctrl+I", self._insert_image_reference)
        self._add_action(edit_menu, "Insert &Economic Theme", "Ctrl+Alt+T", self._insert_economic_theme)

        run_menu = menu_bar.addMenu("&Run")
        self._add_action(run_menu, "▶  Validate", "F5", self._validate)
        self._add_action(run_menu, "▶  Lint", "F6", self._lint)
        self._add_action(run_menu, "▶  Preview Text", "F7", self._preview_text_run)

        export_menu = menu_bar.addMenu("E&xport")
        self._add_action(export_menu, "&Export…", "Ctrl+E", self._export)
        export_menu.addSeparator()
        for fmt in ["html", "json", "markdown", "text", "moodle"]:
            export_menu.addAction(f"Export as {fmt.upper()}", lambda checked=False, f=fmt: self._quick_export(f))

        view_menu = menu_bar.addMenu("&View")
        self._add_action(view_menu, "Zoom &In", "Ctrl+=", self._zoom_in)
        self._add_action(view_menu, "Zoom &Out", "Ctrl+-", self._zoom_out)
        self._add_action(view_menu, "Clear Output", "", self._clear_output)

        help_menu = menu_bar.addMenu("&Help")
        self._add_action(help_menu, "QuizMark DSL Reference", "", self._show_dsl_help)
        self._add_action(help_menu, "Image/Media Help", "", self._show_media_help)
        self._add_action(help_menu, "Grammar (BNF view)", "", self._show_grammar)
        self._add_action(help_menu, "Insert Question Template", "Ctrl+T", self._insert_template)
        self._add_action(help_menu, "Insert Economic Theme", "", self._insert_economic_theme)

    def _add_action(self, menu, label: str, shortcut: str, slot) -> QAction:
        action = QAction(label, self)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(lambda checked=False, callback=slot: callback())
        menu.addAction(action)
        return action

    # ── Toolbar ────────────────────────────────────────────────────────────
    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        def make_button(label: str, tip: str, slot, color: str = ACCENT) -> QPushButton:
            button = QPushButton(label)
            button.setToolTip(tip)
            button.setFixedHeight(26)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background:{color};color:{DARK};border:none;
                    padding:0 12px;border-radius:3px;font-weight:bold;font-size:11px;
                }}
                QPushButton:hover {{ background:{PURPLE}; }}
                """
            )
            button.clicked.connect(lambda checked=False, callback=slot: callback())
            return button

        toolbar.addWidget(make_button("+ New", "New file (Ctrl+N)", self._new_file))
        toolbar.addWidget(make_button("Open", "Open file (Ctrl+O)", self._open_file, SURFACE))
        toolbar.addWidget(make_button("Save", "Save (Ctrl+S)", self._save, SURFACE))
        toolbar.addSeparator()
        toolbar.addWidget(make_button("▶ Validate", "Validate (F5)", self._validate, GREEN))
        toolbar.addWidget(make_button("▶ Lint", "Lint (F6)", self._lint, TEAL))
        toolbar.addSeparator()
        toolbar.addWidget(make_button("Image Q", "Insert an image-question template", self._insert_image_question, ACCENT))
        toolbar.addWidget(make_button("Theme change", "Insert an economic classroom theme", self._insert_economic_theme, YELLOW))
        toolbar.addSeparator()
        toolbar.addWidget(make_button("Export…", "Export (Ctrl+E)", self._export, PURPLE))

    # ── Tab helpers ────────────────────────────────────────────────────────
    def _add_tab(self, tab: EditorTab) -> None:
        index = self._tabs.addTab(tab, tab.display_name)
        self._tabs.setCurrentIndex(index)
        tab.parse_errors_changed.connect(self._on_errors_changed)
        tab.modified_changed.connect(lambda: self._update_tab_title(tab))
        tab.path_changed.connect(lambda: (self._update_tab_title(tab), self._update_title()))
        tab.editor.cursorPositionChanged.connect(self._update_cursor)
        self._update_tab_title(tab)
        self._update_title()
        self._update_cursor()

    def _cur_tab(self) -> EditorTab | None:
        widget = self._tabs.currentWidget()
        return widget if isinstance(widget, EditorTab) else None

    def _cur_editor(self) -> Editor | None:
        tab = self._cur_tab()
        return tab.editor if tab else None

    def _update_tab_title(self, tab: EditorTab) -> None:
        index = self._tabs.indexOf(tab)
        if index < 0:
            return
        name = tab.display_name
        if tab.is_modified:
            name = "• " + name
        self._tabs.setTabText(index, name)
        self._update_title()

    def _on_tab_switched(self, index: int) -> None:
        del index
        self._update_title()
        self._update_cursor()
        tab = self._cur_tab()
        self._problems.set_errors(tab.errors if tab else [])

    def _close_tab(self, index: int) -> None:
        tab = self._tabs.widget(index)
        if isinstance(tab, EditorTab) and tab.is_modified:
            response = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"Save changes to {tab.display_name}?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
            )
            if response == QMessageBox.StandardButton.Save and not tab.save():
                return
            if response == QMessageBox.StandardButton.Cancel:
                return
        self._tabs.removeTab(index)

    def _close_current_tab(self) -> None:
        index = self._tabs.currentIndex()
        if index >= 0:
            self._close_tab(index)

    # ── File actions ───────────────────────────────────────────────────────
    def _new_file(self) -> None:
        dialog = NewFileDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        tab = EditorTab()
        tab.set_text(dialog.template(), modified=True)
        self._add_tab(tab)

    def _open_file(self, path: Path | str | bool | None = None) -> None:
        # QAction/QPushButton signals can pass a boolean checked value. Treat it as no file path.
        if not isinstance(path, (str, Path)):
            path = None
        if path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open QuizMark File",
                str(PROJECT_ROOT),
                "QuizMark Files (*.qm);;All Files (*)",
            )
            if not file_path:
                return
            path = Path(file_path)

        path = Path(path).expanduser().resolve()
        if not path.exists():
            QMessageBox.warning(self, "Open failed", f"File not found:\n{path}")
            return

        for i in range(self._tabs.count()):
            widget = self._tabs.widget(i)
            if isinstance(widget, EditorTab) and widget.path and widget.path.resolve() == path:
                self._tabs.setCurrentIndex(i)
                return

        tab = EditorTab(path)
        self._add_tab(tab)

    def _open_folder(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Open Folder", str(PROJECT_ROOT))
        if directory:
            root_index = self._fs_model.setRootPath(directory)
            self._tree.setRootIndex(root_index)

    def _save(self) -> None:
        tab = self._cur_tab()
        if tab and tab.save():
            self._update_tab_title(tab)

    def _save_as(self) -> None:
        tab = self._cur_tab()
        if tab and tab.save_as():
            self._update_tab_title(tab)
            self._update_title()

    # ── Tree ───────────────────────────────────────────────────────────────
    def _tree_open(self, index: QModelIndex) -> None:
        info = self._fs_model.fileInfo(index)
        if info.isFile():
            self._open_file(Path(info.absoluteFilePath()))

    # ── Validate / lint ────────────────────────────────────────────────────
    def _validate(self) -> None:
        tab = self._cur_tab()
        if not tab:
            return
        self._output("─── Validate ───")
        if not self._ensure_quizmark():
            return
        try:
            parser = QuizMarkParser()
            quiz_data = parser.parse_text(tab.text(), source=str(tab.path or "untitled"))
            validation_messages = [str(e) for e in validate_quiz(quiz_data)]
            media_warnings = media_path_warnings(quiz_data, tab.path)
            tab._quiz_data = quiz_data
            tab._errors = validation_messages + media_warnings
            self._on_errors_changed(tab._errors)

            if validation_messages:
                self._output(f"  Validation failed with {len(validation_messages)} issue(s).", warn=True)
                for error in validation_messages:
                    self._output(f"  ✗  {error}", warn=True)
                tab.preview.show_error("\n".join(validation_messages))
                return

            question_count = len(quiz_data.questions)
            answer_count = sum(len(question.answers) for question in quiz_data.questions)
            self._output("  Syntax      : PASS ✓", ok=True)
            self._output("  Validation  : PASS ✓", ok=True)
            self._output(f"  Questions   : {question_count}")
            self._output(f"  Answers     : {answer_count}")
            if media_warnings:
                for warning in media_warnings:
                    self._output(f"  ⚠  {warning}", warn=True)
                self._output("  Validation passed, but media warnings need attention.", warn=True)
            else:
                self._output("  ✓  Media paths look OK.", ok=True)
                self._output("  ✓  Ready to preview or export. Tip: use Export… for HTML, Moodle, PDF, or DOCX.", ok=True)
            tab._refresh_preview()
        except (ParserError, ValidationError) as exc:
            message = str(exc)
            tab._quiz_data = None
            tab._errors = [message]
            self._on_errors_changed(tab._errors)
            self._output(f"  ✗  {message}", warn=True)
        except Exception as exc:
            message = str(exc)
            tab._quiz_data = None
            tab._errors = [message]
            self._on_errors_changed(tab._errors)
            self._output(f"  ✗  {message}", warn=True)

    def _lint(self) -> None:
        tab = self._cur_tab()
        if not tab:
            return
        self._output("─── Lint ───")
        if not self._ensure_quizmark():
            return
        try:
            parser = QuizMarkParser()
            quiz_data = parser.parse_text(tab.text(), source=str(tab.path or "untitled"))
            validation_messages = [str(e) for e in validate_quiz(quiz_data)]
            media_warnings = media_path_warnings(quiz_data, tab.path)
            tab._quiz_data = quiz_data
            tab._errors = validation_messages + media_warnings
            self._on_errors_changed(tab._errors)

            question_count = len(quiz_data.questions)
            answer_count = sum(len(question.answers) for question in quiz_data.questions)
            correct_count = sum(1 for question in quiz_data.questions for answer in question.answers if answer.correct)
            has_theme = quiz_data.theme is not None
            has_meta = any([
                quiz_data.metadata.time_limit is not None,
                quiz_data.metadata.pass_mark is not None,
                quiz_data.metadata.shuffle is not None,
                bool(quiz_data.metadata.extras),
            ])
            media_refs = _collect_media_refs(quiz_data)
            local_media_refs = [ref for ref in media_refs if ref[0] in _LOCAL_MEDIA_KINDS and not _is_external_media_reference(ref[1])]

            self._output(f"  Title       : {quiz_data.title}")
            self._output(f"  Questions   : {question_count}")
            self._output(f"  Answers     : {answer_count}")
            self._output(f"  Correct     : {correct_count}")
            self._output(f"  Media refs  : {len(media_refs)} ({len(local_media_refs)} local files)")
            self._output(f"  Missing media: {len(media_warnings)}")
            self._output(f"  Theme       : {'yes' if has_theme else 'no'}")
            self._output(f"  Metadata    : {'yes' if has_meta else 'no'}")
            self._output(f"  Validation  : {'PASS ✓' if not validation_messages else 'FAIL ✗'}")

            for error in validation_messages:
                self._output(f"    ✗  {error}", warn=True)
            for warning in media_warnings:
                self._output(f"    ⚠  {warning}", warn=True)

            if not validation_messages and not media_warnings:
                self._output("  Lint complete — OK.", ok=True)
            elif not validation_messages:
                self._output("  Lint complete — validation passed, but media warnings were found.", warn=True)
            else:
                self._output("  Lint complete — fix validation errors before exporting.", warn=True)
        except (ParserError, ValidationError) as exc:
            message = str(exc)
            tab._quiz_data = None
            tab._errors = [message]
            self._on_errors_changed(tab._errors)
            self._output(f"  ✗  {message}", warn=True)
        except Exception as exc:
            message = str(exc)
            tab._quiz_data = None
            tab._errors = [message]
            self._on_errors_changed(tab._errors)
            self._output(f"  ✗  {message}", warn=True)

    def _preview_text_run(self) -> None:
        tab = self._cur_tab()
        if not tab:
            return
        self._output("─── Text Preview ───")
        if not self._ensure_quizmark():
            return
        try:
            parser = QuizMarkParser()
            quiz_data = parser.parse_text(tab.text(), source=str(tab.path or "untitled"))
            self._output(str(export_quiz_data(quiz_data, "text")), ok=True)
        except Exception as exc:
            self._output(str(exc), warn=True)

    def _ensure_quizmark(self) -> bool:
        if _QUIZMARK_OK:
            return True
        self._output(f"QuizMark library not available: {_IMPORT_ERR}", warn=True)
        return False

    # ── Export ─────────────────────────────────────────────────────────────
    def _export(self) -> None:
        tab = self._cur_tab()
        if not tab:
            return
        dialog = ExportDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        fmt, out_path = dialog.values()
        self._do_export(tab, fmt, out_path)

    def _quick_export(self, fmt: str) -> None:
        tab = self._cur_tab()
        if tab:
            self._do_export(tab, fmt, "")

    def _do_export(self, tab: EditorTab, fmt: str, out_path: str) -> None:
        if not self._ensure_quizmark():
            return
        self._output(f"─── Export ({fmt}) ───")
        try:
            parser = QuizMarkParser()
            quiz_data = parser.parse_text(tab.text(), source=str(tab.path or "untitled"))
            validation_errors = validate_quiz(quiz_data)
            if validation_errors:
                for error in validation_errors:
                    self._output(f"  ✗  {error}", warn=True)
                self._on_errors_changed([str(e) for e in validation_errors])
                return

            result = export_quiz_data(quiz_data, fmt)
            self._write_or_show_export(result, fmt, out_path)
        except (ParserError, ValidationError) as exc:
            self._output(f"  ✗  {exc}", warn=True)
        except Exception as exc:
            self._output(f"  ✗  {exc}", warn=True)

    def _write_or_show_export(self, result: str | bytes | dict[str, str], fmt: str, out_path: str) -> None:
        if isinstance(result, dict):
            if out_path:
                out_dir = Path(out_path)
                out_dir.mkdir(parents=True, exist_ok=True)
                for name, content in result.items():
                    (out_dir / name).write_text(content, encoding="utf-8")
                self._output(f"  ✓  Wrote web package to {out_dir}", ok=True)
            else:
                self._output(json.dumps(result, indent=2), ok=True)
            return

        if isinstance(result, bytes):
            if not out_path:
                default_ext = ".pdf" if fmt == "pdf" else ".docx"
                suggested = PROJECT_ROOT / f"quiz_export{default_ext}"
                selected, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Binary Export",
                    str(suggested),
                    f"{fmt.upper()} Files (*{default_ext});;All Files (*)",
                )
                if not selected:
                    self._output("  Export cancelled.", warn=True)
                    return
                out_path = selected
            Path(out_path).write_bytes(result)
            self._output(f"  ✓  Written to {out_path}", ok=True)
            return

        if out_path:
            Path(out_path).write_text(result, encoding="utf-8")
            self._output(f"  ✓  Written to {out_path}", ok=True)
        else:
            self._output(result, ok=True)

    # ── User-friendly insert helpers ─────────────────────────────────────────
    def _goto_line(self, line_no: int) -> None:
        editor = self._cur_editor()
        if not editor or line_no < 1:
            return
        block = editor.document().findBlockByNumber(line_no - 1)
        if not block.isValid():
            return
        cursor = QTextCursor(block)
        editor.setTextCursor(cursor)
        editor.setFocus()
        editor.centerCursor()

    def _insert_image_reference(self) -> None:
        editor = self._cur_editor()
        tab = self._cur_tab()
        if not editor or not tab:
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Image",
            str(tab.base_dir()),
            "Images (*.png *.jpg *.jpeg *.gif *.svg *.webp);;All Files (*)",
        )
        if not file_path:
            return
        image_path = Path(file_path).resolve()
        base = tab.base_dir().resolve()
        try:
            media_path = image_path.relative_to(base)
        except ValueError:
            try:
                media_path = image_path.relative_to(PROJECT_ROOT.resolve())
            except ValueError:
                media_path = image_path
        media_text = str(media_path).replace("\\", "/")
        prefix = "" if editor.textCursor().atBlockStart() else "\n"
        editor.insertPlainText(f'{prefix}IMAGE: "{media_text}"\n')
        self._output(f'Inserted image reference: IMAGE: "{media_text}"', ok=True)

    def _insert_image_question(self) -> None:
        editor = self._cur_editor()
        if not editor:
            return
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if editor.toPlainText().strip():
            cursor.insertText("\n\n")
        cursor.insertText(_IMAGE_QUESTION_SNIPPET)
        editor.setTextCursor(cursor)
        self._output("Inserted image question template. Replace images/example.jpg with your real image path.")

    def _insert_economic_theme(self) -> None:
        editor = self._cur_editor()
        if not editor:
            return
        text = editor.toPlainText()
        if "THEME" in text.upper():
            response = QMessageBox.question(
                self,
                "Theme already exists",
                "This file already contains a THEME block. Insert the economic theme anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if response != QMessageBox.StandardButton.Yes:
                return
        cursor = editor.textCursor()
        match = re.search(r"(?im)^\s*QUESTION\b", text)
        if match:
            cursor.setPosition(match.start())
            prefix = "" if text[:match.start()].endswith("\n\n") else "\n"
            cursor.insertText(prefix + _ECONOMIC_THEME_SNIPPET.rstrip() + "\n\n")
        else:
            cursor.movePosition(QTextCursor.MoveOperation.End)
            prefix = "\n\n" if text.strip() else ""
            cursor.insertText(prefix + _ECONOMIC_THEME_SNIPPET.rstrip() + "\n")
        editor.setTextCursor(cursor)
        self._output("Inserted economic theme snippet before the first question.", ok=True)

    def _show_media_help(self) -> None:
        self._output(
            """Image/Media Help
═══════════════════════════════════════════════════════

Use media lines after a question or answer:

QUESTION: Name this landmark
IMAGE: images/eiffel_tower.jpg
A: Eiffel Tower *
B: Statue of Liberty

Recommended project layout:

quiz1.qm
images/
  eiffel_tower.jpg
  liberty.jpg

Rules:
  • Relative paths are resolved from the folder of the saved .qm file.
  • If the file is not saved yet, relative paths resolve from the project root.
  • Use quotes for names with spaces: IMAGE: "images/eiffel tower.jpg"
  • URLs are allowed: IMAGE: https://example.com/picture.jpg
  • Run Lint to check missing local image/audio/video/attachment files.
"""
        )

    # ── Help ───────────────────────────────────────────────────────────────
    def _show_dsl_help(self) -> None:
        gui_notes = """QuizMark GUI Notes
═══════════════════════════════════════════════════════
• Validate (F5) parses the file and runs QuizMark semantic checks.
• Lint (F6) runs the same checks, then prints counts and media warnings.
• Local media paths are resolved relative to the saved .qm file folder.
  Example: IMAGE: "images/eiffel.jpg" means <quiz folder>/images/eiffel.jpg.
• Valid theme properties include background, foreground, accent, font, spacing, radius.
• Use Edit > Insert Economic Theme for a ready-made business/economics style.

"""
        docs_file = PROJECT_ROOT / "docs" / "dsl.md"
        if docs_file.exists():
            self._output(gui_notes + docs_file.read_text(encoding="utf-8"))
            return

        self._output(
            gui_notes
            + """QuizMark DSL Quick Reference
═══════════════════════════════════════════════════════

QUIZ: <title>
[TIME_LIMIT: <number>]
[PASS_MARK: <number>%]
[SHUFFLE: true|false]
[THEME { ... }]

QUESTION [(points=N)]: <text>
[IMAGE: <path>]
A: <text> [*]
B: <text> [*]

Correct answers end with *. Comments start with # or //.
"""
        )

    def _show_grammar(self) -> None:
        grammar_file = PROJECT_ROOT / "Quiz.g4"
        if grammar_file.exists():
            self._output("─── ANTLR4 Grammar (Quiz.g4) ───\n" + grammar_file.read_text(encoding="utf-8"))
        else:
            self._output(f"Quiz.g4 not found under {PROJECT_ROOT}", warn=True)

    def _insert_template(self) -> None:
        editor = self._cur_editor()
        if not editor:
            return
        snippet = "QUESTION: Your question here?\nA: Option one\nB: Option two *\nC: Option three\n"
        editor.insertPlainText(snippet)

    # ── Zoom ───────────────────────────────────────────────────────────────
    def _zoom_in(self) -> None:
        editor = self._cur_editor()
        if editor:
            font = editor.font()
            font.setPointSize(font.pointSize() + 1)
            editor.setFont(font)

    def _zoom_out(self) -> None:
        editor = self._cur_editor()
        if editor:
            font = editor.font()
            font.setPointSize(max(6, font.pointSize() - 1))
            editor.setFont(font)

    def _clear_output(self) -> None:
        self._output_view.clear()

    # ── Output helpers ─────────────────────────────────────────────────────
    def _output(self, text: str, warn: bool = False, ok: bool = False) -> None:
        color = RED if warn else GREEN if ok else FG
        cursor = self._output_view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        char_format = QTextCharFormat()
        char_format.setForeground(QColor(color))
        cursor.insertText(str(text) + "\n", char_format)
        self._output_view.setTextCursor(cursor)
        self._output_view.ensureCursorVisible()

    # ── Status bar ─────────────────────────────────────────────────────────
    def _update_title(self) -> None:
        tab = self._cur_tab()
        title = "QuizMark Studio — Economics Edition"
        if tab and tab.path:
            title += f" — {tab.path}"
            self._status_path.setText(str(tab.path))
        else:
            self._status_path.setText("")
        self.setWindowTitle(title)

    def _update_cursor(self) -> None:
        tab = self._cur_tab()
        if tab:
            line, column = tab.editor.line_col()
            self._status_pos.setText(f"Ln {line}, Col {column}")

    def _on_errors_changed(self, errors: list[str]) -> None:
        self._problems.set_errors(errors)
        warning_count = sum(1 for e in errors if str(e).lower().startswith("warning:"))
        error_count = len(errors) - warning_count
        if not errors:
            self._status_state.setText("No problems")
        elif error_count == 0:
            self._status_state.setText(f"{warning_count} warning{'s' if warning_count != 1 else ''}")
        elif warning_count == 0:
            self._status_state.setText(f"{error_count} problem{'s' if error_count != 1 else ''}")
        else:
            self._status_state.setText(f"{error_count} error(s), {warning_count} warning(s)")

    # ── Window close ──────────────────────────────────────────────────────
    def closeEvent(self, event) -> None:  # noqa: N802 - Qt override name
        for i in range(self._tabs.count()):
            tab = self._tabs.widget(i)
            if isinstance(tab, EditorTab) and tab.is_modified:
                response = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    f"Save changes to {tab.display_name} before closing?",
                    QMessageBox.StandardButton.Save
                    | QMessageBox.StandardButton.Discard
                    | QMessageBox.StandardButton.Cancel,
                )
                if response == QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                if response == QMessageBox.StandardButton.Save and not tab.save():
                    event.ignore()
                    return
        event.accept()


# ══════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════
def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("QuizMark IDE")
    app.setOrganizationName("QuizMark")

    window = MainWindow()
    window.show()

    opened_any = False
    for arg in sys.argv[1:]:
        file_path = Path(arg)
        if file_path.exists() and file_path.suffix == ".qm":
            window._open_file(file_path)
            opened_any = True

    if not opened_any:
        sample = PROJECT_ROOT / "quiz2.qm"
        if sample.exists():
            window._open_file(sample)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
