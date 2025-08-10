import chromadb
from chromadb.config import Settings
settings = Settings(
    persist_directory="chromadb",
    anonymized_telemetry=False
)
client = chromadb.Client(settings)
colnames = [c.name for c in client.list_collections()]
assert 'faq_kb' in colnames, '[ERR] Missing collection!'
col = client.get_collection('faq_kb')
count = len(col.get()['ids'])
print(f'[OK] Chroma DB ready. Collection: faq_kb, Total Chunks: {count}')