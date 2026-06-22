import streamlit as st
from google import genai

col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/otis_logo.png", width=60) # Scaled beautifully next to text
with col2:
    st.title("Otis AI")

st.set_page_config(page_title="AI E-commerce Assistant", layout="centered")
st.title("Otis  -  Your AI E-commerce Assistant")
st.write("Search with AI powered filters!")

# Retrieve API Key via Streamlit Secrets for production
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Missing Gemini API Key. Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# 1. FILTER DROPDOWN
filter_options = [
    ('value for money', 'vfm'),
    ('fast delivery', 'fd'),
    ('premium quality', 'premium'),
    ('something specific', 'sp')
]
selected_filter_label = st.selectbox(
    "Filter by:",
    options=[opt[0] for opt in filter_options],
    format_func=lambda x: x
)
# Map selected label back to value for logic
selected_filter_value = [opt[1] for opt in filter_options if opt[0] == selected_filter_label][0]


# 2. SEARCH BAR
user_input_value = st.text_input(
    "Search for:",
    placeholder="Let's find you a deal"
)

# LANGUAGE SELECTOR WITH CHINESE AND JAPANESE
selected_language = st.selectbox(
    "Choose Language:",
    ["English", "Italiano", "Español", "Français", "Deutsch", "简体中文 (Chinese)", "日本語 (Japanese)"]
)

# 3. ACTION BUTTON
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
            elif selected_filter_value == 'sms':
                extra_parameters = "books, home-appliances, sportswear, tech , gadgets, value-for-money , franchise , marketplace, general"

        
        # CONSTRUCTING THE FINAL PROMPT
        final_prompt = (
            f"Act as a world expert shopping assistant. Search for '{user_input_value}' and "
            f"filter the results to only include options matching these traits: {extra_parameters}.\n\n"
            f"CRITICAL OUTPUT RULE: You must respond entirely in the following language: {selected_language}. "
            "Translate all table headers, product descriptions, and explanations into this language.\n\n"
            "CRITICAL LINK & IMAGE RULES:\n"
            "1. Use the live Google Search tool results to extract real, active purchase URLs.\n"
            "2. If an active product link is from Amazon, append '?tag=YOUR_AMAZON_TAG' to the end of the URL.\n"
            "3. For ANY OTHER store website, wrap the URL like this: https://pjatr.com/i/YOUR_NETWORK_ID/?url=REAL_URL\n"
            "4. From the search results, find a valid image source URL (like a thumbnail) for each product.\n"
            "5. Present your recommendations in a clean Markdown table with these columns (translated to your output language): Product Name | Image | Price & Store | Why It Matches.\n"
            "6. Display the image inside the table using standard Markdown image syntax: ![Product Name](image_url_here)\n"
            "7. The Product Name column must be a working clickable Markdown link containing your modified affiliate URL.\n"
            "8. CRITICAL: Do not invent links or image URLs. If they are not directly found in the search tools, do not display them."
        )

            
        try:
            response_stream = client.models.generate_content_stream(model='gemini-2.5-flash', contents=final_prompt, config={'tools' : [{'google_search' : {}}] } )
            st.write_stream(chunk.text for chunk in response_stream)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
