from rag import advisor_chat

from stock import (
    extract_company,
    stock_advisor
)


# ==========================================
# FINANCIAL ADVISOR ROUTER
# ==========================================

def financial_advisor(question):

    question_lower = question.lower()

    stock_keywords = [

        "invest in",
        "stock",
        "share",
        "cmp"

    ]

    if any(

        keyword in question_lower

        for keyword in stock_keywords

    ):

        company = extract_company(
            question
        )

        return stock_advisor(
            company
        )

    return advisor_chat(
        question
    )