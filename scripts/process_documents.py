import os
import tiktoken
import uuid
import openai
from chromadb.config import Settings
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

openai.api_key = os.environ.get('OPENAI_API_KEY', 'sk-test')
settings = Settings(
    persist_directory="chromadb",
    anonymized_telemetry=False
)
client = chromadb.Client(settings)
collection = client.get_collection('faq_kb')

enc = tiktoken.get_encoding('cl100k_base')
def chunk_text(text, chunk_size=256, overlap=32):
    tokens = enc.encode(text)
    chunks = []
    pos = 0
    while pos < len(tokens):
        start = max(0, pos - overlap)
        end = min(len(tokens), pos + chunk_size)
        chunk_tokens = tokens[start:end]
        chunk_str = enc.decode(chunk_tokens)
        chunks.append((chunk_str, start, end))
        pos += chunk_size - overlap
    return chunks

docs_dir = 'data/documents'
for fname in os.listdir(docs_dir):
    if not fname.lower().endswith('.txt'):
        continue
    with open(os.path.join(docs_dir, fname), encoding='utf-8') as f:
        text = f.read()
    print(f'[INFO] Processing document: {fname}')
    doc_id = os.path.splitext(fname)[0]
    if doc_id.startswith('faq'): category = 'general'
    else: category = 'misc'
    # Split by Q&A
    qas = [q.strip() for q in text.split('\nQ: ') if q.strip()]
    all_chunks = []
    chunk_idx = 0
    for qa in qas:
        chunked = chunk_text(qa)
        for chunk, start, end in chunked:
            all_chunks.append({
                'chunk_id': str(uuid.uuid4()),
                'doc_id': doc_id,
                'chunk_index': chunk_idx,
                'category': category,
                'content': chunk,
                'start_position': start
            })
            chunk_idx += 1
    # Generate OpenAI-like embeddings via Sentence-Transformer as stand-in (OpenAI disabled in CI)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [c['content'] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()
    metadatas = [{k: c[k] for k in c if k != 'content'} for c in all_chunks]
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=[c['chunk_id'] for c in all_chunks])
    print(f'[INFO] Inserted {len(all_chunks)} chunks for {fname}')
print('[INFO] Document processing complete.')