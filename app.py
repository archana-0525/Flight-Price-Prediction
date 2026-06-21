import streamlit as st
import pandas as pd
import pickle
import time
from datetime import date

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Flight Fare Estimator",
    page_icon="✈️",
    layout="wide"
)

# ================================
# LOAD MODEL
# ================================
@st.cache_resource
def load_model():
    with open("flight_price_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

# ================================
# ADVANCED CSS
# ================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #38bdf8 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 3rem;
    max-width: 1100px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
}

[data-testid="stSidebar"] * {
    color: white;
}

.hero {
    background: rgba(255,255,255,0.14);
    backdrop-filter: blur(18px);
    padding: 35px;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    color: white;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 52px;
    font-weight: 900;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 19px;
    color: #dbeafe;
}

.input-card {
    background: rgba(255,255,255,0.95);
    padding: 32px;
    border-radius: 26px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.30);
}

.result-card {
    background: linear-gradient(135deg, #ffffff, #e0f2fe);
    padding: 35px;
    border-radius: 28px;
    text-align: center;
    box-shadow: 0 18px 45px rgba(15,23,42,0.35);
    border: 1px solid #bfdbfe;
    animation: fadeIn 0.8s ease-in-out;
}

.category-badge {
    display: inline-block;
    background: #1d4ed8;
    color: white;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 16px;
}

.price {
    font-size: 58px;
    font-weight: 900;
    color: #075985;
    margin-bottom: 10px;
}

.details {
    font-size: 17px;
    color: #334155;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2563eb, #0ea5e9);
    color: white;
    border-radius: 14px;
    padding: 0.85rem 1.4rem;
    border: none;
    font-size: 17px;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(37,99,235,0.35);
}

.stButton>button:hover {
    background: linear-gradient(135deg, #1d4ed8, #0284c7);
    color: white;
    transform: scale(1.01);
}

.footer {
    text-align: center;
    color: #e0f2fe;
    margin-top: 35px;
    font-size: 14px;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================
st.sidebar.markdown("## ✈️ Fare Estimator")
st.sidebar.markdown("""
Plan your journey with smart fare estimates based on route and travel date.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Required Details")
st.sidebar.markdown("✅ Route ID")
st.sidebar.markdown("✅ Travel Date")

st.sidebar.markdown("---")
st.sidebar.info("Fare estimates are generated from historical route-wise pricing trends.")

# ================================
# HERO SECTION
# ================================
st.markdown("""
<div class="hero">
    <div class="hero-title">✈️ Flight Fare Estimator</div>
    <div class="hero-subtitle">
        Get quick route-wise fare estimates and plan your journey smarter.
    </div>
</div>
""", unsafe_allow_html=True)

# ================================
# INPUT SECTION
# ================================
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    st.subheader("Enter Travel Details")

    route_id = st.number_input(
        "Route ID",
        min_value=0,
        step=1,
        help="Enter the route ID available in the ticket system."
    )

    travel_date = st.date_input(
        "Travel Date",
        value=date.today()
    )

    estimate_btn = st.button("Estimate Fare")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.subheader("Fare Summary")
    st.write("Your estimated fare will appear here after entering route details.")
    st.markdown("• Route-based estimate")
    st.markdown("• Date-aware pricing")
    st.markdown("• Simple and instant result")
    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# PREDICTION
# ================================
if estimate_btn:
    year = travel_date.year
    month = travel_date.month
    day = travel_date.day

    input_data = pd.DataFrame(
        [[route_id, year, month, day]],
        columns=["Route_id", "Year", "Month", "Days"]
    )

    with st.spinner("Finding the best fare estimate..."):
        time.sleep(1)
        prediction = model.predict(input_data)[0]

    if prediction < 500:
        fare_category = "Budget Fare"
    elif prediction < 1000:
        fare_category = "Standard Fare"
    else:
        fare_category = "Premium Fare"

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
        <div class="category-badge">{fare_category}</div>
        <div class="price">₹{prediction:,.2f}</div>
        <div class="details">
            <b>Route ID:</b> {route_id}<br>
            <b>Travel Date:</b> {travel_date}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================
# FOOTER
# ================================
st.markdown("""
<div class="footer">
    © 2026 Flight Fare Estimator | Smart travel price estimation system
</div>
""", unsafe_allow_html=True)
