import os
import requests

from dotenv import load_dotenv


load_dotenv()

JINA_API_URL = "https://api.jina.ai/v1/embeddings"

MODEL_NAME = os.getenv(
    "JINA_EMBEDDING_MODEL",
    "jina-code-embeddings-0.5b",
)


class EmbeddingGenerator:

    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")

        if not self.api_key:
            raise ValueError(
                "JINA_API_KEY is missing from your .env file."
            )

    def _embed(
        self,
        texts: list[str],
        task: str,
    ) -> list[list[float]]:

        if not texts:
            return []

        response = requests.post(
            JINA_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "input": texts,
                "task": task,
                "embedding_type": "float",
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()["data"]

        # Preserve the original order of the inputs.
        data.sort(key=lambda item: item["index"])

        return [
            item["embedding"]
            for item in data
        ]

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return self._embed(
            texts,
            task="nl2code.passage",
        )

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        embeddings = self._embed(
            [text],
            task="nl2code.query",
        )

        return embeddings[0]