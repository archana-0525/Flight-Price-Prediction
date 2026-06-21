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
# CUSTOM CSS
# ================================
st.markdown("""
<style>
.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #172554;
}
.subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 25px;
}
.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}
.price-card {
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    padding: 35px;
    border-radius: 22px;
    border: 1px solid #93c5fd;
    text-align: center;
    margin-top: 20px;
}
.price {
    font-size: 46px;
    font-weight: 900;
    color: #075985;
}
.category {
    font-size: 22px;
    font-weight: 700;
    color: #1e3a8a;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 12px;
    padding: 0.7rem 1.4rem;
    border: none;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

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
# SIDEBAR
# ================================
st.sidebar.title("✈️ Flight Fare Estimator")
st.sidebar.write("""
Plan your journey with estimated flight fares based on route and travel date.
""")

st.sidebar.markdown("### Required Details")
st.sidebar.write("• Route ID")
st.sidebar.write("• Travel Date")

st.sidebar.info("Fare estimates are generated from historical route-wise pricing trends.")

# ================================
# SESSION HISTORY
# ================================
if "history" not in st.session_state:
    st.session_state.history = []

# ================================
# MAIN TITLE
# ================================
st.markdown('<div class="main-title">✈️ Flight Fare Estimator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Estimate route-wise flight fares instantly using historical pricing trends.</div>',
    unsafe_allow_html=True
)

# ================================
# INPUT SECTION
# ================================
col1, col2 = st.columns(2)

with col1:
    route_id = st.number_input(
        "Enter Route ID",
        min_value=0,
        step=1,
        help="Enter the route ID available in the ticket system."
    )

with col2:
    travel_date = st.date_input(
        "Select Travel Date",
        value=date.today()
    )

year = travel_date.year
month = travel_date.month
day = travel_date.day

# ================================
# PREDICTION
# ================================
if st.button("Estimate Fare"):
    input_data = pd.DataFrame(
        [[route_id, year, month, day]],
        columns=["Route_id", "Year", "Month", "Days"]
    )

    with st.spinner("Calculating fare estimate..."):
        time.sleep(1)
        prediction = model.predict(input_data)[0]

    if prediction < 500:
        fare_category = "Budget Fare"
    elif prediction < 1000:
        fare_category = "Standard Fare"
    else:
        fare_category = "Premium Fare"

    st.markdown(f"""
    <div class="price-card">
        <div class="category">{fare_category}</div>
        <div class="price">₹{prediction:,.2f}</div>
        <p>Route ID: {route_id} | Travel Date: {travel_date}</p>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.history.append({
        "Route ID": route_id,
        "Travel Date": str(travel_date),
        "Fare Category": fare_category,
        "Estimated Fare": round(prediction, 2)
    })

st.divider()

# ================================
# RECENT SEARCHES
# ================================
if st.session_state.history:
    st.subheader("📌 Recent Fare Searches")

    history_df = pd.DataFrame(st.session_state.history)

    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        <div class="card">
            <b>Route ID:</b> {item["Route ID"]} &nbsp; | &nbsp;
            <b>Date:</b> {item["Travel Date"]} &nbsp; | &nbsp;
            <b>Category:</b> {item["Fare Category"]} &nbsp; | &nbsp;
            <b>Estimated Fare:</b> ₹{item["Estimated Fare"]:,.2f}
        </div>
        <br>
        """, unsafe_allow_html=True)

    st.subheader("📈 Fare Estimate Trend")
    chart_df = history_df[["Estimated Fare"]]
    st.line_chart(chart_df)

    csv = history_df.to_csv(index=False)

    col3, col4 = st.columns(2)

    with col3:
        st.download_button(
            label="Download Fare History",
            data=csv,
            file_name="fare_estimate_history.csv",
            mime="text/csv"
        )

    with col4:
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# ================================
# FOOTER
# ================================
st.caption("© 2026 Flight Fare Estimator | Smart travel price estimation system.")
