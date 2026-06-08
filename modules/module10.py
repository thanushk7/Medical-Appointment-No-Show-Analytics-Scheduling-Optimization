import pandas as pd
import os

path = os.getcwd()

risk_path = os.path.join(path, "risk_analysis")
simulation_path = os.path.join(path, "simulation")

df = pd.read_csv(os.path.join(risk_path, "appointments_with_risk.csv"))
sim = pd.read_csv(os.path.join(simulation_path, "overbooking_simulation.csv"))

df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'])

df['Hour'] = df['Appointment_Date'].dt.hour
df['Weekday'] = df['Appointment_Date'].dt.day_name()
df['Month'] = df['Appointment_Date'].dt.month

high_risk_slots = df[df['Risk_Score'] > 0.6]

peak_hours = high_risk_slots.groupby('Hour').size().reset_index(name='High_Risk_Count')
peak_weekdays = high_risk_slots.groupby('Weekday').size().reset_index(name='High_Risk_Count')

high_risk_patients = df.groupby('Patient_ID')['Risk_Score'].mean().reset_index()
high_risk_patients = high_risk_patients.sort_values(by='Risk_Score', ascending=False).head(20)

idle_before = sim['Idle_Time_No_Overbooking'].mean()
idle_after = sim['Idle_Time_With_Overbooking'].mean()

waiting_impact = sim['Waiting_Time_Impact'].mean()

impact_df = pd.DataFrame({
    "Metric": [
        "Idle Time Before Overbooking",
        "Idle Time After Overbooking",
        "Waiting Time Impact"
    ],
    "Value": [
        idle_before,
        idle_after,
        waiting_impact
    ]
})

recommendations = pd.DataFrame({
    "Recommendation": [
        "Apply overbooking for high-risk slots",
        "Send SMS/Email reminders to high-risk patients",
        "Implement dynamic scheduling based on risk score",
        "Allocate flexible slots for high-risk patients"
    ]
})

output_path = os.path.join(path, "executive_report")
os.makedirs(output_path, exist_ok=True)

peak_hours.to_csv(os.path.join(output_path, "peak_hours_risk.csv"), index=False)
peak_weekdays.to_csv(os.path.join(output_path, "peak_weekdays_risk.csv"), index=False)
high_risk_patients.to_csv(os.path.join(output_path, "high_risk_patients.csv"), index=False)
impact_df.to_csv(os.path.join(output_path, "business_impact.csv"), index=False)
recommendations.to_csv(os.path.join(output_path, "recommendations.csv"), index=False)

