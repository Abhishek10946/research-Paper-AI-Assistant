from groq import Groq
import os
from langchain_core.messages import HumanMessage, AIMessage


def get_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not set")
    return Groq(api_key=key)


def chat(messages, memory=None, temperature=0.2):
    client = get_client()

    full_messages = []

    if memory:
        full_messages.extend(memory.get())

    full_messages.extend(messages)

    payload = []
    for m in full_messages:
        role = "user" if isinstance(m, HumanMessage) else "assistant"
        payload.append({"role": role, "content": m.content})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=payload,
        temperature=temperature,
    )

    return response.choices[0].message.content
