# ✈️ Flight Price Prediction System

## Project Overview

The Flight Price Prediction System is a Machine Learning project that predicts the average flight ticket price based on the Route ID and travel date information.

The project uses historical flight pricing data and multiple regression algorithms to learn pricing patterns and estimate future ticket prices.

A Streamlit web application is developed to allow users to enter route details and obtain instant flight price predictions.



## Objective

To build a Machine Learning model that predicts flight ticket prices using:

- Route ID
- Travel Year
- Travel Month
- Travel Day



## Dataset Information

The dataset contains approximately **5,96,650 flight records** with the following attributes:

| Column Name | Description |
|------------|-------------|
| route_id | Unique route identifier |
| min_start_date | Journey start date |
| min_end_date | Journey end date |
| min_price | Minimum recorded price |
| max_price | Maximum recorded price |
| avg_price | Average flight price (Target Variable) |
| std_dev_price | Price variation |
| create_date | Record creation timestamp |
| update_date | Record update timestamp |

### Target Variable

```text
avg_price
```



## Data Preprocessing

The following preprocessing steps were performed:

- Removed unnecessary columns
- Extracted Year, Month, and Day from travel date
- Converted data types
- Removed outliers using Z-Score technique
- Encoded categorical features where required
- Feature selection and preparation


## Machine Learning Models Used

Multiple regression algorithms were trained and evaluated:

- Linear Regression
- Ridge Regression
- Lasso Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- Extra Trees Regressor
- K-Nearest Neighbors Regressor
- XGBoost Regressor

The best-performing model was selected based on evaluation metrics and saved using Pickle for deployment.


## Evaluation Metrics

The models were evaluated using:

- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score
- Adjusted R² Score
- RMSLE


## Trained Model File

The trained model file (`flight_price_model.pkl`) is not included in this repository due to file size limitations.

To generate the model:

1. Open `flight_price_model.ipynb`
2. Run all notebook cells
3. The notebook will create `flight_price_model.pkl`
4. Run the application:

```bash
streamlit run app.py


## Streamlit Application Features

- User-friendly interface
- Route ID input
- Travel date selection
- Instant flight price prediction
- Fast and interactive UI


## Project Structure

```text
Flight_Price_Prediction/
│
├── app.py
├── flight_price_model.pkl
├── Route_Avg_Prices_12072023.xlsx
├── requirements.txt
├── README.md
└── flight_price_model.ipynb
```


## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Matplotlib
- Seaborn
- Streamlit
- Pickle



## User Inputs

The user provides:

- Route ID
- Travel Date

The application automatically extracts:

- Year
- Month
- Day

and predicts the estimated flight ticket price.


## Future Enhancements

- Source and Destination City Mapping
- Airline-Based Prediction
- Flight Class Selection
- Real-Time Flight Data Integration
- Deployment on Streamlit Cloud


⭐ If you found this project useful, feel free to star the repository.
