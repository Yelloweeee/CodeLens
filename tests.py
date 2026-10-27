from pathlib import Path

from app.ingestion.parser import parse_python_file


def test_parse_python_file(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()

    file_path = repo_path / "example.py"

    file_path.write_text(
        "def greet(name):\n"
        "    return f'Hello, {name}'\n",
        encoding="utf-8",
    )

    chunks = parse_python_file(file_path, repo_path)

    assert len(chunks) == 1

    chunk = chunks[0]

    assert chunk["name"] == "greet"
    assert chunk["type"] == "function"
    assert chunk["file_path"] == "example.py"
    assert chunk["start_line"] == 1
    assert chunk["end_line"] == 2
    assert "Hello" in chunk["code"]