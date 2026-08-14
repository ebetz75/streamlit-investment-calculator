import streamlit as st
import sys
sys.path.append('..') # Add parent directory to path to import utils
from utils import REHAB_TIERS

st.set_page_config(
    page_title="Property Details",
    page_icon="🏠",
    layout="wide"
)

st.title("Property Details & Acquisition")

col_prop1, col_prop2 = st.columns(2)
with col_prop1:
    st.session_state.purchase_price = st.number_input(
        "Purchase Price ($",
        min_value=0,
        value=st.session_state.purchase_price,
        help="The price you are paying for the property."
    )
    st.session_state.sqft = st.number_input(
        "Square Footage (sqft)",
        min_value=0,
        value=st.session_state.sqft,
        help="The total square footage of the property."
    )
with col_prop2:
    st.session_state.arv = st.number_input(
        "After Repair Value (ARV) ($",
        min_value=0,
        value=st.session_state.arv,
        help="The estimated value of the property after all renovations are complete."
    )
    st.session_state.rehab_tier_selection = st.selectbox(
        "Rehab Tier",
        list(REHAB_TIERS.keys()),
        index=list(REHAB_TIERS.keys()).index(st.session_state.rehab_tier_selection) if st.session_state.rehab_tier_selection in REHAB_TIERS else 0,
        help="Select the level of renovation needed. Each tier has an estimated cost per square foot."
    )
