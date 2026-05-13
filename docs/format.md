# File Format Specification

QuizMark files use a simple line-oriented plain-text format with the `.qm` extension. Blank lines and comment lines (starting with `#` or `//`) are ignored by the parser.

---

## Required Elements

Every valid `.qm` file must contain:

1. A `QUIZ:` header line with the quiz title
2. At least one `QUESTION` block with at least two answers

---

## Optional Elements

The following are optional and can appear in any order after the `QUIZ:` line:

- `THEME { ... }` — visual styling metadata
- `TIME_LIMIT: <minutes>` — total time allowed
- `PASS_MARK: <percent>%` — minimum score to pass
- `SHUFFLE: true|false` — whether to randomize question order
- Media lines at the quiz level (see below)

---

## Image Syntax

```
IMAGE: "path/to/file.png"
```

Both quoted and unquoted paths are accepted. Paths are stored as-is and not resolved or validated by the parser.

---

## Media Lines

Media lines can appear at three levels: quiz, question, or answer. All follow the same syntax:

```
AUDIO:  "path/to/clip.mp3"
VIDEO:  "path/to/video.mp4"
ATTACH: "path/to/file.pdf"
MATH:   "x^2 + y^2 = z^2"
```

When a media line appears inside an answer block, it can be suffixed with `*` to mark that answer as correct:

```
A: 
IMAGE: "images/mars.png" *
```

---

## Structure Example

```
QUIZ: Solar System Quiz

TIME_LIMIT: 15
PASS_MARK: 70%
SHUFFLE: true

QUESTION: Which is the largest planet?
A: Earth
B: Saturn
C: Jupiter *
D: Neptune

QUESTION (points=2): What is shown in the image?
IMAGE: "images/nebula.png"
A: A galaxy
B: A nebula *
```

---

> For the full DSL syntax, see [dsl.md](dsl.md).  
> For semantic validation rules, see [semantic.md](semantic.md).