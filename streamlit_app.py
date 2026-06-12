import streamlit as st
import requests

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("💰 Financial Advisor AI")

    st.markdown("---")

    st.markdown("""
    ### Features

    📚 Knowledge Advisor

    📈 Stock Advisor

    💼 Portfolio Advisor
    """)

    st.markdown("---")

    st.info(
        "Powered by OpenAI, Pinecone, FastAPI and Streamlit"
    )

# ==========================================
# TITLE
# ==========================================

st.title("💰 Financial Advisor AI")

st.caption(
    "AI-Powered Investment, Portfolio and Stock Advisory Platform"
)

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "📚 Knowledge Advisor",
    "📈 Stock Advisor",
    "💼 Portfolio Advisor"
])

# ==========================================
# KNOWLEDGE ADVISOR
# ==========================================

with tab1:

    st.header("📚 Knowledge Advisor")

    question = st.text_area(
        "Ask a financial question"
    )

    if st.button(
        "Ask",
        key="knowledge"
    ):

        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "question": question
            }
        )

        result = response.json()

        st.success("Response")

        st.markdown(
            result["answer"]
        )

# ==========================================
# STOCK ADVISOR
# ==========================================

with tab2:

    st.header("📈 Stock Advisor")

    stock_question = st.text_input(
        "Ask about a stock"
    )

    if st.button(
        "Analyze Stock",
        key="stock"
    ):

        response = requests.post(
            "http://localhost:8000/stock",
            json={
                "question": stock_question
            }
        )

        result = response.json()

        st.subheader(
            "📈 Stock Analysis"
        )

        st.markdown(
            result["answer"]
        )

# ==========================================
# PORTFOLIO ADVISOR
# ==========================================

with tab3:

    st.header("💼 Portfolio Advisor")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Client Name"
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        monthly_income = st.number_input(
            "Monthly Income (₹)",
            value=100000
        )

        monthly_expenses = st.number_input(
            "Monthly Expenses (₹)",
            value=50000
        )

        dependents = st.number_input(
            "Number of Dependents",
            min_value=0,
            value=0
        )

    with col2:

        risk = st.selectbox(
            "Risk Appetite",
            [
                "low",
                "moderate",
                "high"
            ]
        )

        goal = st.selectbox(
            "Financial Goal",
            [
                "🏠 House Purchase",
                "🚗 Car Purchase",
                "🎓 Child Education",
                "💍 Marriage",
                "🏖 Vacation",
                "💼 Business Startup",
                "👴 Retirement",
                "💰 Wealth Creation"
            ]
        )

        amount = st.number_input(
            "Goal Amount (₹)",
            value=1000000
        )

        years = st.number_input(
            "Goal Years",
            value=10
        )

        existing_investments = st.number_input(
            "Existing Investments (₹)",
            value=0
        )

    if st.button(
        "Generate Financial Plan",
        key="portfolio"
    ):

        payload = {

            "name": name,
            "age": age,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "risk_appetite": risk,
            "financial_goal": goal,
            "goal_amount": amount,
            "goal_years": years,
            "investment_horizon": years,
            "existing_investments": existing_investments,
            "emergency_fund": 0,
            "dependents": dependents

        }

        response = requests.post(
            "http://localhost:8000/portfolio",
            json=payload
        )

        result = response.json()

        st.success(
            "Financial Plan Generated"
        )

        st.info(
            f"""
Goal: {goal}

Goal Amount: ₹{amount:,}

Time Horizon: {years} Years
"""
        )

        # ==================================
        # FINANCIAL HEALTH
        # ==================================

        monthly_surplus = (
            monthly_income
            - monthly_expenses
        )

        st.subheader(
            "💰 Financial Health"
        )

        fh1, fh2, fh3, fh4 = st.columns(4)

        with fh1:

            st.metric(
                "Monthly Surplus",
                f"₹{monthly_surplus:,}"
            )

        with fh2:

            st.metric(
                "Remaining Goal",
                f"₹{result.get('Remaining Goal', 0):,}"
            )

        with fh3:

            st.metric(
                "Existing Investments",
                f"₹{existing_investments:,}"
            )

        with fh4:

            st.metric(
                "Required SIP",
                f"₹{result.get('Required SIP', 0):,}"
            )

        if result.get(
            "Required SIP",
            0
        ) <= monthly_surplus:

            st.success(
                "✅ Goal appears achievable"
            )

        else:

            st.error(
                "❌ Goal may not be achievable with current savings"
            )

        # ==================================
        # INVESTMENT SUMMARY
        # ==================================

        st.subheader(
            "📊 Investment Summary"
        )

        s1, s2, s3 = st.columns(3)

        with s1:

            st.metric(
                "Equity SIP",
                f"₹{result.get('Equity SIP', 0):,}"
            )

        with s2:

            st.metric(
                "Debt SIP",
                f"₹{result.get('Debt SIP', 0):,}"
            )

        with s3:

            st.metric(
                "Gold SIP",
                f"₹{result.get('Gold SIP', 0):,}"
            )

        # ==================================
        # ASSET ALLOCATION
        # ==================================

        allocation = result.get(
            "Asset Allocation",
            {}
        )

        st.subheader(
            "🎯 Asset Allocation"
        )

        a1, a2, a3 = st.columns(3)

        with a1:

            st.metric(
                "Equity",
                f"{allocation.get('Equity', 0)}%"
            )

        with a2:

            st.metric(
                "Debt",
                f"{allocation.get('Debt', 0)}%"
            )

        with a3:

            st.metric(
                "Gold",
                f"{allocation.get('Gold', 0)}%"
            )

        # ==================================
        # RECOMMENDED FUNDS
        # ==================================

        st.subheader(
            "🏆 Recommended Funds"
        )

        for fund in result.get(
            "Recommended Funds",
            []
        ):

            with st.expander(
                fund.get(
                    "Fund",
                    "Fund"
                )
            ):

                st.write(
                    f"Category: {fund.get('Category', 'N/A')}"
                )

                st.write(
                    f"Monthly SIP: ₹{fund.get('Monthly SIP', 0):,}"
                )

                st.write(
                    f"5Y CAGR: {fund.get('5Y CAGR', 'N/A')}"
                )