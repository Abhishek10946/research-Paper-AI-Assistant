from deconstructor.llm import chat


def ask_question(vectorstore, memory, question: str):
    docs = vectorstore.similarity_search(question, k=5)

    context = "\n\n".join(d.page_content for d in docs)

    history = ""
    for m in memory:
        history += f"{m['role']}: {m['content']}\n"

    prompt = f"""
You are an AI research assistant.

Context:
{context}

Conversation:
{history}

Question:
{question}

Answer clearly and concisely using the context.
"""

    return chat(prompt)
