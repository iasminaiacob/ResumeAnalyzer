import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.chatbot import start_chat_with_context

print("Enter the job description (press Enter twice to lock in): ")
lines = []
while True:
    line = input()
    if not line.strip():
        break
    lines.append(line)
job_desc = "\n".join(lines)

chat = start_chat_with_context(job_desc, top_k=15)

while True:
    user_msg = input("You: ")
    if user_msg.lower() in {"exit", "quit"}:
        break
    response = chat.send_message(user_msg)
    print("\nGemini:", response.text.strip())
