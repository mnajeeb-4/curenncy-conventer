import streamlit as st
import requests

def get_exchange_rates(api_key, from_currency):
    """
    Fetches live exchange rates from the API.
    Returns a dictionary of rates with 'from_currency' as the base.
    """
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            if data.get("result") == "success":
                return data.get("conversion_rates") 
            else:
                st.error(f"API Error: {data.get('error-type')}")
                return None
        else:
            st.error("Could not connect to the exchange rate service.")
            return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Streamlit Web Interface Setup ---
st.set_page_config(page_title="Live Currency Converter", page_icon="🌐", layout="centered")

# --- CUSTOM LIQUID GLASS CSS INJECTION WITH HIGH CONTRAST INPUT FIELDS ---
st.markdown("""
    <style>
    /* 1. Liquid moving gradient background for the entire app */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #3b0764, #030712);
        background-size: 400% 400%;
        animation: liquidGradient 15s ease infinite;
        color: #ffffff !important;
    }
    
    @keyframes liquidGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Style Main Text & Headers to be clean and bright */
    h1, h2, h3, p, label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* 3. HIGH VISIBILITY Glassmorphism effect for Input Fields */
    /* Target inputs, wrappers, and active text blocks */
    .stTextInput input, .stNumberInput input, div[data-baseweb="input"] input {
        background-color: rgba(15, 23, 42, 0.6) !important; /* Solid dark tint for contrast */
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important; /* Thick white border */
        border-radius: 12px !important;
        color: #ffffff !important; /* Pure white input text color */
        font-size: 16px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4) !important;
        -webkit-text-fill-color: #ffffff !important; /* Fixes safari/chrome visibility overrides */
    }
    
    /* Input hover and active focus states */
    .stTextInput input:focus, .stNumberInput input:focus, div[data-baseweb="input"]:focus-within {
        border: 2px solid #a855f7 !important; /* Bright purple border when clicking */
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* Fix labels color above the inputs */
    div[data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* 4. Sleek style for the Convert Button */
    div.stButton > button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05)) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
        margin-top: 10px;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.35), rgba(255,255,255,0.1)) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px);
    }

    /* 5. Glassmorphic container wrapper for metrics/results */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# UI Layout Headers
st.title("🌐 Live Currency Converter")
st.write("Convert amounts instantly using dynamic global exchange rates inside a high-contrast workspace.")
st.markdown("<br>", unsafe_allow_html=True)

# API key from assignment
api_key = "cdc20596f4099cac2454f35a"

# Step 1: Web UI Layout for User Input
col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Amount to convert:", min_value=0.0, value=100.0, step=1.0)

with col2:
    from_currency = st.text_input("From (e.g., USD):", value="USD").strip().upper()

with col3:
    to_currency = st.text_input("To (e.g., PKR):", value="PKR").strip().upper()

st.markdown("<br>", unsafe_allow_html=True) # Space

# Step 2: Trigger Conversion on Button Click
if st.button("Convert Currency", type="primary", use_container_width=True):
    if not from_currency or not to_currency:
        st.warning("Please fill in both currency boxes.")
    else:
        # Visual loading spinner while API fetches data
        with st.spinner("Fetching latest live exchange rates..."):
            exchange_rates = get_exchange_rates(api_key, from_currency)
        
        # Step 3: Calculation & Output display
        if exchange_rates:
            if to_currency in exchange_rates:
                exchange_rate = exchange_rates[to_currency]
                converted_amount = amount * exchange_rate
                
                st.markdown("### ✅ Conversion Successful")
                
                # Displays the metric wrapped inside our glass container styled above
                st.metric(
                    label=f"Total in {to_currency}", 
                    value=f"{converted_amount:,.2f} {to_currency}"
                )
                
                st.info(f"📊 **Exchange Rate Info:** 1 {from_currency} = {exchange_rate:,} {to_currency}")
            else:
                st.error(f"The currency code '{to_currency}' was not found in the live database.")
