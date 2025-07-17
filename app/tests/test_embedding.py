import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion import ingest_resumes
from app.embedding import process_resume_chunks

resumes = ingest_resumes("resumes")
chunked = process_resume_chunks(resumes)

print(f"\nGenerated {len(chunked)} chunks.")
print("\nSample chunk:\n", chunked[0]["chunk"][:300])
print("\nSample embedding (first 5 values):", chunked[0]["embedding"][:5])
