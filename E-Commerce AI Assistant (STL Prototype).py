import streamlit as st
from google.colab import userdata
from google import genai

st.set_page_config(page_title="AI E-commerce Assistant", layout="centered")
st.title("AI E-commerce Assistant")
st.write("Find the best deals with AI-powered filters!")

# Retrieve API Key (for Colab environment testing, adapt for production Streamlit via st.secrets)
api_key = userdata.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

# 1. FILTER DROPDOWN (Streamlit equivalent)
filter_options = [
    ('value for money', 'vfm'),
    ('fast delivery', 'fd'),
    ('premium quality', 'premium')
]
selected_filter_label = st.selectbox(
    "Filter by:",
    options=[opt[0] for opt in filter_options],
    format_func=lambda x: x
)
# Map selected label back to value for logic
selected_filter_value = [opt[1] for opt in filter_options if opt[0] == selected_filter_label][0]


# 2. SEARCH BAR (Streamlit equivalent)
user_input_value = st.text_input(
    "Search for:",
    placeholder="Let's find you a deal"
)

# 3. ACTION BUTTON (Streamlit equivalent)
if st.button("Search with AI filters", type="primary"):
    if not user_input_value.strip():
        st.warning("Please type a product to search for.")
    else:
        with st.spinner("Analyzing..."):
            extra_parameters = ""

            # CONDITIONAL STATEMENT
            if selected_filter_value == 'vfm':
                extra_parameters = "budget friendly , positive reviews"
            elif selected_filter_value == 'fd':
                extra_parameters = "next day delivery, fast, immediate next-day shipping"
            elif selected_filter_value == 'premium':
                extra_parameters = "luxury, top-tier performance, five-stars reviews, premium build quality"

            # CONSTRUCTING THE FINAL PROMPT
            final_prompt = f"Act as a world expert shopping assistant. Search for {user_input_value} and filter the results to only include options that are {extra_parameters}. Present your reccomandations in a clean markdown table with colums for: Product Name, Price, Why It Fits, and Clickable Purchase Link. For each product recommended, include a brief 'Buying Advisory' sentence that builds a logical reason for fast action. Dynamically tie this urgency to the nature of {user_input_value} (e.g., mention high seasonal demand, fluctuating online price trends, or rapid stock turnover for top-rated items in this category). Remind the user that acting quickly ensures they secure the current pricing and immediate shipping availability"

            try:
                response = client.models.generate_content(model='gemini-2.5-flash', contents=final_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
