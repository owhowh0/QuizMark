# GUI Integration Guide

QuizMark exposes a stable JSON schema designed to make GUI tooling straightforward. The recommended approach is to use the Python API as a backend layer and drive your interface from the structured JSON output.

---

## Recommended Workflow

1. **Load** the `.qm` file using the Python API
2. **Convert** to JSON with `Quiz.to_json()`
3. **Display** the structured data in your GUI
4. **Validate** on the fly and surface any errors as UI feedback
5. **Persist** changes back to `.qm` format after edits

```python
from quizmark import Quiz

quiz = Quiz.load("quiz.qm")
errors = []

try:
    quiz.validate()
except Exception as e:
    errors.append(str(e))

data = quiz.to_json()
# Pass `data` to your GUI layer; pass `errors` to your error display
```

---

## Notes

- The JSON schema is kept stable across minor versions, making it safe to build UI components against it.
- Validation errors are returned with enough context (question index, field name) to highlight the relevant part of the GUI.
- After the user edits the quiz in your GUI, serialize the result back to `.qm` format before saving to disk.

---

> For the full data model, see [format.md](format.md).  
> For validation rules, see [semantic.md](semantic.md).