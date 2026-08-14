import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Repair Estimator",
    page_icon="⚙️",
    layout="wide"
)

# Configure Gemini API
try:
    # Use st.secrets for Streamlit Cloud deployment
    if 'GOOGLE_API_KEY' in st.secrets:
        GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
        genai.configure(api_key=GOOGLE_API_KEY)

        # Using a stable, high-performance model to avoid 404 errors
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("GOOGLE_API_KEY not found in Streamlit Secrets. Please add it to the Secrets tab in the Streamlit Cloud dashboard.")
        gemini_model = None

except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    gemini_model = None

st.title("AI-Powered Repair Estimator")
st.write("Get an estimated repair cost based on location and scope.")

st.subheader("Property Location")
col_geo1, col_geo2 = st.columns(2)
with col_geo1:
    city = st.text_input("City", help="e.g., San Francisco")
with col_geo2:
    state_zip = st.text_input("State / Zip Code", help="e.g., CA or 90210")

st.subheader("Repair Details")
repair_description = st.text_area(
    "Describe the repair needed",
    value="",
    height=150
)

repair_category = st.selectbox(
    "Select Repair Category",
    ["Structural", "Plumbing", "Electrical", "HVAC", "Roofing", "Interior Finishes", "Exterior", "Landscaping", "Other"]
)

if st.button("Get AI Estimate"):
    if not gemini_model:
        st.error("API Key is missing or model failed to initialize. Add 'GOOGLE_API_KEY' to Streamlit Cloud Secrets.")
    elif not city or not state_zip or not repair_description:
        st.warning("Please fill in all fields.")
    else:
        prompt = f"Estimate repair costs for: {repair_description} in {city}, {state_zip}. Category: {repair_category}. Provide a range and explanation."

        with st.spinner("Consulting Gemini AI..."):
            try:
                response = gemini_model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")
