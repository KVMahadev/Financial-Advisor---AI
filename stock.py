import yfinance as yf

from config import client


# ==========================================
# FIND BEST INDIAN STOCK MATCH
# ==========================================

def find_indian_stock(company_name):

    try:

        search = yf.Search(
            company_name
        )

        quotes = search.quotes

        if not quotes:

            return None

        # Prefer NSE

        for stock in quotes:

            if stock.get("exchange") == "NSI":

                return stock

        # Prefer BSE

        for stock in quotes:

            if stock.get("exchange") == "BSE":

                return stock

        # Fallback

        return quotes[0]

    except Exception as e:

        print(
            f"Search Error: {e}"
        )

        return None


# ==========================================
# GET STOCK INFORMATION
# ==========================================

def get_stock_info(company_name):

    stock_match = find_indian_stock(
        company_name
    )

    if not stock_match:

        return None

    ticker = stock_match["symbol"]

    stock = yf.Ticker(
        ticker
    )

    hist = stock.history(
        period="5d"
    )

    current_price = None

    if not hist.empty:

        current_price = round(

            hist["Close"].iloc[-1],

            2

        )

    info = stock.info

    return {

        "Company":
        info.get(
            "longName"
        ),

        "Ticker":
        ticker,

        "Current Price":
        current_price,

        "Sector":
        info.get(
            "sector"
        ),

        "PE Ratio":
        info.get(
            "trailingPE"
        ),

        "52 Week High":
        info.get(
            "fiftyTwoWeekHigh"
        ),

        "52 Week Low":
        info.get(
            "fiftyTwoWeekLow"
        )

    }


# ==========================================
# EXTRACT COMPANY NAME
# ==========================================

def extract_company(question):

    prompt = f"""
Extract only the company name from the question.

Examples:

Question:
Can I invest in Tata Chemicals at current CMP?

Output:
Tata Chemicals

Question:
Should I buy Infosys?

Output:
Infosys

Question:
Is TCS a good long term investment?

Output:
TCS

Question:
What are the risks of investing in HDFC Bank?

Output:
HDFC Bank

Question:
{question}

Output:
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
        .strip()

    )


# ==========================================
# STOCK ADVISOR
# ==========================================

def stock_advisor(company_name):

    stock_info = get_stock_info(
        company_name
    )

    if not stock_info:

        return (
            "Unable to find stock information."
        )

    prompt = f"""

You are a financial advisor.

Stock Information:

Company: {stock_info['Company']}
Ticker: {stock_info['Ticker']}
Current Price: {stock_info['Current Price']}
Sector: {stock_info['Sector']}
PE Ratio: {stock_info['PE Ratio']}
52 Week High: {stock_info['52 Week High']}
52 Week Low: {stock_info['52 Week Low']}

User Question:

Can I invest in {company_name} at current CMP?

Provide:

## Market Snapshot

## Company Overview

## Key Positives

## Key Risks

## Investment Considerations

Use the exact values supplied above.

Do NOT provide buy/sell signals.

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