import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "models/embedding-001" #Gemini embedding model


def chunk_text(text: str, chunk_size: int = 400, chunk_overlap: int = 100) -> List[str]:
    #split text into chunks of max chunk_size chars with overlap of chunk_overlap chars
    #RecursiveCharacterTextSplitter splits text intelligently based on paragraphs and sentences
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """Generate embeddings using Gemini embedding-001 model"""
    embeddings = []

    for chunk in chunks:
        response = genai.embed_content(
            model="models/embedding-001",
            content=chunk,
            task_type="retrieval_document",
            title="Resume"
        )
        embeddings.append(response["embedding"])

    return embeddings

def process_resume_chunks(resumes: List[Dict]) -> List[Dict]:
    results = []
    for resume in resumes:
        chunks = chunk_text(resume["content"])
        embeddings = embed_chunks(chunks)
        for chunk, embedding in zip(chunks, embeddings):
            results.append({
                "filename": resume["filename"],
                "chunk": chunk,
                "embedding": embedding
            })
    return results
