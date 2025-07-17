import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.vector_store import search_similar_chunks

job_desc = """
We are looking for an experienced AI/ML Engineer with strong Python/Computer Vision skills
to help us build and maintain automotive solutions. Experience with ASPP and performance optimization is a plus.
"""

results = search_similar_chunks(job_desc, top_k=10)

for i, res in enumerate(results, 1):
    print(f"\nResult #{i} (Score: {res['score']}) from {res['filename']}")
    print("-" * 60)
    print(res["chunk"][:500])  # Print first 500 chars
