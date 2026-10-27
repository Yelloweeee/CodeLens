from app.ingestion.index_repository import index_repository


result = index_repository(
    "https://github.com/pallets/flask"
)

print(result)