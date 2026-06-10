from portfolio import portfolio_summary

profile = {

    "name": "Krish",

    "age": 30,

    "monthly_income": 50000,

    "monthly_expenses": 20000,

    "risk_appetite": "low",

    "financial_goal": "home",

    "goal_amount": 6000000,

    "goal_years": 8,

    "investment_horizon": "8",

    "existing_investments": "no",

    "emergency_fund": 500000,

    "dependents": 3

}

print(
    portfolio_summary(
        profile
    )
)