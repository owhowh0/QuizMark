from quizmark.cli.main import main


def test_cli_version(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["quizmark", "version"])
    assert main() == 0
    captured = capsys.readouterr()
    assert captured.out.strip()
