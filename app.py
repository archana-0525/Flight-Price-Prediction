import streamlit as st
import pandas as pd
import pickle
from datetime import date

st.set_page_config(
    page_title="Flight Price Prediction",
    page_icon="✈️",
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #1f2937;
}
.subtitle {
    font-size: 17px;
    color: #4b5563;
}
.price-card {
    background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #bae6fd;
    text-align: center;
}
.price {
    font-size: 38px;
    font-weight: 800;
    color: #0369a1;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    border: none;
}
.stButton>button:hover {
    background-color: #1d4ed8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    with open("flight_price_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

# ---------- SIDEBAR ----------
st.sidebar.title("✈️ Flight Predictor")
st.sidebar.write("""
This app predicts the average flight ticket price using Machine Learning.

**Inputs Required:**
- Route ID
- Travel Date
""")

st.sidebar.info("Model trained on historical route-wise flight price data.")

# ---------- SESSION HISTORY ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- MAIN UI ----------
st.markdown('<div class="main-title">✈️ Flight Price Prediction App</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Predict average flight ticket price based on route ID and travel date.</p>',
    unsafe_allow_html=True
)

st.divider()

route_id = st.number_input(
    "Enter Route ID",
    min_value=0,
    step=1,
    help="Enter the route ID available in the dataset/ticket system."
)

travel_date = st.date_input(
    "Select Travel Date",
    value=date.today()
)

year = travel_date.year
month = travel_date.month
day = travel_date.day

if st.button("Predict Flight Price"):
    input_data = pd.DataFrame(
        [[route_id, year, month, day]],
        columns=["Route_id", "Year", "Month", "Days"]
    )

    prediction = model.predict(input_data)[0]

    st.markdown(f"""
    <div class="price-card">
        <h3>Predicted Flight Price</h3>
        <div class="price">₹{prediction:,.2f}</div>
        <p>Route ID: {route_id} | Travel Date: {travel_date}</p>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.history.append({
        "Route ID": route_id,
        "Travel Date": travel_date,
        "Predicted Price": round(prediction, 2)
    })

st.divider()

# ---------- HISTORY ----------
if st.session_state.history:
    st.subheader("📊 Prediction History")

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

    csv = history_df.to_csv(index=False)

    st.download_button(
        label="Download Prediction History",
        data=csv,
        file_name="flight_price_predictions.csv",
        mime="text/csv"
    )

# ---------- FOOTER ----------
st.caption("Developed using Python, Scikit-learn, XGBoost, Pickle and Streamlit.")
