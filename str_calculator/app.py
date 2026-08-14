import streamlit as st

st.set_page_config(
    page_title="Real Estate Investment Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Welcome to the Real Estate Investment Calculator!")
st.write("Please use the sidebar to navigate through the different sections of the calculator.")

# Initialize session state variables if they don't exist
# This ensures that values persist across pages
if 'purchase_price' not in st.session_state:
    st.session_state.purchase_price = 200000
if 'sqft' not in st.session_state:
    st.session_state.sqft = 1500
if 'arv' not in st.session_state:
    st.session_state.arv = 300000
if 'rehab_tier_selection' not in st.session_state:
    st.session_state.rehab_tier_selection = "Cosmetic Update (Paint & Floors)"

if 'loan_amount' not in st.session_state:
    st.session_state.loan_amount = 150000
if 'annual_interest_rate' not in st.session_state:
    st.session_state.annual_interest_rate = 7.0
if 'loan_term_years' not in st.session_state:
    st.session_state.loan_term_years = 30

if 'months_holding' not in st.session_state:
    st.session_state.months_holding = 6
if 'annual_property_taxes' not in st.session_state:
    st.session_state.annual_property_taxes = 3000
if 'annual_property_insurance' not in st.session_state:
    st.session_state.annual_property_insurance = 1200
if 'monthly_utility_costs' not in st.session_state:
    st.session_state.monthly_utility_costs = 200

if 'expected_monthly_rent' not in st.session_state:
    st.session_state.expected_monthly_rent = 2500
if 'annual_maintenance_repairs' not in st.session_state:
    st.session_state.annual_maintenance_repairs = 1500
if 'vacancy_rate' not in st.session_state:
    st.session_state.vacancy_rate = 5.0
if 'annual_capex' not in st.session_state:
    st.session_state.annual_capex = 1000
if 'property_management_fees_percentage' not in st.session_state:
    st.session_state.property_management_fees_percentage = 8.0
if 'selling_costs_percentage' not in st.session_state:
    st.session_state.selling_costs_percentage = 7.0
