import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion import ingest_resumes
from app.embedding import process_resume_chunks
from app.vector_store import insert_chunks
from app.vector_store import setup_db

#This script is used to load resumes into the database and process them for vector storage

setup_db()  #ensure the database is set up before loading resumes

resumes = ingest_resumes("resumes_test") 
print(f"Loaded {len(resumes)} resumes.")

chunked_data = process_resume_chunks(resumes)
print(f"Generated {len(chunked_data)} chunks.")

insert_chunks(chunked_data)