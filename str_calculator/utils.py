import numpy_financial as npf
from fpdf import FPDF
import io

# 1. Cost Matrix (Per Square Foot Estimates)
REHAB_TIERS = {
    "Cosmetic Update (Paint & Floors)": 15.00,
    "Mid-Tier (Kitchen/Bath Refresh)": 45.00,
    "Full Gut (Down to Studs)": 95.00
}

def calculate_rehab_cost(sqft, tier):
    return sqft * REHAB_TIERS[tier]

def calculate_holding_costs(
    months,
    annual_property_taxes,
    annual_property_insurance,
    monthly_utility_costs,
    monthly_loan_payment
):
    total_annual_holding_expenses = annual_property_taxes + annual_property_insurance
    total_monthly_holding_expenses = (total_annual_holding_expenses / 12) + monthly_utility_costs + monthly_loan_payment
    return total_monthly_holding_expenses * months

def calculate_loan_payment(principal, annual_interest_rate, loan_term_years):
    if annual_interest_rate == 0 or loan_term_years == 0:
        return 0.0
    monthly_interest_rate = annual_interest_rate / 12 / 100
    number_of_payments = loan_term_years * 12
    return npf.pmt(monthly_interest_rate, number_of_payments, -principal)

def create_pdf_report(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Split the report text into lines and add to PDF
    for line in report_text.split('\n'):
        # Encode to latin-1 and replace unencodable characters
        # to handle potential non-ASCII characters that FPDF might struggle with
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output.getvalue()

def generate_report(
    purchase_price, sqft, rehab_tier_selection, months_holding,
    rehab_cost, holding_costs, total_project_cost,
    loan_amount, annual_interest_rate, loan_term_years, monthly_loan_payment,
    annual_property_taxes, annual_property_insurance, monthly_utility_costs,
    expected_monthly_rent, vacancy_rate, property_management_fees_percentage,
    annual_maintenance_repairs, annual_capex,
    gross_annual_income, total_annual_operating_expenses, net_operating_income,
    cash_flow_monthly, cash_flow_annual, cap_rate, grm, dscr,
    arv, selling_costs_percentage, selling_costs, net_sale_price, estimated_profit, roi
):
    report_content = f"""
Real Estate Investment Report
=============================

Property Details:
-----------------
Purchase Price: ${purchase_price:,.2f}
Square Footage: {sqft} sqft
Rehab Tier: {rehab_tier_selection}
Months Holding (Rehab Period): {months_holding}

Loan Details:
-------------
Loan Amount: ${loan_amount:,.2f}
Interest Rate: {annual_interest_rate:.2f}%
Loan Term: {loan_term_years} years
Monthly Loan Payment (P&I): ${monthly_loan_payment:,.2f}

Operating Expenses (Annualized):
--------------------------------
Annual Property Taxes: ${annual_property_taxes:,.2f}
Annual Property Insurance: ${annual_property_insurance:,.2f}
Monthly Utilities (during holding): ${monthly_utility_costs:,.2f}
Property Management Fees ({property_management_fees_percentage:.1f}%): ${gross_annual_income * (property_management_fees_percentage / 100):,.2f}
Ongoing Maintenance & Repairs: ${annual_maintenance_repairs:,.2f}
Capital Expenditures (CapEx): ${annual_capex:,.2f}
Total Annual Operating Expenses: ${total_annual_operating_expenses:,.2f}

Revenue Projections:
--------------------
Expected Monthly Rent: ${expected_monthly_rent:,.2f}
Vacancy Rate: {vacancy_rate:.1f}%
Gross Annual Income (Effective): ${gross_annual_income:,.2f}
Net Operating Income (NOI): ${net_operating_income:,.2f}

Calculated Costs:
-----------------
Estimated Rehab Cost: ${rehab_cost:,.2f}
Estimated Holding Costs (during rehab): ${holding_costs:,.2f}
Total Estimated Project Cost: ${total_project_cost:,.2f}

Key Financial Metrics:
----------------------
Monthly Cash Flow: ${cash_flow_monthly:,.2f}
Annual Cash Flow: ${cash_flow_annual:,.2f}
Capitalization Rate (Cap Rate): {cap_rate:,.2f}%
Gross Rent Multiplier (GRM): {grm:,.2f}
Debt Service Coverage Ratio (DSCR): {dscr:,.2f}

Exit Strategy & Profit:
-----------------------
After Repair Value (ARV): ${arv:,.2f}
Selling Costs Percentage: {selling_costs_percentage:.1f}%
Estimated Selling Costs: ${selling_costs:,.2f}
Net Sale Price: ${net_sale_price:,.2f}
Estimated Profit: ${estimated_profit:,.2f}
Return on Investment (ROI): {roi:,.2f}%

"""
    return report_content
