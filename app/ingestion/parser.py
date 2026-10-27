import ast
from pathlib import Path


def parse_python_file(file_path: Path, repo_path: Path) -> list[dict]:
    """
    Extract top-level functions, async functions, and classes
    from a Python file.
    """

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (UnicodeDecodeError, SyntaxError, OSError):
        return []

    relative_path = file_path.relative_to(repo_path).as_posix()

    chunks = []

    for node in tree.body:

        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
        ):
            start_line = node.lineno
            end_line = node.end_lineno

            code = ast.get_source_segment(source, node)

            if not code:
                continue

            if isinstance(node, ast.ClassDef):
                chunk_type = "class"
                name = node.name

            elif isinstance(node, ast.AsyncFunctionDef):
                chunk_type = "async_function"
                name = node.name

            else:
                chunk_type = "function"
                name = node.name

            chunks.append(
                {
                    "name": name,
                    "type": chunk_type,
                    "file_path": relative_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "code": code,
                }
            )

    return chunks