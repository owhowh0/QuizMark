# Python API

```python
from quizmark import Quiz

quiz = Quiz.load("quiz.qm")
quiz.validate()

html = quiz.render_html()
json_data = quiz.to_json()
moodle_zip = quiz.render_moodle_zip()  # bytes, requires Quiz.load() source path
```

## Data access

```python
quiz.data.title
quiz.data.questions[0].answers[0].text
quiz.data.questions[0].media
quiz.data.questions[0].answers[0].media
```
