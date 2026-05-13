# Example QuizMark Files

These examples demonstrate how to write valid `.qm` files using the QuizMark DSL.

---

## Full Example

See [examples/geography.qm](../examples/geography.qm) for a complete, real-world quiz file covering:

- Quiz-level metadata (`TIME_LIMIT`, `PASS_MARK`, `SHUFFLE`)
- Questions with images and audio
- Multiple answer types (text, image, text + image)
- A `THEME` block

---

## Minimal Example

A minimal valid quiz with one question:

```
QUIZ: Sample Quiz

QUESTION: What is the capital of France?
A: Berlin
B: Paris *
C: Rome
```

---

## Question with Media

```
QUIZ: Geography Quiz

TIME_LIMIT: 20
PASS_MARK: 60%

QUESTION (points=2): Which planet is shown?
IMAGE: "images/mars.png"

A: Earth
B: Mars *
C: Venus
D: Jupiter
```

---

> For the full DSL syntax reference, see [dsl.md](dsl.md).  
> For all export options, see [exporters.md](exporters.md).