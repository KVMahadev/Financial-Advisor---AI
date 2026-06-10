import pandas as pd

# ==========================================
# LOAD TOP FUNDS
# ==========================================

top_funds = pd.read_csv(
    "top_funds.csv"
)



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

    age = int(profile["age"])

    risk = profile["risk_appetite"].lower()

    horizon = int(profile["goal_years"])

    if age < 35:

        if risk == "high":

            if horizon >= 10:
                equity = 85
            elif horizon >= 5:
                equity = 80
            else:
                equity = 70

        elif risk in ["moderate", "medium"]:

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

        elif risk in ["moderate", "medium"]:

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

        elif risk in ["moderate", "medium"]:

            if horizon >= 10:
                equity = 55
            else:
                equity = 45

        else:
            equity = 25

    gold = 10

    debt = 100 - equity - gold

    return {

        "Equity": equity,
        "Debt": debt,
        "Gold": gold

    }

# ==========================================
# SIP CALCULATOR
# ==========================================

def calculate_sip(

    target_amount,
    years,
    annual_return=12

):

    monthly_rate = annual_return / 12 / 100

    months = years * 12

    sip = (

        target_amount
        * monthly_rate

    ) / (

        ((1 + monthly_rate) ** months)
        - 1

    )

    return round(sip)

# ==========================================
# EQUITY BREAKDOWN
# ==========================================

def get_equity_breakdown(profile):

    risk = profile["risk_appetite"].lower()

    if risk == "low":

        return {

            "Large Cap Index": 60,
            "Flexi Cap": 25,
            "Mid Cap": 10,
            "Small Cap": 5

        }

    elif risk in ["moderate", "medium"]:

        return {

            "Large Cap Index": 50,
            "Flexi Cap": 30,
            "Mid Cap": 10,
            "Small Cap": 10

        }

    else:

        return {

            "Large Cap Index": 45,
            "Flexi Cap": 25,
            "Mid Cap": 20,
            "Small Cap": 10

        }

# ==========================================
# FUND RECOMMENDATION ENGINE
# ==========================================

def generate_fund_recommendations(profile):

    allocation = get_asset_allocation(profile)

    required_sip = calculate_sip(

        profile["goal_amount"],
        profile["goal_years"]

    )

    sip_allocation = {}

    for asset, percentage in allocation.items():

        sip_allocation[asset] = round(

            required_sip
            * percentage
            / 100

        )

    equity_breakdown = get_equity_breakdown(
        profile
    )

    equity_sip = sip_allocation["Equity"]

    debt_sip = sip_allocation["Debt"]

    gold_sip = sip_allocation["Gold"]

    equity_sip_breakdown = {}

    for category, percentage in equity_breakdown.items():

        equity_sip_breakdown[category] = round(

            equity_sip
            * percentage
            / 100

        )

    category_sip_map = {

        "Equity Scheme - Large Cap Fund":
        equity_sip_breakdown.get(
            "Large Cap Index",
            0
        ),

        "Equity Scheme - Flexi Cap Fund":
        equity_sip_breakdown.get(
            "Flexi Cap",
            0
        ),

        "Equity Scheme - Mid Cap Fund":
        equity_sip_breakdown.get(
            "Mid Cap",
            0
        ),

        "Equity Scheme - Small Cap Fund":
        equity_sip_breakdown.get(
            "Small Cap",
            0
        ),

        "Debt Scheme - Corporate Bond Fund":
        round(debt_sip / 2),

        "Debt Scheme - Short Duration Fund":
        round(debt_sip / 2)

    }

    recommendations = []

    for _, row in top_funds.iterrows():

        fund_name = row["fund_name"]

        

        print("ORIGINAL:", fund_name)


        fund_name = fund_name.split(
        "(no. of segregated portfolios"
        )[0].strip()

        print("CLEANED:", fund_name)

        recommendations.append({

            "Fund":
            row["fund_name"],

            "Category":
            row["category"],

            "Monthly SIP":
            category_sip_map.get(
                row["category"],
                0
            ),

            "5Y CAGR":
            row["5Y CAGR"]

        })

    recommendations.append({

        "Fund":
        "Gold ETF",

        "Category":
        "Gold",

        "Monthly SIP":
        gold_sip,

        "5Y CAGR":
        None

    })

    return recommendations

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
        gold_sip,

        "Recommended Funds":
        generate_fund_recommendations(
            profile
        )

    }