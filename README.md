<div align="center">

# ✦ QuizMark

**A domain-specific language for authoring, validating, and exporting digital quizzes.**

*Write once. Export everywhere.*

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-22c55e?style=flat-square)
![Formats](https://img.shields.io/badge/Export_Formats-8-f59e0b?style=flat-square)
![Parser](https://img.shields.io/badge/Parser-ANTLR4-6366f1?style=flat-square)
![GUI](https://img.shields.io/badge/GUI-PyQt6-0ea5e9?style=flat-square)

</div>

---

## What is QuizMark?

QuizMark is a Python-based quiz authoring tool built around a clean, human-readable `.qm` domain-specific language. Instead of wrestling with LMS interfaces or verbose XML, you write structured plain text — QuizMark handles validation, theming, and exporting to every format you need.

The parser is generated from `Quiz.g4` using **ANTLR4**, with a custom `QuizVisitorImpl` that walks the parse tree and produces typed Python dataclass models.

```qm
QUIZ: World Capitals
QUESTION: What is the capital of France?
A: Berlin
B: Paris *
C: Rome
```

That's a complete, valid quiz. Everything else is optional.

---

## ✦ Features at a Glance

| Area | What you get |
|------|-------------|
| **Language** | Clean `.qm` DSL with themes, metadata, media, and math |
| **Validation** | Instant feedback — syntax + semantic checks at parse time |
| **Export** | 8 formats: HTML, JSON, Markdown, Text, Moodle XML, DOCX, PDF, Web bundle |
| **GUI** | Full PyQt6 desktop editor with live preview and linting |
| **API** | Python API for programmatic quiz generation and rendering |
| **CLI** | Validate, lint, preview, and export from the terminal |
| **Media** | Images, audio, video, attachments, and LaTeX math |
| **Themes** | CSS-like block styling baked into the source file |

---

## ✦ Quick Start

```bash
# Validate a quiz file
python -m quizmark validate examples/geography.qm

# Export to HTML
python -m quizmark export examples/geography.qm --format html --out quiz.html

# Export a self-contained web bundle
python -m quizmark export examples/geography.qm --format web --out web_bundle/

# Run the parser directly (with optional parse tree output)
python main.py examples/geography.qm
python main.py examples/geography.qm --tree

# Launch the GUI editor
python Front/Interface.py
```

---

## ✦ The `.qm` Format

### Minimal valid quiz

The bare minimum: a title, one question, one correct answer.

```qm
QUIZ: Simple Math
QUESTION: What is 2 + 2?
A: 3
B: 4 *
C: 5
```

### Full-featured example

```qm
QUIZ: World Landmarks

THEME {
    background = "#f7f4ea"
    foreground = "#1a1a1a"
    accent     = "#2e7d32"
    font       = "Arial"
    spacing    = "1.5rem"
    radius     = "8px"

    question [font="Arial", size=17, color="#1f2d2a", weight="bold"]
    answer   [font="Arial", size=14, color="#2c3e36"]
    correct  [color="#1b5e20", weight="bold"]
    wrong    [color="#b71c1c"]
}

TIME_LIMIT: 60
PASS_MARK: 70%
SHUFFLE: false
DIFFICULTY: Easy
CATEGORY: Geography

QUESTION (points=5): Name this structure
IMAGE: "assets/eiffel.jpg"
A: Eiffel Tower *
B: Statue of Liberty
C: Colosseum

QUESTION (points=3): Which flag belongs to Italy?
A:
IMAGE: "images/france.png"
B:
IMAGE: "images/italy.png" *
C:
IMAGE: "images/germany.png"

QUESTION: The speed of light is approximately $3 \times 10^8$ m/s.
MATH: "$E = mc^2$"
A: True *
B: False
```

### Supported constructs

| Construct | Syntax | Notes |
|-----------|--------|-------|
| Quiz title | `QUIZ: My Title` | Required. Must be first line. |
| Theme block | `THEME { ... }` | Optional. CSS-like selectors. |
| Metadata | `TIME_LIMIT: 60` | Optional. Number, boolean, or string. |
| Question | `QUESTION (points=N): Text` | Points optional. |
| Answer option | `A: Text *` | Labels A–E. `*` marks correct answer. |
| Image | `IMAGE: "path/to/file.jpg"` | Quoted path required. |
| Audio | `AUDIO: "path/to/file.mp3"` | Attached to question or answer. |
| Video | `VIDEO: "path/to/file.mp4"` | Attached to question or answer. |
| Math | `MATH: "$E=mc^2$"` | LaTeX notation, rendered via MathJax in HTML. |
| Attachment | `ATTACH: "file.pdf"` | Supplementary file reference. |

### Correct answer placement

The `*` marker works for both text answers and image answers:

```qm
# Text answer — asterisk after the text
A: Paris *

# Image answer — asterisk after the IMAGE reference
A:
IMAGE: "flags/france.png" *
```

---

## ✦ Validation Rules

QuizMark validates your quiz at parse time and produces clear, line-numbered errors.

| Rule | Violation example | Error |
|------|-------------------|-------|
| At least one question required | File with only `QUIZ:` | `No questions found in quiz` |
| Every question needs answers | `QUESTION:` with no `A:` | `Question has no answers` |
| Exactly one correct answer | Two `*` markers, or none | `Question must have exactly one correct answer` |
| `IMAGE:` needs a quoted path | `IMAGE: assets/img.png` | `Expected quoted string after IMAGE:` |
| Metadata types must match | `TIME_LIMIT: abc` | `Expected number for TIME_LIMIT` |
| `PASS_MARK` must be 0–100% | `PASS_MARK: 120%` | `PASS_MARK out of valid range` |
| Answer labels must be A–E | Using `F:` | `Invalid answer label: F` |

---

## ✦ Data Model

QuizMark represents parsed quizzes as typed Python dataclasses:

```python
@dataclass
class AnswerData:
    label: str
    text: Optional[str]
    image: Optional[str]
    correct: bool

@dataclass
class QuestionData:
    text: str
    points: Optional[float]
    image: Optional[str]
    answers: list

    @property
    def correct_answers(self) -> list[AnswerData]:
        """Return only the answers marked as correct."""
        return [a for a in self.answers if a.correct]

@dataclass
class ThemeData:
    properties: dict   # key → value  (e.g. background = "#fff")
    styles: dict       # selector → {attr: value}  (e.g. question[font="Arial"])

@dataclass
class QuizData:
    title: str
    theme: Optional[ThemeData]
    metadata: dict
    questions: list[QuestionData]

    def to_dict(self) -> dict:
        """Serialize the quiz to a plain dict (used for JSON export).
        Note: theme is not included in serialization."""
        return {
            "title": self.title,
            "metadata": self.metadata,
            "questions": [
                {
                    "text": q.text,
                    "points": q.points,
                    "image": q.image,
                    "answers": [
                        {"label": a.label, "text": a.text,
                         "image": a.image, "correct": a.correct}
                        for a in q.answers
                    ],
                }
                for q in self.questions
            ],
        }
```

> **Note:** `to_dict()` serializes `title`, `metadata`, and `questions` only. The `theme` block is intentionally excluded from the dict/JSON output as it is used only for rendering.

---

## ✦ Export Formats

```bash
quizmark export file.qm --format <flag> --out <path>
```

| Format | Flag | Output |
|--------|------|--------|
| Styled HTML | `html` | Single `.html` file with embedded CSS and theme |
| JSON data | `json` | Structured quiz object via `to_dict()` |
| Markdown | `markdown` | Readable `.md` document with headings and lists |
| Plain text | `text` | Terminal-friendly, no markup |
| Moodle XML | `moodle` | LMS-importable `.xml` for Moodle / Canvas |
| Word document | `docx` | `.docx` with embedded images via python-docx |
| PDF | `pdf` | Paginated `.pdf` rendered via ReportLab |
| Web bundle | `web` | Folder: `index.html` + `quizmark.css` + `quizmark.js` + `quiz.json` |

### Batch export

Export an entire folder of quizzes in one command:

```bash
quizmark export examples/*.qm --format html --out output/
# Produces: output/geography.html, output/math.html, ...
```

---

## ✦ Command-Line Interface

```bash
quizmark validate file.qm               # Check syntax and semantics
quizmark lint     file.qm               # Full linting report with stats
quizmark preview  file.qm               # Quick plain-text preview

quizmark export file.qm --format html     --out out.html
quizmark export file.qm --format moodle   --out quiz.xml
quizmark export file.qm --format web      --out web_bundle/
quizmark export file.qm --format docx     --out quiz.docx
quizmark export file.qm --format pdf      --out quiz.pdf

quizmark docs                            # Open documentation index
quizmark version                         # Print current version
```

**Exit codes:** `0` = success · `1` = parse or validation error

### Running the parser directly

`main.py` provides a lightweight entry point that runs the ANTLR4 pipeline and pretty-prints the parsed quiz:

```bash
# Parse and print quiz structure
python main.py examples/geography.qm

# Print the raw ANTLR4 parse tree instead
python main.py examples/geography.qm --tree
```

`main.py` also validates the input before parsing:
- Exits with an error if the file does not exist
- Warns if the file does not have a `.qm` extension
- Reports the number of ANTLR4 syntax errors and exits with code `1` if any are found

---

## ✦ Desktop GUI

Launch with:

```bash
python Front/Interface.py
```

The PyQt6 editor gives you a full IDE-style experience:

- Multi-tab `.qm` file editing
- Syntax highlighting across all DSL constructs
- Debounced real-time parsing — triggers 500 ms after you stop typing
- HTML, plain text, and JSON preview modes side-by-side
- Problems panel with clickable errors that jump to the relevant line
- File browser filtered to `.qm` files
- Export dialog with format selection and directory picker
- One-click quick export for common formats
- Built-in templates for image questions and theme blocks

**Keyboard shortcuts**

| Action | Shortcut |
|--------|----------|
| Validate | `F5` |
| Lint | `F6` |
| Preview text | `F7` |
| Export dialog | `Ctrl+E` |
| Zoom in / out | `Ctrl++` / `Ctrl+-` |
| Undo / Redo | `Ctrl+Z` / `Ctrl+Y` |

---

## ✦ Python API

```python
from quizmark.api import Quiz

quiz = Quiz.load('examples/geography.qm')

# Text and structured formats
html       = quiz.render_html()
md         = quiz.render_markdown()
text       = quiz.render_text()
moodle_xml = quiz.render_moodle_xml()
json_str   = quiz.to_json()
data_dict  = quiz.to_dict()   # title + metadata + questions (theme excluded)

# Binary formats — returns bytes, write directly to disk
pdf_bytes  = quiz.render_pdf()
docx_bytes = quiz.render_docx()
with open("quiz.pdf", "wb") as f:
    f.write(pdf_bytes)

# Web bundle — returns dict of filename → content
bundle = quiz.render_web_package()
for filename, content in bundle.items():
    print(filename)   # index.html, quizmark.css, quizmark.js, quiz.json
```

### Accessing correct answers directly

```python
from quizmark.parser import QuizMarkParser

parser = QuizMarkParser()
quiz_data = parser.parse(source)

for question in quiz_data.questions:
    correct = question.correct_answers   # list[AnswerData]
    print(f"{question.text} → {[a.label for a in correct]}")
```

### Parse from a string

```python
from quizmark.parser import QuizMarkParser

source = """
QUIZ: Inline Quiz
QUESTION: What is the capital of France?
A: Berlin
B: Paris *
C: Rome
"""

parser = QuizMarkParser()
quiz_data = parser.parse(source)
```

### Error handling

```python
from quizmark.api import Quiz
from quizmark.parser import ParserError
from quizmark.validators import ValidationError

try:
    quiz = Quiz.load('broken.qm')
except ParserError as e:
    print(f"Syntax error on line {e.line}: {e.message}")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## ✦ Project Structure

```
QuizMark/
├── Front/
│   └── Interface.py           # PyQt6 GUI editor and preview tool
├── quizmark/
│   ├── api/                   # Public API — Quiz.load(), render_*(), to_*()
│   ├── cli/                   # CLI entry point and command handlers
│   ├── exporters/             # One module per export format
│   ├── models/                # QuizData, QuestionData, AnswerData, ThemeData
│   ├── parser/                # Parser wrapper + error definitions
│   ├── themes/                # Theme block parsing and CSS generation
│   └── validators/            # Semantic validation logic
├── docs/                      # Documentation per feature area
├── examples/                  # Sample .qm quiz files
├── tests/                     # Full test suite
├── Quiz.g4                    # ANTLR4 grammar definition
├── QuizVisitorImpl.py         # Visitor: ANTLR4 parse tree → QuizData
├── main.py                    # Direct parser entry point with --tree flag
├── requirements.txt
└── README.md
```

---

## ✦ Testing

```bash
pytest
```

| Test file | Coverage |
|-----------|----------|
| `tests/test_parser.py` | Grammar rules, tokenization, AST structure |
| `tests/test_validation.py` | Semantic rules, missing answers, bad metadata |
| `tests/test_exporters.py` | All 8 export formats for output correctness |
| `tests/test_cli.py` | CLI commands, exit codes, batch processing |

---

## ✦ Dependencies

**Install everything:**

```bash
pip install -r requirements.txt
pip install PyQt6 PyQt6-WebEngine   # optional — required for GUI
```

**Core (`requirements.txt`):**

```
antlr4-python3-runtime==4.13.0
rich==13.7.1
pytest==8.2.2
python-docx==1.1.2
reportlab==4.2.5
matplotlib==3.10.0
svglib==1.5.1
```

**Optional (GUI):**

```
PyQt6
PyQt6-WebEngine    # required for HTML preview inside the editor
```

---

## ✦ Notes

- **Parser:** Generated from `Quiz.g4` using ANTLR4. Do not edit `Quiz.g4` without updating `QuizVisitorImpl.py` to match the new parse tree structure.
- **`to_dict()` scope:** Serializes `title`, `metadata`, and `questions` only. The `theme` block is excluded — it is used for rendering, not data exchange.
- **`correct_answers`:** `QuestionData` exposes a `correct_answers` property that filters answers by the `correct` flag — useful when building custom exporters or validators.
- **`--tree` flag:** `main.py` accepts `--tree` to dump the raw ANTLR4 parse tree, useful for debugging grammar changes.
- **Media paths:** Resolved relative to the `.qm` file's directory first, then relative to the project root.
- **Math:** LaTeX-style notation (e.g. `$E=mc^2$`) rendered via MathJax in HTML and web bundle outputs.
- **SHUFFLE:** Affects question order in web bundle and HTML outputs only.
- **Architecture:** The `parser/` module has zero imports from `exporters/`, `gui/`, or `cli/` — fully format-agnostic. New export formats can be added without touching core grammar logic.

---

## ✦ Documentation

Full documentation lives in `docs/`:

| File | Contents |
|------|----------|
| `docs/dsl.md` | Complete DSL language reference |
| `docs/cli.md` | CLI usage guide and examples |
| `docs/api.md` | Python API reference |
| `docs/exporters.md` | Export format specifications |
| `docs/format.md` | `.qm` file format details |
| `docs/gui.md` | GUI integration guide |
| `docs/themes.md` | Theme system and customization |
| `docs/semantic.md` | Validation semantics |
| `docs/moodle.md` | Moodle integration and import/export |

---

<div align="center">

*QuizMark — built for educators, designed for developers.*

**FAF-243 · Technical University of Moldova · 2026**

</div>