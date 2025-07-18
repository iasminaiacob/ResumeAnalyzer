import os
from typing import List, Dict
from pathlib import Path

import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as extract_pdfminer_text

def extract_text_from_pdf(filepath: str) -> str:
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to extract {filepath} with PyMuPDF: {e}")
        return extract_pdfminer_text(filepath)  # fallback

def extract_text_from_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def ingest_resumes(folder_path: str) -> List[Dict]:
    """
    Loads all PDF and TXT files from a folder, extracts text.
    Returns a list of dicts: {filename, content}
    """
    parsed = []
    files = Path(folder_path).glob("*")
    for file in files:
        if file.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(str(file))
        elif file.suffix.lower() == ".txt":
            text = extract_text_from_txt(str(file))
        else:
            continue
        parsed.append({
            "filename": file.name,
            "content": text.strip()
        })
    return parsed

