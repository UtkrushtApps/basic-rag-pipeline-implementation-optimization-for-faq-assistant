import chromadb
from chromadb.config import Settings
import json
with open('config/database.json') as f:
    config = json.load(f)
def get_faq_collection():
    settings = Settings(
        persist_directory=config["chromadb_dir"],
        anonymized_telemetry=False
    )
    client = chromadb.Client(settings)
    return client.get_collection(config["collection"])
