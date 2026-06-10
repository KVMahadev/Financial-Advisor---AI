import pandas as pd


# ==========================================
# USER PROFILE TEMPLATE
# ==========================================

profile = {

    "name": None,
    "age": None,
    "monthly_income": None,
    "monthly_expenses": None,
    "risk_appetite": None,
    "financial_goal": None,
    "goal_amount": None,
    "goal_years": None,
    "investment_horizon": None,
    "existing_investments": None,
    "emergency_fund": None,
    "dependents": None

}


# ==========================================
# ASSET ALLOCATION ENGINE
# ==========================================

def get_asset_allocation(profile):

    age = int(
        profile["age"]
    )

    risk = (
        profile["risk_appetite"]
        .lower()
    )

    horizon = int(
        profile["goal_years"]
    )

    if age < 35:

        if risk == "high":

            if horizon >= 10:
                equity = 85

            elif horizon >= 5:
                equity = 80

            else:
                equity = 70

        elif risk in [
            "moderate",
            "medium"
        ]:

            if horizon >= 10:
                equity = 70

            else:
                equity = 60

        else:

            equity = 40

    elif age < 50:

        if risk == "high":

            if horizon >= 10:
                equity = 80

            elif horizon >= 5:
                equity = 70

            else:
                equity = 60

        elif risk in [
            "moderate",
            "medium"
        ]:

            if horizon >= 10:
                equity = 65

            else:
                equity = 55

        else:

            equity = 35

    else:

        if risk == "high":

            if horizon >= 10:
                equity = 70

            elif horizon >= 5:
                equity = 60

            else:
                equity = 50

        elif risk in [
            "moderate",
            "medium"
        ]:

            if horizon >= 10:
                equity = 55

            else:
                equity = 45

        else:

            equity = 25

    gold = 10

    debt = 100 - equity - gold

    allocation = {

        "Equity": equity,

        "Debt": debt,

        "Gold": gold

    }

    return allocation


# ==========================================
# SIP CALCULATOR
# ==========================================

def calculate_sip(

    target_amount,

    years,

    annual_return=12

):

    monthly_rate = (

        annual_return / 12 / 100

    )

    months = years * 12

    sip = (

        target_amount
        * monthly_rate

    ) / (

        ((1 + monthly_rate)
        ** months)

        - 1

    )

    return round(
        sip
    )


# ==========================================
# PORTFOLIO SUMMARY
# ==========================================

def portfolio_summary(profile):

    allocation = get_asset_allocation(
        profile
    )

    required_sip = calculate_sip(

        profile["goal_amount"],

        profile["goal_years"]

    )

    equity_sip = round(

        required_sip
        * allocation["Equity"]
        / 100

    )

    debt_sip = round(

        required_sip
        * allocation["Debt"]
        / 100

    )

    gold_sip = round(

        required_sip
        * allocation["Gold"]
        / 100

    )

    return {

        "Client Name":
        profile["name"],

        "Goal":
        profile["financial_goal"],

        "Required SIP":
        required_sip,

        "Asset Allocation":
        allocation,

        "Equity SIP":
        equity_sip,

        "Debt SIP":
        debt_sip,

        "Gold SIP":
        gold_sip

    }