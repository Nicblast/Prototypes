import streamlit as st
from google import genai

col1, col2 = st.columns([1, 6])

# vertical alignment
col1, col2 = st.columns([1, 6], vertical_alignment="center")

with col1:
    st.image("Otis.ai.logo.png.png", width=70)

with col2:
    st.title("Otis AI")
    st.markdown("**Your E-commerce Assistant**")
    st.caption("Search with AI powered filters!")

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
           f"""Act as a world expert shopping assistant. Search for '{user_input_value}' and filter the results to only include options matching these traits: {extra_parameters}.

            CRITICAL OUTPUT RULE: You must respond entirely in the following language: {selected_language}. Translate all table headers, product descriptions, and explanations into this language.

            CRITICAL FORMATTING & LINK RULES:
            1. You MUST find real, active product purchase URLs using the live Google Search tool results.
            2. Present your recommendations in a clean Markdown table with exactly four columns: Product Name | Image | Price & Store | Why It Matches

            3. PRODUCT NAME COLUMN RULE:
            Inside the 'Product Name' column, create a clickable markdown link using the real store URL. 
            - If the URL is from Amazon, append '?tag=YOUR_AMAZON_TAG' to the end.
            - If the URL is from ANY OTHER website, wrap it exactly like this: https://pjatr.com/i/YOUR_NETWORK_ID/?url=REAL_URL
            Example format: [Product Name](https://pjatr.com/i/YOUR_NETWORK_ID/?url=REAL_URL)

            4. IMAGE COLUMN RULE:
            Inside the 'Image' column, provide the direct image asset URL found in the search results.
            - DO NOT wrap this image URL in the pjatr link structure.
            - DO NOT append any affiliate tags to this URL.
            - Use standard markdown image syntax: ![Product](image_url)
            - If no direct image asset URL is found in the search text, you MUST use this exact placeholder link: https://raw.githubusercontent.com/Nicblast/Prototypes/main/Otis.ai.logo.png

            5. STRICT ENFORCEMENT: Do not invent or hallucinate any links. If a real purchase link cannot be found in the search tool, do not guess it. """
        )

            
        try:
            response_stream = client.models.generate_content_stream(model='gemini-2.5-flash', contents=final_prompt, config={'tools' : [{'google_search' : {}}] } )
            st.write_stream(chunk.text for chunk in response_stream)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
