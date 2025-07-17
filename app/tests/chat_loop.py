import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.chatbot import start_chat_with_context

job_desc = """
We are looking for an experienced AI/ML Engineer with strong Python and Computer Vision skills.
"""

chat = start_chat_with_context(job_desc, top_k=15)

while True:
    user_msg = input("👤 You: ")
    if user_msg.lower() in {"exit", "quit"}:
        break
    response = chat.send_message(user_msg)
    print("\n🤖 Gemini:", response.text.strip())
