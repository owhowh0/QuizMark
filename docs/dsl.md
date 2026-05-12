# QuizMark DSL Syntax

## Top-level structure

```
QUIZ: <title>

IMAGE: "path/to/image.png"   # optional quiz-level media
AUDIO: "path/to/intro.mp3"
VIDEO: "path/to/intro.mp4"
ATTACH: "path/to/handout.pdf"
MATH: "x^2 + y^2 = z^2"

THEME { ... }   # optional
TIME_LIMIT: 30  # optional
PASS_MARK: 70%  # optional
SHUFFLE: true   # optional

QUESTION: <text>
A: <answer>
B: <answer> *
```

## Theme block

```
THEME {
    background = dark
    question [font=Arial, size=18]
    correct [color=green]
}
```

## Questions

```
QUESTION (points=2): Which planet is shown?
IMAGE: "images/mars.png"
AUDIO: "audio/clip.mp3"

A: Earth
B: Mars *
C: Venus
```

## Answers

- `A:` to `Z:` labels
- `*` marks correct answer
- Answers can be text, image, or text + image
- Answers can also include audio, video, attachments, or math lines

## Media lines

```
IMAGE: "path/to/image.png"
AUDIO: "path/to/clip.mp3"
VIDEO: "path/to/video.mp4"
ATTACH: "path/to/file.pdf"
MATH: "x^2 + y^2 = z^2"
```

Media lines inside answers can end with `*` to mark the answer correct.
