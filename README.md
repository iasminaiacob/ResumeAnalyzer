# AI Resume Analyzer

A full-stack AI-powered system that analyzes resumes against job descriptions using vector search and Retrieval-Augmented Generation (RAG). Upload resumes, input job descriptions, and receive tailored evaluations from an AI recruiter assistant.

## Features

### Core Functionality
- **Resume Ingestion**: Upload and parse multiple PDF resumes.
- **Text Chunking**: Resumes are chunked into manageable text segments.
- **Embedding Generation**: Vector embeddings are created using Gemini.
- **Vector Database Search**: Similarity search with pgvector on PostgreSQL.
- **RAG Chatbot**: Gemini API is used to answer job fit questions by referencing relevant resume segments.
- **API Endpoints (FastAPI)**:
  - `POST /upload/` - Upload and ingest new resumes
  - `POST /generate/` - Match job description with best candidates
  - `POST /analyze_resume/` - Analyze a single resume against a job description
  - `POST /save_resume/` - Save and embed resume for future comparisons

### User Interface
- Built with Next.js + TypeScript (initially deployed on Vercel, reverted to local for simplicity)
- Allows:
  - Resume upload
  - Job description input
  - Chat interaction with the AI
  - Candidate comparison

### Interactive CLI
Run `chat_loop.py` to start a conversational session:
```bash
python app/chat_loop.py
