import streamlit as st
import sys
sys.path.append('..') # Add parent directory to path to import utils
from utils import calculate_loan_payment

st.set_page_config(
    page_title="Financing Details",
    page_icon="💰",
    layout="wide"
)

st.title("Financing Details")

col_loan1, col_loan2, col_loan3 = st.columns(3)
with col_loan1:
    st.session_state.loan_amount = st.number_input(
        "Loan Amount ($",
        min_value=0,
        value=st.session_state.loan_amount,
        help="The total amount of money borrowed."
    )
with col_loan2:
    st.session_state.annual_interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        value=st.session_state.annual_interest_rate,
        step=0.1,
        help="Annual interest rate of the loan."
    )
with col_loan3:
    st.session_state.loan_term_years = st.number_input(
        "Loan Term (Years)",
        min_value=0,
        value=st.session_state.loan_term_years,
        step=1,
        help="The duration of the loan in years."
    )

# Calculate monthly loan payment and store in session state
st.session_state.monthly_loan_payment = calculate_loan_payment(
    st.session_state.loan_amount,
    st.session_state.annual_interest_rate,
    st.session_state.loan_term_years
)

st.write(f"**Estimated Monthly Loan Payment (P&I):** ${st.session_state.monthly_loan_payment:,.2f}")
