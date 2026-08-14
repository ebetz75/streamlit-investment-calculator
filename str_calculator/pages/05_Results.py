import streamlit as st
import pandas as pd
import sys
sys.path.append('..') # Add parent directory to path to import utils
from utils import (
    REHAB_TIERS,
    calculate_rehab_cost,
    calculate_holding_costs,
    calculate_loan_payment,
    create_pdf_report,
    generate_report
)

st.set_page_config(
    page_title="Results",
    page_icon="📈",
    layout="wide"
)

st.title("Investment Results")

# Retrieve values from session state
purchase_price = st.session_state.purchase_price
sqft = st.session_state.sqft
arv = st.session_state.arv
rehab_tier_selection = st.session_state.rehab_tier_selection

loan_amount = st.session_state.loan_amount
annual_interest_rate = st.session_state.annual_interest_rate
loan_term_years = st.session_state.loan_term_years
monthly_loan_payment = st.session_state.monthly_loan_payment # Already calculated and stored

months_holding = st.session_state.months_holding
annual_property_taxes = st.session_state.annual_property_taxes
annual_property_insurance = st.session_state.annual_property_insurance
monthly_utility_costs = st.session_state.monthly_utility_costs

expected_monthly_rent = st.session_state.expected_monthly_rent
annual_maintenance_repairs = st.session_state.annual_maintenance_repairs
vacancy_rate = st.session_state.vacancy_rate
annual_capex = st.session_state.annual_capex
property_management_fees_percentage = st.session_state.property_management_fees_percentage
selling_costs_percentage = st.session_state.selling_costs_percentage

st.header("Calculations")

# Core Calculations
rehab_cost = calculate_rehab_cost(sqft, rehab_tier_selection)
holding_costs = calculate_holding_costs(
    months_holding,
    annual_property_taxes,
    annual_property_insurance,
    monthly_utility_costs,
    monthly_loan_payment if loan_amount > 0 else 0 # Only include loan payment in holding if there's a loan
)

total_project_cost = purchase_price + rehab_cost + holding_costs
selling_costs = arv * (selling_costs_percentage / 100)
net_sale_price = arv - selling_costs
estimated_profit = net_sale_price - total_project_cost

# Annual Income and Expenses (for Cash Flow and Ratios)
gross_annual_income = (expected_monthly_rent * 12) * (1 - vacancy_rate / 100)
annual_property_management_fees = gross_annual_income * (property_management_fees_percentage / 100)

total_annual_operating_expenses = (
    annual_property_taxes
    + annual_property_insurance
    + (monthly_utility_costs * 12) # Assume utilities continue post-rehab if property is held
    + annual_maintenance_repairs
    + annual_capex
    + annual_property_management_fees
)

net_operating_income = gross_annual_income - total_annual_operating_expenses

# Key Financial Metrics
cap_rate = (net_operating_income / purchase_price) * 100 if purchase_price > 0 else 0.0
grm = purchase_price / gross_annual_income if gross_annual_income > 0 else 0.0
dscr = net_operating_income / (monthly_loan_payment * 12) if (monthly_loan_payment * 12) > 0 else 0.0

cash_flow_monthly = (net_operating_income - (monthly_loan_payment * 12)) / 12
cash_flow_annual = net_operating_income - (monthly_loan_payment * 12)

# Overall ROI
roi = (estimated_profit / total_project_cost) * 100 if total_project_cost > 0 else 0.0


st.subheader("Cost Summary")
col_disp1, col_disp2, col_disp3 = st.columns(3)
col_disp1.metric(label="Estimated Rehab Cost", value=f"${rehab_cost:,.2f}", help="Estimated cost for renovations.")
col_disp2.metric(label="Estimated Holding Costs", value=f"${holding_costs:,.2f}", help="Costs incurred during the rehab/vacant period (taxes, insurance, utilities, loan interest).")
col_disp3.metric(label="Total Estimated Project Cost", value=f"${total_project_cost:,.2f}", help="Purchase Price + Rehab Cost + Holding Costs.")

