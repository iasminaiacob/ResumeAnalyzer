import os
import psycopg
from dotenv import load_dotenv
from app.embedding import embed_chunks

load_dotenv()
conn = psycopg.connect(os.getenv("POSTGRES_URL"), autocommit=True)

def setup_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
                    
            DROP TABLE IF EXISTS resume_chunks;

            CREATE TABLE IF NOT EXISTS resume_chunks (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                chunk TEXT,
                embedding VECTOR(768)
            );
        """)
    print("Table and extension ready.")

def insert_chunks(chunk_data: list):
    """
    Inserts a list of dicts: {filename, chunk, embedding} into the DB
    """
    with conn.cursor() as cur:
        for row in chunk_data:
            cur.execute(
                """
                INSERT INTO resume_chunks (filename, chunk, embedding)
                VALUES (%s, %s, %s)
                """,
                (row["filename"], row["chunk"], row["embedding"])
            )
    print(f"Inserted {len(chunk_data)} chunks into the database.")

def search_similar_chunks(job_description: str, top_k: int = 5) -> list:
    """Embed job description and perform vector similarity search"""
    query_embedding = embed_chunks([job_description])[0]

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT filename, chunk, embedding <=> %s::vector AS distance
            FROM resume_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (query_embedding, query_embedding, top_k)
        )


        results = cur.fetchall()

        for r in results:
            print("From resume:", r[0])
            print("Chunk preview:", r[1][:150], "\n")
    
    return [{
        "filename": r[0],
        "chunk": r[1],
        "score": round(r[2], 4)
    } for r in results]
