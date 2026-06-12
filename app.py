from fastapi import FastAPI

from advisor import financial_advisor

from portfolio import portfolio_summary

from stock import stock_advisor

app = FastAPI(
    title="Financial Advisor AI"
)


@app.get("/")
def home():

    return {

        "message":
        "Financial Advisor AI Running"

    }


@app.post("/chat")
def chat(payload: dict):

    question = payload.get(
        "question"
    )

    answer = financial_advisor(
        question
    )

    return {

        "answer":
        answer

    }


@app.post("/portfolio")
def portfolio(payload: dict):

    result = portfolio_summary(
        payload
    )

    return result

@app.post("/stock")
def stock(payload: dict):

    question = payload.get(
        "question"
    )

    answer = stock_advisor(
        question
    )

    return {

        "answer":
        answer

    }