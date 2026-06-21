import streamlit as st
import pandas as pd
import pickle
import time
from datetime import date

st.set_page_config(
    page_title="Flight Fare Estimator",
    page_icon="✈️",
    layout="centered"
)

@st.cache_resource
def load_model():
    with open("flight_price_model.pkl", "rb") as file:
        return pickle.load(file)

model = load_model()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc, #eef2f7, #e0f2f1);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 3rem;
    max-width: 850px;
}

[data-testid="stSidebar"] {
    background: #f1f5f9;
    border-right: 1px solid #dbe3ea;
}

.hero {
    background: linear-gradient(135deg, #ffffff, #e8f3f1);
    padding: 35px;
    border-radius: 26px;
    border: 1px solid #d1e3e0;
    box-shadow: 0 12px 35px rgba(15,23,42,0.08);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 44px;
    font-weight: 850;
    color: #102a43;
}

.hero-subtitle {
    font-size: 18px;
    color: #52616b;
    margin-top: 10px;
}

.result-card {
    background: linear-gradient(135deg, #ffffff, #edf7f5);
    padding: 35px;
    border-radius: 26px;
    text-align: center;
    box-shadow: 0 12px 35px rgba(15,23,42,0.10);
    border: 1px solid #cfe3df;
    animation: fadeIn 0.7s ease-in-out;
    margin-top: 30px;
}

.category-badge {
    display: inline-block;
    background: #2f6f73;
    color: white;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 14px;
}

.price {
    font-size: 52px;
    font-weight: 900;
    color: #164e63;
    margin-bottom: 12px;
}

.details {
    font-size: 16px;
    color: #475569;
    line-height: 1.8;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #2f6f73, #3b8c88);
    color: white;
    border-radius: 12px;
    padding: 0.8rem 1.3rem;
    border: none;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 8px 20px rgba(47,111,115,0.25);
}

.stButton>button:hover {
    background: linear-gradient(135deg, #285e61, #327c78);
    color: white;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 35px;
    font-size: 14px;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(18px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## ✈️ Fare Estimator")
st.sidebar.markdown("Plan your journey with smart fare estimates based on route and travel date.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Required Details")
st.sidebar.markdown("✅ Route ID")
st.sidebar.markdown("✅ Travel Date")
st.sidebar.info("Fare estimates are generated from historical route-wise pricing trends.")

st.markdown("""
<div class="hero">
    <div class="hero-title">✈️ Flight Fare Estimator</div>
    <div class="hero-subtitle">
        Get quick route-wise fare estimates and plan your journey smarter.
    </div>
</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="footer">
    © 2026 Flight Fare Estimator | Smart travel price estimation system
</div>
""", unsafe_allow_html=True)
