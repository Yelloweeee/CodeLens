from pathlib import Path

from app.ingestion.clone_repo import clone_repository
from app.ingestion.file_filter import get_python_files
from app.ingestion.parser import parse_python_file
from app.indexing.embeddings import EmbeddingGenerator
from app.indexing.vector_store import CodeVectorStore

def embed_in_batches(
    generator,
    texts: list[str],
    batch_size: int = 32,
) -> list[list[float]]:

    embeddings = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        batch_embeddings = generator.embed_documents(
            batch
        )

        embeddings.extend(batch_embeddings)

    return embeddings

def index_repository(repo_url: str) -> dict:
    """
    Clone a repository, extract code chunks,
    generate embeddings, and store them in ChromaDB.
    """

    try:
        repo_path = clone_repository(repo_url)
    except FileExistsError:
        repo_name = repo_url.rstrip("/").split("/")[-1]
        repo_path = Path("data") / repo_name

    # Ensure repo_path is a Path object if clone_repository returned a string
    repo_path = Path(repo_path)

    python_files = get_python_files(repo_path)

    all_chunks = []

    for file_path in python_files:
        chunks = parse_python_file(
            file_path,
            repo_path,
        )

        all_chunks.extend(chunks)

    if not all_chunks:
        return {
            "repository": repo_path.name,
            "files_found": len(python_files),
            "chunks_created": 0,
            "message": "No supported code chunks found.",
        }

    embedding_generator = EmbeddingGenerator()

    texts = [
        chunk["code"]
        for chunk in all_chunks
    ]

    embeddings = embed_in_batches(
        embedding_generator,
        texts,
    )

    vector_store = CodeVectorStore(repo_path.name)

    vector_store.add_chunks(
        all_chunks,
        embeddings,
    )

    return {
        "repository": repo_path.name,
        "files_found": len(python_files),
        "chunks_created": len(all_chunks),
        "message": "Repository indexed successfully.",
    }