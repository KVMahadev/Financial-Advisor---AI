from config import client, index

# ==========================================
# OPENAI EMBEDDING FUNCTION
# ==========================================

def get_embedding(text):

    response = client.embeddings.create(

        model="text-embedding-3-small",

        input=text,

        dimensions=512

    )

    return response.data[0].embedding


# ==========================================
# RAG FINANCIAL CHATBOT
# ==========================================

def advisor_chat(question):

    query_vector = get_embedding(
        question
    )

    results = index.query(

        vector=query_vector,

        top_k=3,

        include_metadata=True

    )

    matches = results.get(
        "matches",
        []
    )

    # ==========================================
    # CHECK RELEVANCE SCORE
    # ==========================================

    use_rag = False

    if len(matches) > 0:

        best_score = matches[0].get(
            "score",
            0
        )

        print(
            f"Best Match Score: {best_score}"
        )

        if best_score > 0.75:

            use_rag = True

    # ==========================================
    # RAG ANSWER
    # ==========================================

    if use_rag:

        context = "\n\n".join(

            [

                match["metadata"].get(
                    "text",
                    ""
                )

                for match

                in matches

            ]

        )

        prompt = f"""
You are a professional financial advisor.

Use ONLY the supplied context.

If the answer exists in the context:
- Explain clearly.
- Keep the answer concise.
- Use simple language.

Context:

{context}

Question:

{question}

Answer:
"""

    # ==========================================
    # GPT FALLBACK
    # ==========================================

    else:

        prompt = f"""
You are a professional financial advisor.

Answer the question using your general financial knowledge.

Question:

{question}

Answer:
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )

    return (

        response
        .choices[0]
        .message
        .content

    )