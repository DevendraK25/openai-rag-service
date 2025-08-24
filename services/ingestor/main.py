import os
import psycopg2
import openai
from sources.loader import load_sources
import hashlib

DB_URL = os.getenv("DB_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

def ensure_table():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding VECTOR(3072),
        source TEXT,
        content_hash TEXT UNIQUE
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def embed_text(text: str):
    resp = openai.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return resp.data[0].embedding

def compute_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def ingest_all():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    sources = load_sources()
    for src in sources:
        for f in src.list_files():
            text = src.read_file(f)
            content_hash = compute_hash(text)
            cur.execute("SELECT 1 FROM documents WHERE content_hash = %s", (content_hash,))
            if cur.fetchone() is None:
                emb = embed_text(text)
                cur.execute(
                    "INSERT INTO documents (content, embedding, source, content_hash) VALUES (%s, %s, %s, %s)",
                    (text, emb, str(f), content_hash)
                )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ensure_table()
    ingest_all()
    print("✅ Ingestion complete")
