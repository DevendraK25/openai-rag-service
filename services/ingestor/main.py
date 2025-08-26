import os
import psycopg2
import openai
from sources.loader import load_sources
import hashlib
from sqlalchemy import create_engine
import pandas as pd

DB_URL = os.getenv("DB_URL") # POSTGRES DB USED FOR VECTOR STORAGE
openai.api_key = os.getenv("OPENAI_API_KEY") # OPENAI API KEY
engine = create_engine(os.getenv("MYSQL_URL")) # MYSQL DB USED FOR QUERYING DATA TO SEND INTO RAG

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

def fetch_mysql_data():
    # # Example: holdings
    # df = pd.read_sql("SELECT * FROM holdings", engine)
    # docs = []
    # for _, row in df.iterrows():
    #     text = (
    #         f"User {row['user_id']} holds {row['quantity']} shares "
    #         f"of {row['ticker']} worth {row['market_value']}."
    #     )
    #     docs.append({"content": text, "source": "mysql:holdings"})
    return None

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
    print("Ingestion complete")
