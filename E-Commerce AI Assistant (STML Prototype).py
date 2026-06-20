import streamlit as st
from google import genai

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
    ('premium quality', 'premium')
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

            # CONSTRUCTING THE FINAL PROMPT
            final_prompt_complete = (
    f"Act as a world expert shopping assistant. Search for {user_input_value_example} and "
    f"filter the results to only include options that are {extra_parameters_example}.\n\n"
    "CRITICAL LINK RULES:\n"
    "1. Use the live Google Search tool results to find actual active URLs for these products.\n"
    "2. Format all product recommendations inside a clean Markdown table.\n"
    "3. If a product link is from Amazon, append '?tag=YOUR_AMAZON_TAG' to the end of the URL.\n"
    "4. For ANY OTHER store website (e.g., Walmart, eBay, etc.), you must wrap the URL in my universal affiliate redirect link. "
    "To do this, take the real product URL you found and paste it directly onto the end of this base string: "
    "https://pjatr.com/i/YOUR_NETWORK_ID/?url=\n"
    "Example final format: [Product Name](https://pjatr.com/i/YOUR_NETWORK_ID/?url=https://www.walmart.com/ip/12345)\n"
    "5. Do not invent links; if a link is not directly found in the search tools, do not display it."
)

           
          try:
                response = client.models.generate_content(model='gemini-2.5-flash', contents=final_prompt, config={'tools' : [{'google_search' : {}}] } )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
