import streamlit as st

st.set_page_config(
    page_title="Holding Costs",
    page_icon="🗓️",
    layout="wide"
)

st.title("Holding Costs (During Rehab/Vacant Period)")

col_hold1, col_hold2 = st.columns(2)
with col_hold1:
    st.session_state.months_holding = st.number_input(
        "Months Holding Property (during rehab/vacancy)",
        min_value=0,
        value=st.session_state.months_holding,
        help="Number of months you expect to hold the property during renovation or vacancy before it generates income."
    )
    st.session_state.annual_property_taxes = st.number_input(
        "Annual Property Taxes ($",
        min_value=0,
        value=st.session_state.annual_property_taxes,
        help="Estimated annual property tax."
    )
with col_hold2:
    st.session_state.annual_property_insurance = st.number_input(
        "Annual Property Insurance ($",
        min_value=0,
        value=st.session_state.annual_property_insurance,
        help="Estimated annual property insurance."
    )
    st.session_state.monthly_utility_costs = st.number_input(
        "Monthly Utility Costs (during holding) ($",
        min_value=0,
        value=st.session_state.monthly_utility_costs,
        help="Estimated monthly utility costs during the holding period."
    )
