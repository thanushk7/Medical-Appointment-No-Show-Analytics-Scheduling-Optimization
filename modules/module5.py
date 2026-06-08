import pandas as pd
import os

path = os.getcwd()
clean_path = os.path.join(path, "cleaning")

df = pd.read_csv(os.path.join(clean_path, "appointments_cleaned.csv"))

df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'])
df['Booking_Date'] = pd.to_datetime(df['Booking_Date'])



total_appointments = len(df)

no_show_count = (df['Status'] == 'No-Show').sum()

no_show_rate = (no_show_count / total_appointments) * 100


df['Wait_Time_Days'] = (df['Appointment_Date'] - df['Booking_Date']).dt.days

avg_wait_time = df['Wait_Time_Days'].mean()



kpi_df = pd.DataFrame({
    "Metric": ["Total Appointments", "No-show Count", "No-show Rate (%)", "Avg Wait Time (Days)"],
    "Value": [total_appointments, no_show_count, no_show_rate, avg_wait_time]
})

output_path = os.path.join(path, "kpi")
os.makedirs(output_path, exist_ok=True)

kpi_df.to_csv(os.path.join(output_path, "kpi_summary.csv"), index=False)

df.to_csv(os.path.join(output_path, "appointments_with_kpi.csv"), index=False)