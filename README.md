# QuizMark — Lightweight Quiz DSL and Multi-Format Exporter

QuizMark is a Python-based quiz authoring and export tool built around a simple `.qm` domain-specific language. It supports parsing, validation, theming, rich media handling, previewing, and exporting quizzes to multiple formats, including web, Moodle, PDF, and DOCX.

## Quick start

```bash
python -m quizmark validate examples/geography.qm
python -m quizmark export examples/geography.qm --format html --out quiz.html
python -m quizmark export examples/geography.qm --format web --out web_bundle
```

## What QuizMark Does

- Parses `.qm` quiz files using a custom handwritten parser.
- Validates quiz structure, answer correctness, required metadata, and media references.
- Provides a desktop editor with syntax highlighting, preview, live linting, and export tools.
- Exports quizzes to:
  - HTML
  - JSON
  - Markdown
  - Plain text
  - Moodle XML
  - DOCX
  - PDF
  - Self-contained web package
- Supports images, audio/video references, attachments, and math notation.

## Project Structure

```
QuizMark/
├── Front/Interface.py          # Optional PyQt6 GUI editor and preview tool
├── docs/                      # Documentation: CLI, API, exporters, DSL, Moodle, themes
├── examples/                  # Example `.qm` quiz files
├── quizmark/                  # Core Python package
│   ├── api/                   # Public API wrapper and export helpers
│   ├── cli/                   # Command-line interface
│   ├── exporters/             # Exporter implementations for all supported formats
│   ├── models/                # Quiz data model classes
│   ├── parser/                # Parser and error definitions
│   ├── themes/                # Theme parsing and support
│   └── validators/            # Quiz validation logic
├── Quiz.g4                    # Grammar definition
├── QuizVisitorImpl.py         # Visitor implementation for parse tree conversion
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── quiz1.qm                   # Sample quiz file
└── tests/                     # Test suite for parser, exporters, CLI, and validation
```

## Supported Export Formats

QuizMark can export parsed quizzes into these formats:

- `html` — styled HTML output
- `json` — structured quiz data
- `markdown` — readable markdown output
- `text` — plain text rendering
- `moodle` — Moodle-compatible XML for LMS import
- `docx` — Microsoft Word documents
- `pdf` — paginated PDF export
- `web` — self-contained web bundle with HTML/CSS/JS/JSON

## Command-Line Interface

Use the CLI for validation, linting, previewing, and exporting:

```bash
quizmark validate file.qm
quizmark lint file.qm
quizmark preview file.qm
quizmark export file.qm --format html --out out.html
quizmark export file.qm --format moodle --out quiz.xml
quizmark export file.qm --format web --out web_bundle
quizmark export file.qm --format docx --out quiz.docx
quizmark export file.qm --format pdf --out quiz.pdf
quizmark docs
quizmark version
```

Exit codes:
- `0` — success
- `1` — parse or validation error

## Desktop GUI

The optional PyQt6 GUI (`Front/Interface.py`) provides:

- Multi-tab `.qm` editing
- Syntax highlighting for QuizMark DSL
- Real-time parsing and linting
- HTML, text, and JSON preview modes
- Built-in problems panel with clickable line navigation
- File browser for `.qm` files
- Export dialog with format-aware output selection
- Quick export buttons and menu actions for common formats
- Insert templates for image questions and theme definitions

## API Usage

The Python API exposes quiz rendering and export methods through `quizmark.api.Quiz`:

```python
from quizmark.api import Quiz

quiz = Quiz.load('examples/geography.qm')
html = quiz.render_html()
json_data = quiz.to_json()
pdf_bytes = quiz.render_pdf()
```

Available render methods include:

 - `to_json()`
 - `render_html()`
 - `render_markdown()`
 - `render_text()`
 - `render_moodle_xml()`
 - `render_docx()`
 - `render_pdf()`
 - `render_web_package()`

## Grammar and Input Format

The `.qm` format supports:

- `QUIZ:` title declaration
- optional `THEME` blocks for custom styling
- expandable metadata fields
- `QUESTION:` blocks with optional `(points=N)` modifiers
- multiple answer options using `A:`, `B:`, `C:`, etc.
- correct answer marking using `*`
- media references using `IMAGE:`, `AUDIO:`, `VIDEO:`, `ATTACH:`, and `MATH:`

Example quiz:

```qm
QUIZ: World Landmarks
THEME {
    background = "#f7f4ea"
    question[font="Arial", size=17, color="#1f2d2a"]
    answer[font="Arial", size=14, color="#2c3e36"]
    correct[color="#1b5e20", weight="bold"]
}
TIME_LIMIT: 60
PASS_MARK: 70%
SHUFFLE: false

QUESTION(points=5): Name this structure
IMAGE: "assets/eiffel.jpg"
A: Eiffel Tower *
B: Statue of Liberty
C: Colosseum
```

## Documentation

See `docs/` for detailed documentation:

- `docs/cli.md`
- `docs/api.md`
- `docs/dsl.md`
- `docs/exporters.md`
- `docs/format.md`
- `docs/gui.md`
- `docs/moodle.md`
- `docs/semantic.md`
- `docs/themes.md`

## Development and Testing

Run tests with `pytest`:

```bash
pytest
```

## Dependencies

Primary dependencies are listed in `requirements.txt`:

- `rich==13.7.1`
- `pytest==8.2.2`
- `python-docx==1.1.2`
- `reportlab==4.2.5`
- `matplotlib==3.10.0`
- `svglib==1.5.1`

Optional GUI dependencies:

- `PyQt6`
- `PyQt6-WebEngine` (for HTML preview inside the app)

## Running the GUI

From the project root, if PyQt6 is installed:

```bash
python Front/Interface.py
```

## Notes

- The parser is a custom handwritten implementation
- The grammar file should not be edited without updating the parser accordingly.

## License

This project is intended for educational and development use.
