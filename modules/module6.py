import pandas as pd
import os

path = os.getcwd()
clean_path = os.path.join(path, "cleaning")

appointments = pd.read_csv(os.path.join(clean_path, "appointments_cleaned.csv"))
patients = pd.read_csv(os.path.join(clean_path, "patient_logs_cleaned.csv"))

appointments['Appointment_Date'] = pd.to_datetime(appointments['Appointment_Date'])

appointments['Hour'] = appointments['Appointment_Date'].dt.hour
appointments['Weekday'] = appointments['Appointment_Date'].dt.dayofweek

df = appointments.merge(patients, on='Patient_ID', how='left')

df['Past_Visits'] = df['Past_Visits'].fillna(0)
df['No_Show_History'] = df['No_Show_History'].fillna(0)

df['History_Risk'] = df['No_Show_History'] / (df['Past_Visits'] + 1)

def time_risk(hour):
    if 9 <= hour <= 11:
        return 0.2   
    elif 12 <= hour <= 16:
        return 0.5   
    else:
        return 0.7   

df['Time_Risk'] = df['Hour'].apply(time_risk)
 
 
def weekday_risk(day):
    if day in [0, 1, 2]:   
        return 0.3
    elif day in [3, 4]:    
        return 0.5
    else:                  
        return 0.7

df['Weekday_Risk'] = df['Weekday'].apply(weekday_risk)



df['Risk_Score'] = (
    0.5 * df['History_Risk'] +
    0.3 * df['Time_Risk'] +
    0.2 * df['Weekday_Risk']
)

df['Risk_Score'] = df['Risk_Score'].clip(0, 1)


slot_risk = df.groupby(['Hour', 'Weekday'])['Risk_Score'].mean().reset_index()

slot_risk.rename(columns={'Risk_Score': 'Avg_Risk_Score'}, inplace=True)


output_path = os.path.join(path, "risk_analysis")
os.makedirs(output_path, exist_ok=True)

df.to_csv(os.path.join(output_path, "appointments_with_risk.csv"), index=False)
slot_risk.to_csv(os.path.join(output_path, "time_slot_risk.csv"), index=False)