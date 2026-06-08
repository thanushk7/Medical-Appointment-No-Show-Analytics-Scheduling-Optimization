import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np

path = os.getcwd()
clean_path = os.path.join(path, "cleaning")

df = pd.read_csv(os.path.join(clean_path, "appointments_cleaned.csv"))

df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'])

daily_data = df.groupby('Appointment_Date').size().reset_index(name='Total_Appointments')

no_show_series = df[df['Status'] == 'No-Show'].groupby('Appointment_Date').size()
daily_data['No_Show'] = daily_data['Appointment_Date'].map(no_show_series).fillna(0)

daily_data = daily_data.sort_values('Appointment_Date')
daily_data['Day_Index'] = range(len(daily_data))

X = daily_data[['Day_Index']]
y = daily_data['Total_Appointments']

model = LinearRegression()
model.fit(X, y)

future_days = 30

future_index = np.arange(len(daily_data), len(daily_data) + future_days)

future_dates = pd.date_range(
    start=daily_data['Appointment_Date'].max() + pd.Timedelta(days=1),
    periods=future_days
)

future_df = pd.DataFrame({'Day_Index': future_index})

future_predictions = model.predict(future_df)

forecast_df = pd.DataFrame({
    'Date': future_dates,
    'Predicted_Appointments': future_predictions
})

forecast_df['Predicted_Appointments'] = forecast_df['Predicted_Appointments'].clip(0)

output_path = os.path.join(path, "forecasting")
os.makedirs(output_path, exist_ok=True)

daily_data.to_csv(os.path.join(output_path, "historical_daily_data.csv"), index=False)
forecast_df.to_csv(os.path.join(output_path, "appointment_forecast.csv"), index=False)