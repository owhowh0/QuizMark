# QuizMark DSL Syntax

QuizMark uses a simple, line-oriented domain-specific language (DSL) for authoring quizzes. Each `.qm` file consists of a header, optional metadata, and one or more question blocks.

---

## Top-Level Structure

```
QUIZ: <title>

# Optional quiz-level media
IMAGE:  "path/to/image.png"
AUDIO:  "path/to/intro.mp3"
VIDEO:  "path/to/intro.mp4"
ATTACH: "path/to/handout.pdf"
MATH:   "x^2 + y^2 = z^2"

# Optional metadata
THEME { ... }
TIME_LIMIT: 30     # in minutes
PASS_MARK:  70%    # percentage required to pass
SHUFFLE:    true   # randomize question order

QUESTION: <text>
A: <answer>
B: <answer> *      # * marks the correct answer
```

---

## Questions

Questions begin with the `QUESTION:` keyword. You can optionally assign a point value and attach media.

```
QUESTION (points=2): Which planet is shown?
IMAGE: "images/mars.png"
AUDIO: "audio/clip.mp3"

A: Earth
B: Mars *
C: Venus
```

---

## Answers

- Answer labels run from `A:` to `Z:`
- Append `*` to mark an answer as correct
- Answers may contain plain text, a media line, or both
- Supported media inside answers: `IMAGE`, `AUDIO`, `VIDEO`, `ATTACH`, `MATH`
- A media line ending with `*` also marks that answer as correct

---

## Media Lines

Media lines can appear at the quiz level, inside a question, or inside an answer:

```
IMAGE:  "path/to/image.png"
AUDIO:  "path/to/clip.mp3"
VIDEO:  "path/to/video.mp4"
ATTACH: "path/to/file.pdf"
MATH:   "x^2 + y^2 = z^2"
```

Both quoted and unquoted paths are accepted. Paths are stored as-is.

---

## Theme Block

The `THEME` block allows lightweight visual styling metadata:

```
THEME {
    background = dark
    question [font=Arial, size=18]
    correct   [color=green]
}
```

See [Theme System](themes.md) for all supported properties and selectors.

---

## Comments & Blank Lines

Lines beginning with `#` or `//` are treated as comments and ignored. Blank lines are also ignored and can be used freely for readability.