# CLI Usage

The `quizmark` command-line tool lets you validate, preview, lint, and export quiz files directly from your terminal.

---

## Commands

### Validate

Check that a `.qm` file is structurally and semantically correct.

```
quizmark validate file.qm
quizmark validate file1.qm file2.qm
```

### Lint

Report style and formatting suggestions without blocking on errors.

```
quizmark lint file.qm
```

### Preview

Open an interactive preview of the quiz in your browser.

```
quizmark preview file.qm
```

### Export

Export a quiz to a specific output format.

```
quizmark export file.qm --format html    --out out.html
quizmark export file.qm --format moodle  --out quiz.xml
quizmark export file.qm --format web     --out web_bundle
quizmark export file.qm --format docx    --out quiz.docx
quizmark export file.qm --format pdf     --out quiz.pdf
```

See [Export Formats](exporters.md) for the full list of supported `--format` values.

### Help & Info

```
quizmark docs       # Open documentation in browser
quizmark version    # Print the installed version
```

---

## Exit Codes

| Code | Meaning                   |
|------|---------------------------|
| `0`  | Success                   |
| `1`  | Parse or validation error |