st.subheader("Profit & Return")
col_profit1, col_profit2, col_profit3 = st.columns(3)
col_profit1.metric(label="Net Sale Price (ARV - Selling Costs)", value=f"${net_sale_price:,.2f}", help="After Repair Value minus selling costs.")
col_profit2.metric(label="Estimated Profit", value=f"${estimated_profit:,.2f}", help="Net Sale Price minus Total Estimated Project Cost.")
col_profit3.metric(label="Return on Investment (ROI)", value=f"{roi:,.2f}%", help="(Estimated Profit / Total Estimated Project Cost) * 100.")

st.subheader("Cash Flow & Ratios")
col_cf1, col_cf2, col_cf3 = st.columns(3)
col_cf1.metric(label="Monthly Cash Flow", value=f"${cash_flow_monthly:,.2f}", help="Net Operating Income minus Annual Debt Service, divided by 12.")
col_cf2.metric(label="Annual Cash Flow", value=f"${cash_flow_annual:,.2f}", help="Net Operating Income minus Annual Debt Service.")
with col_cf3:
    st.metric(label="Capitalization Rate (Cap Rate)", value=f"{cap_rate:,.2f}%", help="Net Operating Income / Purchase Price. For income-generating properties.")
col_ratio1, col_ratio2 = st.columns(2)
col_ratio1.metric(label="Gross Rent Multiplier (GRM)", value=f"{grm:,.2f}", help="Purchase Price / Gross Annual Income. Simpler valuation multiple.")
col_ratio2.metric(label="Debt Service Coverage Ratio (DSCR)", value=f"{dscr:,.2f}", help="Net Operating Income / Annual Debt Service. Measures ability to cover loan payments.")

st.subheader("Cost Breakdown Visualization")
# Create a DataFrame for the bar chart
cost_data = pd.DataFrame({
    'Category': ['Purchase Price', 'Rehab Cost', 'Holding Costs'],
    'Amount': [purchase_price, rehab_cost, holding_costs]
})
st.bar_chart(cost_data.set_index('Category'))


st.subheader("ROI Sensitivity Analysis (by ARV)")
# Generate a range of ARV values around the input ARV for sensitivity analysis
arv_range = pd.Series([arv * (1 - p/100) for p in range(20, 0, -5)] + [arv * (1 + p/100) for p in range(0, 25, 5)])
arv_range = arv_range.sort_values().unique()

roi_sensitivity_data = []
for current_arv in arv_range:
    current_selling_costs = current_arv * (selling_costs_percentage / 100)
    current_net_sale_price = current_arv - current_selling_costs
    current_total_project_cost = purchase_price + rehab_cost + holding_costs # Assuming holding costs are fixed for this analysis
    current_estimated_profit = current_net_sale_price - current_total_project_cost

    current_roi = 0.0
    if current_total_project_cost > 0:
        current_roi = (current_estimated_profit / current_total_project_cost) * 100
    roi_sensitivity_data.append({'ARV': current_arv, 'ROI': current_roi})

roi_df = pd.DataFrame(roi_sensitivity_data)
roi_df['ARV'] = roi_df['ARV'].map(lambda x: f"${x:,.0f}") # Format ARV for display
st.line_chart(roi_df.set_index('ARV'))


st.subheader("Download Investment Report")
report_text = generate_report(
    purchase_price, sqft, rehab_tier_selection, months_holding,
    rehab_cost, holding_costs, total_project_cost,
    loan_amount, annual_interest_rate, loan_term_years, monthly_loan_payment,
    annual_property_taxes, annual_property_insurance, monthly_utility_costs,
    expected_monthly_rent, vacancy_rate, property_management_fees_percentage,
    annual_maintenance_repairs, annual_capex,
    gross_annual_income, total_annual_operating_expenses, net_operating_income,
    cash_flow_monthly, cash_flow_annual, cap_rate, grm, dscr,
    arv, selling_costs_percentage, selling_costs, net_sale_price, estimated_profit, roi
)

col_report1, col_report2 = st.columns(2)
with col_report1:
    st.download_button(
        label="Download Report (TXT)",
        data=report_text,
        file_name="investment_report.txt",
        mime="text/plain"
    )
with col_report2:
    pdf_report = create_pdf_report(report_text)
    st.download_button(
        label="Download Report (PDF)",
        data=pdf_report,
        file_name="investment_report.pdf",
        mime="application/pdf"
    )
