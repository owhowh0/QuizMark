# Moodle Integration

QuizMark exports Moodle-compatible XML for multiple-choice questions.

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
	</question>
</quiz>
```
