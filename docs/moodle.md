# Moodle Integration

QuizMark can export quizzes to Moodle-compatible XML format, ready to be imported directly into Moodle's Question Bank.

---

## Export

Use the CLI to generate the Moodle XML file:

```
quizmark export quiz.qm --format moodle --out quiz.xml
```

---

## Import into Moodle

1. Open your Moodle course
2. Navigate to **Question bank**
3. Click **Import**
4. Select **Moodle XML** as the file format
5. Upload the generated `quiz.xml` file

---

## Media Handling

| Media type  | Output in XML                              |
|-------------|---------------------------------------------|
| Image       | `<img src="path">` in question/answer text  |
| Audio       | `<audio>` HTML tag                          |
| Video       | `<video>` HTML tag                          |
| Attachment  | `<a href="path">` link                      |
| Math        | Inline MathJax syntax                       |

---

## Example XML Output

```xml
<quiz>
    <question type="multichoice">
        <name>
            <text>Which planet is shown?</text>
        </name>
        <questiontext format="html">
            <text><![CDATA[Which planet is shown?<br><img src="images/mars.png">]]></text>
        </questiontext>
        <answer fraction="100" format="html">
            <text><![CDATA[Mars]]></text>
        </answer>
        <answer fraction="0" format="html">
            <text><![CDATA[Earth]]></text>
        </answer>
    </question>
</quiz>
```

> **Note:** Only multiple-choice questions are currently exported to Moodle XML. The correct answer is exported with `fraction="100"`; all others with `fraction="0"`.