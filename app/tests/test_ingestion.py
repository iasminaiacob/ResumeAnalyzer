import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion import ingest_resumes

resumes = ingest_resumes("resumes") 

for res in resumes:
    print(f"\n=== {res['filename']} ===")
    print(res['content'][:500])  # Print first 500 chars only
