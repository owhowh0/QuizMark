# Export Formats

QuizMark supports exporting to multiple output formats via the CLI or Python API.

---

## Supported Formats

| Format        | `--format` value | Output              | Description                                      |
|---------------|------------------|---------------------|--------------------------------------------------|
| JSON          | `json`           | `.json` file        | Structured data, useful for custom integrations  |
| HTML          | `html`           | `.html` file        | Single-page rendered quiz                        |
| Markdown      | `markdown`       | `.md` file          | Readable plain-text representation               |
| Plain text    | `text`           | `.txt` file         | Stripped-down, no formatting                     |
| Moodle XML    | `moodle`         | `.xml` file         | Compatible with Moodle's Question Bank import    |
| DOCX          | `docx`           | `.docx` file        | Microsoft Word document                          |
| PDF           | `pdf`            | `.pdf` file         | Print-ready PDF                                  |
| Web package   | `web`            | folder              | Self-contained bundle (HTML + CSS + JS + JSON)   |

---

## CLI Usage

```
quizmark export file.qm --format <format> --out <output>
```

**Examples:**

```
quizmark export quiz.qm --format html    --out out.html
quizmark export quiz.qm --format moodle  --out quiz.xml
quizmark export quiz.qm --format web     --out web_bundle/
quizmark export quiz.qm --format pdf     --out quiz.pdf
```

---

> For Moodle-specific export details, see [moodle.md](moodle.md).