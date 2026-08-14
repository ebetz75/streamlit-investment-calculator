import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Repair Estimator",
    page_icon="🛠️",
    layout="wide"
)

# Configure Gemini API
try:
    # Use st.secrets for Streamlit Cloud deployment
    GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Attempt to use gemini-pro, if it fails, list available models
    try:
        gemini_model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for general text generation
    except Exception as model_e:
        st.error(f"Failed to load 'gemini-pro' model: {model_e}")
        st.info("Attempting to list available models...")
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if available_models:
            st.write(f"Available models that support 'generateContent': {', '.join(available_models)}")
            st.warning("Please update `gemini-pro` in the code to one of the listed models, e.g., `gemini-1.5-flash-latest`.")
            gemini_model = None # Set to None to prevent further errors
        else:
            st.error("No suitable models found. Please check your API key and region settings.")
            gemini_model = None

except Exception as e:
    st.error(f"Failed to configure Gemini API. Please ensure GOOGLE_API_KEY is set in Streamlit secrets and you have network access: {e}")
    gemini_model = None # Set to None to prevent further errors if API fails

st.title("AI-Powered Repair Estimator")
st.write("Get an estimated repair cost based on geographical location and repair details.")

st.subheader("Property Location")
col_geo1, col_geo2 = st.columns(2)
with col_geo1:
    city = st.text_input("City", help="e.g., San Francisco")
with col_geo2:
    state_zip = st.text_input("State / Zip Code", help="e.g., CA or 90210")

st.subheader("Repair Details")
repair_description = st.text_area(
    "Describe the repair needed (be specific)",
    value="e.g., Full kitchen remodel with new cabinets and countertops",
    height=150,
    help="Provide as much detail as possible about the scope of work."
)

repair_category = st.selectbox(
    "Select Repair Category (for general guidance)",
    ["Structural", "Plumbing", "Electrical", "HVAC", "Roofing", "Interior Finishes", "Exterior", "Landscaping", "Other"],
    help="Categorize the primary type of repair."
)

submit_estimate = st.button("Get AI Estimate")

if submit_estimate:
    st.subheader("AI-Driven Repair Cost Estimate")
    if not gemini_model:
        st.error("Gemini API is not configured or a suitable model could not be loaded. Please check your API key and connection, and consult the available models list above.")
    elif not city or not state_zip or not repair_description:
        st.warning("Please fill in all fields (City, State/Zip Code, and Repair Description) to get an estimate.")
    else:
        prompt = f"""
        As an AI repair cost estimator, provide a cost range for the following repair.
        Location: {city}, {state_zip}
        Repair Category: {repair_category}
        Repair Description: {repair_description}

        Provide the estimate as a cost range (e.g., $X,XXX - $Y,YYY), and include a short explanation of factors influencing the cost. Also, provide a confidence level (Low, Medium, High). Format the output clearly.
        """

        with st.spinner("Generating estimate with Gemini AI..."):
            try:
                response = gemini_model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating estimate from Gemini API: {e}")
                st.warning("It's possible the model is unavailable or your prompt was too complex. Please try again or simplify your request.")
