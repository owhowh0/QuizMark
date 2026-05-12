# File Format Specification

QuizMark files use a line-oriented format. Blank lines and comments (`#` or `//`) are ignored.

## Required

- `QUIZ: <title>` header
- One or more `QUESTION` blocks

## Optional

- `THEME { ... }` block
- `TIME_LIMIT`, `PASS_MARK`, `SHUFFLE` metadata

## Images

```
IMAGE: "path/to/file.png"
```

Quoted and unquoted paths are accepted. Paths are preserved as-is.

## Media

Media lines can appear at the quiz level, within questions, or within answers:

```
AUDIO: "path/to/clip.mp3"
VIDEO: "path/to/video.mp4"
ATTACH: "path/to/file.pdf"
MATH: "x^2 + y^2 = z^2"
```
