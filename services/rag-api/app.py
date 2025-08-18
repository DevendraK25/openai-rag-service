from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import openai
import os

DB_URL = os.getenv("DB_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Query(BaseModel):
    q: str
    top_k: int = 3

def search_embeddings(query, k=3):
    # 1. Embed query
    q_emb = openai.embeddings.create(
        model="text-embedding-3-large",
        input=query
    ).data[0].embedding

    # Convert Python list -> string like "[0.123, -0.456, ...]"
    emb_str = "[" + ",".join(str(x) for x in q_emb) + "]"

    # 2. Vector search
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT content, source
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
    """, (emb_str, k))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


@app.post("/query")
def query(body: Query):
    docs = search_embeddings(body.q, body.top_k)
    context = "\n\n".join([d[0] for d in docs])
    print(context)
    prompt = f"Answer based on context:\n{context}\n\nQuestion: {body.q}"
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "answer": completion.choices[0].message.content,
        "sources": [d[1] for d in docs]
    }
