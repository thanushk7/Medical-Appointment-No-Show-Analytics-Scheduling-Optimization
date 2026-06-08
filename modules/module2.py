import pandas as pd
import os 


path = os.getcwd()

raw_path = os.path.join(path, "datas", "raw")

appointment = os.path.join(raw_path, "appointments_data.csv")
patient = os.path.join(raw_path, "patient_logs.csv")

df = pd.read_csv(appointment)
pl = pd.read_csv(patient)

df['Appointment_Date'] = pd.to_datetime(df['Appointment_Date'], errors='coerce')
df['Booking_Date'] = pd.to_datetime(df['Booking_Date'], errors='coerce')

df['Status'] = df['Status'].str.strip().str.title()

df = df.dropna(subset=['Patient_ID', 'Appointment_Date', 'Doctor_ID'])

df['Status'] = df['Status'].fillna('Unknown')

df = df[df['Booking_Date'] <= df['Appointment_Date']]

df = df.sort_values(by='Booking_Date', ascending=False)

duplicate_appointments = df[df.duplicated(
    subset=['Patient_ID', 'Appointment_Date', 'Doctor_ID'],
    keep='first'
)]

df_cleaned = df.drop_duplicates(
    subset=['Patient_ID', 'Appointment_Date', 'Doctor_ID'],
    keep='first'
)

pl = pl.dropna(subset=['Patient_ID'])

pl['Age'] = pl['Age'].fillna(pl['Age'].median())
pl['Gender'] = pl['Gender'].fillna('Unknown')

pl['Gender'] = pl['Gender'].str.strip().str.title()

pl = pl[(pl['Age'] >= 0) & (pl['Age'] <= 100)]

pl = pl.drop_duplicates(subset=['Patient_ID'], keep='last')


clean_path = os.path.join(path, "cleaning")

os.makedirs(clean_path, exist_ok=True)

df_cleaned.to_csv(os.path.join(clean_path, "appointments_cleaned.csv"), index=False)
duplicate_appointments.to_csv(os.path.join(clean_path, "duplicate_appointments.csv"), index=False)

pl.to_csv(os.path.join(clean_path, "patient_logs_cleaned.csv"), index=False)