import pandas as pd
import os

path = os.getcwd()

risk_path = os.path.join(path, "risk_analysis")

df = pd.read_csv(os.path.join(risk_path, "appointments_with_risk.csv"))

df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'])

df['Allow_Overbooking'] = df['Risk_Score'] > 0.6


df['Extra_Booking'] = df['Allow_Overbooking'].apply(lambda x: 1 if x else 0)


df['Show_Prob'] = 1 - df['Risk_Score']

df['Expected_Show'] = df['Show_Prob']

df['Expected_Extra_Show'] = df['Extra_Booking'] * df['Show_Prob']

df['Total_Expected'] = df['Expected_Show'] + df['Expected_Extra_Show']

df['Idle_Time_No_Overbooking'] = 1 - df['Expected_Show']

df['Idle_Time_With_Overbooking'] = 1 - df['Total_Expected']

df['Waiting_Time_Impact'] = df['Total_Expected'] - 1

df['Waiting_Time_Impact'] = df['Waiting_Time_Impact'].apply(
    lambda x: x if x > 0 else 0
)

slot_analysis = df.groupby(['Doctor_ID']).agg({
    'Idle_Time_No_Overbooking': 'mean',
    'Idle_Time_With_Overbooking': 'mean',
    'Waiting_Time_Impact': 'mean'
}).reset_index()

output_path = os.path.join(path, "simulation")
os.makedirs(output_path, exist_ok=True)

df.to_csv(os.path.join(output_path, "overbooking_simulation.csv"), index=False)
slot_analysis.to_csv(os.path.join(output_path, "doctor_performance.csv"), index=False)