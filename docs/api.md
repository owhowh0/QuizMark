# Python API

The QuizMark Python API lets you load, validate, and render `.qm` quiz files programmatically from within your application.

---

## Basic Usage

```python
from quizmark import Quiz

# Load a quiz file from disk
quiz = Quiz.load("quiz.qm")

# Validate structure and semantic rules
quiz.validate()

# Render to HTML string
html = quiz.render_html()

# Serialize to a Python dict (JSON-compatible)
json_data = quiz.to_json()
moodle_zip = quiz.render_moodle_zip()  # bytes, requires Quiz.load() source path
```

---

## Data Access

Once loaded, the quiz data is available via `quiz.data`:

```python
# Quiz title
quiz.data.title

# Access the first question's text
quiz.data.questions[0].text

# Access the first answer of the first question
quiz.data.questions[0].answers[0].text

# Access media attached to a question
quiz.data.questions[0].media

# Access media attached to a specific answer
quiz.data.questions[0].answers[0].media
```

> **Note:** `quiz.validate()` raises an exception if the file contains semantic errors (e.g. missing correct answer, empty image path). It is recommended to always call it after loading before accessing data.