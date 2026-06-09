# Moodle Integration

QuizMark can export quizzes to Moodle-compatible XML format, ready to be imported directly into Moodle's Question Bank.

---
QuizMark supports two Moodle import workflows.

## Direct plugin import (recommended for media)

Install the plugin from `moodle_plugin/qformat_quizmark` into Moodle's `question/format/quizmark` directory.

1. Go to Question bank → Import
2. Choose format: **QuizMark format**
3. Upload either:
   - a `.qm` file (text and URL-based media only), or
   - a `.zip` archive containing the `.qm` file and referenced media files
4. Import

The plugin embeds images, audio, and video into Moodle's file store using `@@PLUGINFILE@@` references. Attachments are imported as downloadable links.

### Package a quiz with media

```
quizmark export quiz.qm --format moodle-zip --out quiz.zip
```

The zip contains the `.qm` file plus any local files referenced by `IMAGE:`, `AUDIO:`, `VIDEO:`, and `ATTACH:` lines.

## Export

```
quizmark export quiz.qm --format moodle --out quiz.xml
```

## Import

1. Open Moodle
2. Go to Question bank
3. Choose Import
4. Select Moodle XML
5. Upload `quiz.xml`

Images are emitted as `<img src="path">` references in the question/answer text.
Audio, video, attachments, and math are emitted as HTML tags or inline MathJax syntax.

## Example XML

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