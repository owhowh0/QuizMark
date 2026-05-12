from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.text import Text

from quizmark import __version__
from quizmark.api import Quiz
from quizmark.parser.errors import ParserError, ValidationError
from quizmark.validators import validate_quiz


console = Console()


def main() -> int:
    parser = argparse.ArgumentParser(prog="quizmark", description="QuizMark CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_cmd = sub.add_parser("validate", help="Validate a QuizMark file")
    validate_cmd.add_argument("files", nargs="+")

    lint_cmd = sub.add_parser("lint", help="Lint a QuizMark file")
    lint_cmd.add_argument("files", nargs="+")

    export_cmd = sub.add_parser("export", help="Export a QuizMark file")
    export_cmd.add_argument("files", nargs="+")
    export_cmd.add_argument(
        "--format",
        required=True,
        choices=["html", "json", "markdown", "text", "moodle", "web", "docx", "pdf"],
    )
    export_cmd.add_argument("--out", help="Output file or directory")

    preview_cmd = sub.add_parser("preview", help="Render a quick preview")
    preview_cmd.add_argument("files", nargs="+")

    sub.add_parser("docs", help="Show documentation")
    sub.add_parser("version", help="Show version")

    args = parser.parse_args()

    try:
        if args.command == "version":
            console.print(__version__)
            return 0
        if args.command == "docs":
            _print_docs()
            return 0

        if args.command == "validate":
            return _handle_validate(args.files)
        if args.command == "lint":
            return _handle_lint(args.files)
        if args.command == "preview":
            return _handle_preview(args.files)
        if args.command == "export":
            return _handle_export_many(args.files, args.format, args.out)
    except (ParserError, ValidationError) as exc:
        console.print(_error_text(str(exc)))
        return 1

    console.print(_error_text("Unknown command"))
    return 1


def _report_validation(errors: list[ValidationError], show_ok: bool = False) -> int:
    if errors:
        for err in errors:
            console.print(_error_text(str(err)))
        return 1
    if show_ok:
        console.print(Text("OK", style="green"))
    return 0


def _handle_export(quiz: Quiz, fmt: str, output: str | None) -> int:
    result = quiz.export(fmt)
    if fmt == "web":
        out_dir = Path(output) if output else Path("quizmark_web")
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, content in result.items():
            (out_dir / name).write_text(content, encoding="utf-8")
        console.print(Text(f"Wrote web package to {out_dir}", style="green"))
        return 0

    content = result
    if fmt in {"docx", "pdf"}:
        if not output:
            raise ParserError("--out is required for docx/pdf exports")
        Path(output).write_bytes(content)
        console.print(Text(f"Wrote {fmt} to {output}", style="green"))
        return 0

    if output:
        Path(output).write_text(content, encoding="utf-8")
        console.print(Text(f"Wrote {fmt} to {output}", style="green"))
        return 0

    console.print(content)
    return 0


def _handle_export_many(files: list[str], fmt: str, output: str | None) -> int:
    if len(files) == 1:
        quiz = Quiz.load(files[0])
        return _handle_export(quiz, fmt, output)

    if output:
        out_path = Path(output)
        if fmt == "web":
            if not out_path.is_dir():
                out_path.mkdir(parents=True, exist_ok=True)
        elif not out_path.is_dir():
            raise ParserError("--out must be a directory when exporting multiple files")
    else:
        out_path = None

    exit_code = 0
    for file_path in files:
        quiz = Quiz.load(file_path)
        base = Path(file_path).stem
        if fmt == "web":
            target = out_path / f"{base}_web" if out_path else Path(f"{base}_web")
            _handle_export(quiz, fmt, str(target))
        else:
            if out_path:
                target = out_path / f"{base}.{_extension_for_format(fmt)}"
                _handle_export(quiz, fmt, str(target))
            else:
                _handle_export(quiz, fmt, None)
        exit_code = max(exit_code, 0)
    return exit_code


def _extension_for_format(fmt: str) -> str:
    return {
        "html": "html",
        "json": "json",
        "markdown": "md",
        "text": "txt",
        "moodle": "xml",
        "docx": "docx",
        "pdf": "pdf",
    }[fmt]


def _handle_validate(files: list[str]) -> int:
    exit_code = 0
    for file_path in files:
        quiz = Quiz.load(file_path)
        errors = validate_quiz(quiz.data)
        if errors:
            console.print(Text(f"{file_path}", style="bold"))
        exit_code = max(exit_code, _report_validation(errors))
    return exit_code


def _handle_lint(files: list[str]) -> int:
    exit_code = 0
    for file_path in files:
        quiz = Quiz.load(file_path)
        errors = validate_quiz(quiz.data)
        if errors:
            console.print(Text(f"{file_path}", style="bold"))
        exit_code = max(exit_code, _report_validation(errors, show_ok=True))
    return exit_code


def _handle_preview(files: list[str]) -> int:
    for file_path in files:
        quiz = Quiz.load(file_path)
        if len(files) > 1:
            console.print(Text(f"{file_path}", style="bold"))
        console.print(quiz.render_text())
    return 0


def _print_docs() -> None:
    docs = Path("docs")
    if not docs.exists():
        console.print(_error_text("docs/ not found"))
        return
    for doc in sorted(docs.glob("*.md")):
        console.print(str(doc))


def _error_text(message: str) -> Text:
    return Text(message, style="bold red")


if __name__ == "__main__":
    raise SystemExit(main())
