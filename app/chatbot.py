import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.vector_store import search_similar_chunks
from collections import defaultdict

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

chat_model = genai.GenerativeModel("gemini-1.5-flash")

def start_chat_with_context(job_description: str, top_k: int = 5):
    """Start a Gemini chat with initial RAG context"""
    results = search_similar_chunks(job_description, top_k=top_k)
    MAX_CHUNKS_PER_RESUME = 3 #limit chunks per resume to avoid overwhelming the model

    grouped = defaultdict(list) #group results by filename
    for r in results:
        if len(grouped[r["filename"]]) < MAX_CHUNKS_PER_RESUME:
            grouped[r["filename"]].append(r["chunk"]) 

    context = "\n\n".join(
        f"Candidate: {filename}\n---\n" + "\n".join(chunks)
        for filename, chunks in grouped.items()
    )

    system_prompt = f"""
You are an AI assistant helping a recruiter evaluate resumes.
Based on the following job description and candidate content, explain who might be a good fit and why.
Use the candidate names (e.g., "Android-developer-resume.pdf") when evaluating. Do not treat all content as from one person.

Job Description:
{job_description}

Resume Chunks:
{context}

Answer with a summary of matching candidates and their strengths.
"""

    chat = chat_model.start_chat(history=[
        {"role": "user", "parts": [system_prompt]}
    ])

    return chat

#generates an answer based on the job description and resumes
def generate_rag_answer(job_description: str, top_k: int = 5) -> str:
    results = search_similar_chunks(job_description, top_k=top_k)

    if not results:
        return "No relevant candidates found."
    
    MAX_CHUNKS_PER_RESUME = 3

    grouped = defaultdict(list)
    for r in results:
        if len(grouped[r["filename"]]) < MAX_CHUNKS_PER_RESUME:
            grouped[r["filename"]].append(r["chunk"])

    context = "\n\n".join(
        f"Candidate: {filename}\n---\n" + "\n".join(chunks)
        for filename, chunks in grouped.items()
    )

    prompt = f"""
You are an AI recruiter assistant.

Based on the following job description and the resumes grouped by candidate, do the following:

1. Identify the candidate who is the best fit overall
2. Justify your choice using details from their resume
3. Include the candidate name (as labeled in the input)
4. Optionally, mention if any other candidates are also worth considering
5. Use the candidate names (e.g., "Android-developer-resume.pdf") when evaluating. Do not treat all content as from one person.

Job Description:
{job_description}

Resumes:
{context}
"""

    response = chat_model.generate_content(prompt)
    return response.text.strip()
