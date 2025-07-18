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
```

### Testing
You’ll find test files for: resume ingestion, embedding pipeline, vector similarity search and chatbot output.

### Running the app
Clone the repository: git clone https://github.com/iasminaiacob/ResumeAnalyzer/
Create a .env file in the repo:
```bash
POSTGRES_URL=your_postgres_connection_string
GEMINI_API_KEY=your_gemini_api_key
```
Install dependencies: pip install -r requirements.txt
Start the backend server: uvicorn app.api:app --reload
Run the frontend:
```bash
cd resume-analyzer-ui
npm install
npm run dev
```

Example Use:
Upload resumes
Write job description in the frontend or CLI
Add new resume
Click "Compare All Candidates" and receive Gemini-generated summary of best matches
Click "Analyze" and receive Gemini-generated summary of whether the new candidate's resume is a match or not, and why.
