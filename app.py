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

st.title("🌐 Live Currency Converter")
st.write("Convert amounts instantly using live global exchange rates.")
st.markdown("---")

# API key from your assignment
api_key = "cdc20596f4099cac2454f35a"

# Step 1: Web UI Layout for User Input
# We use columns to put input boxes side by side
col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input("Amount to convert:", min_value=0.0, value=100.0, step=1.0)

with col2:
    from_currency = st.text_input("From (e.g., USD):", value="USD").strip().upper()

with col3:
    to_currency = st.text_input("To (e.g., PKR):", value="PKR").strip().upper()

st.markdown("") # Adds a small space

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
                
                # Display results beautifully using clean Streamlit components
                st.success("### ✅ Conversion Successful")
                
                # Displays a big bold financial metric format
                st.metric(
                    label=f"Total in {to_currency}", 
                    value=f"{converted_amount:,.2f} {to_currency}"
                )
                
                st.info(f"📊 **Exchange Rate Info:** 1 {from_currency} = {exchange_rate:,} {to_currency}")
            else:
                st.error(f"The currency code '{to_currency}' was not found in the live database.")
