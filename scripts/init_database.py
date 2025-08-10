import chromadb
from chromadb.config import Settings
import os
settings = Settings(
    persist_directory="chromadb",
    anonymized_telemetry=False
)
client = chromadb.Client(settings)
if 'faq_kb' in [c.name for c in client.list_collections()]:
    client.delete_collection('faq_kb')
collection = client.create_collection(
    name='faq_kb',
    metadata={"hnsw:space": "cosine"}
)
print('[INFO] Chroma DB initialized with collection: faq_kb')