# CLI Usage

```
quizmark validate file.qm
quizmark validate file1.qm file2.qm
quizmark lint file.qm
quizmark preview file.qm
quizmark export file.qm --format html --out out.html
quizmark export file.qm --format moodle --out quiz.xml
quizmark export file.qm --format web --out web_bundle
quizmark export file.qm --format docx --out quiz.docx
quizmark export file.qm --format pdf --out quiz.pdf
quizmark docs
quizmark version
```

Exit codes:
- `0` success
- `1` parse/validation error
