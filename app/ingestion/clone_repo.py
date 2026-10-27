from pathlib import Path
from git import Repo


DATA_DIR = Path("data")


def clone_repository(repo_url: str) -> Path:
    """
    Clone a public GitHub repository into the data directory.

    Returns the local path of the cloned repository.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = DATA_DIR / repo_name

    if repo_path.exists():
        raise FileExistsError(
            f"Repository already exists at {repo_path}"
        )

    Repo.clone_from(
        repo_url,
        repo_path,
        depth=1,
    )

    return repo_path