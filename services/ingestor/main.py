import os
import psycopg2
import openai
from pathlib import Path

DB_URL = os.getenv("DB_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

def ensure_table():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding VECTOR(3072),  -- dimension for text-embedding-3-large
        source TEXT
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

def ingest_folder(path="./data"):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    for file in Path(path).glob("*.txt"):
        text = file.read_text()
        emb = embed_text(text)
        cur.execute("INSERT INTO documents (content, embedding, source) VALUES (%s, %s, %s)",
                    (text, emb, str(file)))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ensure_table()
    ingest_folder("/data")
    print("✅ Ingestion complete")
