import streamlit as st

st.set_page_config(
    page_title="Rental Income & Expenses",
    page_icon="💸",
    layout="wide"
)

st.title("Rental Income & Operating Expenses (Once Rented)")

col_rent1, col_rent2, col_rent3 = st.columns(3)
with col_rent1:
    st.session_state.expected_monthly_rent = st.number_input(
        "Expected Monthly Rent ($",
        min_value=0,
        value=st.session_state.expected_monthly_rent,
        help="The estimated monthly rental income once the property is rented."
    )
    st.session_state.annual_maintenance_repairs = st.number_input(
        "Annual Maintenance & Repairs ($",
        min_value=0,
        value=st.session_state.annual_maintenance_repairs,
        help="Estimated annual cost for ongoing maintenance and repairs."
    )
with col_rent2:
    st.session_state.vacancy_rate = st.slider(
        "Vacancy Rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=st.session_state.vacancy_rate,
        step=0.5,
        help="Percentage of time the property is expected to be vacant."
    )
    st.session_state.annual_capex = st.number_input(
        "Annual Capital Expenditures (CapEx) ($",
        min_value=0,
        value=st.session_state.annual_capex,
        help="Annual budget for major capital improvements or replacements (e.g., roof, HVAC)."
    )
with col_rent3:
    st.session_state.property_management_fees_percentage = st.slider(
        "Property Management Fees (% of Gross Rent)",
        min_value=0.0,
        max_value=15.0,
        value=st.session_state.property_management_fees_percentage,
        step=0.5,
        help="Percentage of gross rental income paid to a property manager."
    )
    st.session_state.selling_costs_percentage = st.slider(
        "Selling Costs (% of ARV)",
        min_value=0.0,
        max_value=10.0,
        value=st.session_state.selling_costs_percentage,
        step=0.1,
        help="Percentage of ARV attributed to real estate commissions, closing costs, etc., when selling."
    )
