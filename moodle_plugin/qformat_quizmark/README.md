# QuizMark Moodle Importer

This plugin adds a QuizMark (.qm) import format to Moodle's Question Bank.

## Supported Moodle versions

- 3.9 LTS
- 4.1 LTS
- 4.4 LTS
- 5.2 (demo)

## Install

1. Copy this folder to: `question/format/quizmark` (rename the folder to `quizmark`)
2. Visit Site administration -> Notifications to complete installation

## Import

1. Go to Question bank -> Import
2. Choose format: QuizMark format
3. Upload a `.qm` file
4. Import

## Media notes

- Image/audio/video/attachment values must be accessible URLs.
- Math is emitted as `\\( ... \\)` for MathJax-compatible rendering.

## Demo testing (moodle.org/demo)

1. Log in to the demo as manager/teacher
2. Navigate to Question bank -> Import
3. Choose QuizMark format
4. Upload your `.qm` file

If the demo blocks third-party plugins, you can still validate the import by using a local Moodle instance.
