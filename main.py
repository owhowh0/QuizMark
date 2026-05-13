import sys
from antlr4 import *
from QuizLexer import QuizLexer
from QuizParser import QuizParser
from QuizVisitorImpl import QuizVisitorImpl
from models import QuizData, ThemeData, QuestionData, AnswerData
from pathlib import Path

def print_quiz(quiz: QuizData) -> None:
    print(f"QUIZ: {quiz.title}")
    print("=" * 50)

    if quiz.theme:
        print("THEME:")
        for k, v in quiz.theme.properties.items():
            print(f"  {k} = {v!r}")
        for sel, attrs in quiz.theme.styles.items():
            attr_str = ", ".join(f"{k}={v}" for k, v in attrs.items())
            print(f"  {sel} [{attr_str}]")
        print()

    if quiz.metadata:
        print("METADATA:")
        for k, v in quiz.metadata.items():
            print(f"  {k}: {v}")
        print()

    for i, q in enumerate(quiz.questions, 1):
        pts = f" [{q.points} pts]" if q.points is not None else ""
        print(f"Q{i}{pts}: {q.text}")
        if q.image:
            print(f"  [image: {q.image}]")
        for ans in q.answers:
            marker = " *" if ans.correct else ""
            if ans.text and ans.image:
                line = f"  {ans.label}) {ans.text}  [image: {ans.image}]"
            elif ans.image:
                line = f"  {ans.label}) [image: {ans.image}]"
            else:
                line = f"  {ans.label}) {ans.text}"
            print(line + marker)
        print()


def main(argv):
    if len(argv) < 2:
        print("Usage: python main.py <qm_file> [--tree]", file=sys.stderr)
        sys.exit(1)

    show_tree = "--tree" in argv
    file_args = [a for a in argv[1:] if not a.startswith("--")]
    if not file_args:
        print("Usage: python main.py <qm_file> [--tree]", file=sys.stderr)
        sys.exit(1)

    path = Path(file_args[0])  # ← новое
    if not path.exists():  # ← новое
        print(f"Error: '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    if path.suffix != ".qm":  # ← новое
        print(f"Warning: expected .qm file, got '{path.suffix}'.", file=sys.stderr)

    input_stream = FileStream(str(path), encoding="utf-8")
    lexer = QuizLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = QuizParser(stream)
    tree = parser.quiz()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"Parse failed with {parser.getNumberOfSyntaxErrors()} syntax error(s).",
              file=sys.stderr)
        sys.exit(1)

    if show_tree:
        print(tree.toStringTree(recog=parser))
        return

    quiz = QuizVisitorImpl().visitQuiz(tree)
    print_quiz(quiz)


if __name__ == '__main__':
    main(sys.argv)


