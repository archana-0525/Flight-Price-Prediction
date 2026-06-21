import streamlit as st
import pickle
import pandas as pd
from datetime import date

# Page config
st.set_page_config(
    page_title="Flight Price Prediction",
    page_icon="✈️",
    layout="centered"
)

# Load trained model
@st.cache_resource
def load_model():
    with open("flight_price_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()

# App title
st.title("✈️ Flight Price Prediction App")
st.write("Enter route ID and travel date details to predict average flight price.")

# User inputs
route_id = st.number_input("Enter Route ID", min_value=0, step=1)

travel_date = st.date_input(
    "Select Travel Date",
    value=date.today()
)

year = travel_date.year
month = travel_date.month
day = travel_date.day

st.write("Selected Date Details:")
st.write(f"Year: {year}, Month: {month}, Day: {day}")

# Prediction button
if st.button("Predict Flight Price"):
    input_data = pd.DataFrame(
        [[route_id, year, month, day]],
        columns=["Route_id", "Year", "Month", "Days"]
    )

    prediction = model.predict(input_data)

    st.success(f"Predicted Flight Price: ₹{prediction[0]:.2f}")
