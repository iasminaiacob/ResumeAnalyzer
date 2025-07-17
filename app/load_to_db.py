import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion import ingest_resumes
from app.embedding import process_resume_chunks
from app.vector_store import insert_chunks

# Step 1: Load resumes
resumes = ingest_resumes("resumes") 
print(f"Loaded {len(resumes)} resumes.")

# Step 2: Chunk + Embed
chunked_data = process_resume_chunks(resumes)
print(f"Generated {len(chunked_data)} chunks.")

# Step 3: Insert into PostgreSQL
insert_chunks(chunked_data)