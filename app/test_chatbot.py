import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.chatbot import generate_rag_answer

job_description = """
We are looking for an experienced AI/ML Engineer with strong Python and Computer Vision skills.
Knowledge of ASPP, embedded systems, and safety-critical pipelines is a plus.
"""

answer = generate_rag_answer(job_description, top_k=15)

print("\nAI Feedback\n")
print(answer)
