from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.ingestion import ingest_resumes
from app.embedding import process_resume_chunks
from app.vector_store import insert_chunks, search_similar_chunks
from app.chatbot import generate_rag_answer
from app.ingestion import extract_text_from_pdf
import tempfile
from app.chatbot import chat_model
import requests
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "https://resume-analyzer-psi.vercel.app", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "resumes"

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resumes = ingest_resumes(UPLOAD_DIR)
    chunks = process_resume_chunks(resumes)
    insert_chunks(chunks)
    return {"message": f"{file.filename} uploaded and processed."}


@app.post("/generate/")
async def generate_answer(job_description: str = Form(...)):
    answer = generate_rag_answer(job_description, top_k=15)
    return {"answer": answer}

@app.post("/save_resume/")
async def save_resume(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resumes = ingest_resumes(UPLOAD_DIR)
    chunks = process_resume_chunks(resumes)
    insert_chunks(chunks)
    return {"message": f"{file.filename} saved and added to database."}

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    content = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(content)

    resumes = [{"filename": file.filename, "content": extract_text_from_pdf("temp_resume.pdf")}]
    chunked = process_resume_chunks(resumes)
    
    context = "\n\n".join(f"From {r['filename']}:\n{r['chunk']}" for r in chunked)
    prompt = f"""
You are an AI recruiter assistant. Based on the following job description and resume content, assess this candidate's fit.

Job Description:
{job_description}

Resume Chunks:
{context}
"""

    response = chat_model.generate_content(prompt)
    return {"answer": response.text.strip()}