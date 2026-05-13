# Semantic Rules

The QuizMark validator enforces a set of semantic rules beyond basic syntax. A file that parses correctly may still fail validation if these rules are violated.

---

## Enforced Rules

### Quiz Level

| Rule                          | Description                                      |
|-------------------------------|--------------------------------------------------|
| At least one question         | The quiz must contain one or more questions      |
| Valid `PASS_MARK`             | Must be a percentage between `0%` and `100%`    |
| Positive `TIME_LIMIT`         | Must be a number greater than zero               |
| Valid theme keys              | Only recognized theme properties are accepted    |

### Question Level

| Rule                          | Description                                               |
|-------------------------------|-----------------------------------------------------------|
| At least two answers          | Each question must have a minimum of two answer options   |
| At least one correct answer   | Each question must have at least one answer marked `*`    |
| No duplicate answer labels    | Labels `A:` through `Z:` must be unique within a question |
| Non-empty image paths         | `IMAGE:` values must not be blank                         |
| Non-empty media values        | `AUDIO:`, `VIDEO:`, `ATTACH:`, `MATH:` must not be blank  |

---

## Running Validation

**CLI:**
```
quizmark validate file.qm
```

**Python API:**
```python
from quizmark import Quiz

quiz = Quiz.load("quiz.qm")
quiz.validate()  # Raises an exception if any rule is violated
```

Validation errors include the question index and the specific rule that was violated, making it easy to pinpoint the issue.

---

> For the full file format specification, see [format.md](format.md).