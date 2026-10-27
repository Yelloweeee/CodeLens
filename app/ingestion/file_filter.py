from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "site-packages",
    "dist",
    "build",
}


def get_python_files(repo_path: Path) -> list[Path]:
    """
    Return Python source files while excluding common
    generated and dependency directories.
    """

    python_files = []

    for file_path in repo_path.rglob("*.py"):
        relative_path = file_path.relative_to(repo_path)

        if any(
            part in EXCLUDED_DIRS
            for part in relative_path.parts
        ):
            continue

        python_files.append(file_path)

    return python_files