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

    context = "\n\n".join(

        [

            match["metadata"].get(
                "text",
                ""
            )

            for match

            in results["matches"]

        ]

    )

    prompt = f"""
You are a financial advisor.

Use only the supplied context.

If the answer is found:
- Explain in 2-4 sentences.
- Keep it simple.
- Do not make up information.

If the answer is not found:
Reply that the information is not available in the financial knowledge base.

Context:

{context}

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