import pandas as pd
import os

path = os.getcwd()

raw_path = os.path.join(path, "datas", "raw")
clean_path = os.path.join(path, "cleaning")
warehouse_path = os.path.join(path, "warehouse")

os.makedirs(clean_path, exist_ok=True)
os.makedirs(warehouse_path, exist_ok=True)


appointments = pd.read_csv(os.path.join(raw_path, "appointments_data.csv"))
patients = pd.read_csv(os.path.join(raw_path, "patient_logs.csv"))

appointments['Appointment_Date'] = pd.to_datetime(appointments['Appointment_Date'], errors='coerce')
appointments['Booking_Date'] = pd.to_datetime(appointments['Booking_Date'], errors='coerce')

appointments['Status'] = appointments['Status'].str.strip().str.title()

appointments = appointments.dropna(subset=['Patient_ID', 'Appointment_Date', 'Doctor_ID'])
appointments['Status'] = appointments['Status'].fillna('Unknown')

appointments = appointments[appointments['Booking_Date'] <= appointments['Appointment_Date']]

appointments = appointments.sort_values(by='Booking_Date', ascending=False)

appointments = appointments.drop_duplicates(
    subset=['Patient_ID', 'Appointment_Date', 'Doctor_ID'],
    keep='first'
)

appointments.to_csv(os.path.join(clean_path, "appointments_cleaned.csv"), index=False)


patients = patients.dropna(subset=['Patient_ID'])

patients['Age'] = patients['Age'].fillna(patients['Age'].median())
patients['Gender'] = patients['Gender'].fillna('Unknown')

patients['Gender'] = patients['Gender'].str.strip().str.title()

patients = patients[(patients['Age'] >= 0) & (patients['Age'] <= 100)]

patients = patients.drop_duplicates(subset=['Patient_ID'], keep='last')

patients.to_csv(os.path.join(clean_path, "patient_logs_cleaned.csv"), index=False)

appointments['No_Show_Flag'] = appointments['Status'].apply(
    lambda x: 1 if x == 'No-Show' else 0
)

time_dim = appointments[['Appointment_Date']].drop_duplicates().copy()

time_dim['Time_ID'] = range(1, len(time_dim) + 1)
time_dim['Day'] = time_dim['Appointment_Date'].dt.day
time_dim['Month'] = time_dim['Appointment_Date'].dt.month
time_dim['Weekday'] = time_dim['Appointment_Date'].dt.day_name()

time_dim.rename(columns={'Appointment_Date': 'Date'}, inplace=True)


doctor_dim = appointments[['Doctor_ID']].drop_duplicates().copy()
doctor_dim['Specialty'] = 'General'


fact = appointments.merge(
    time_dim,
    left_on='Appointment_Date',
    right_on='Date',
    how='left'
)

fact_table = fact[['Patient_ID', 'Doctor_ID', 'Time_ID', 'Status', 'No_Show_Flag']].copy()

fact_table['Appointment_ID'] = range(1, len(fact_table) + 1)

fact_table = fact_table[
    ['Appointment_ID', 'Patient_ID', 'Doctor_ID', 'Time_ID', 'Status', 'No_Show_Flag']
]


time_dim.to_csv(os.path.join(warehouse_path, "dim_time.csv"), index=False)
doctor_dim.to_csv(os.path.join(warehouse_path, "dim_doctor.csv"), index=False)
fact_table.to_csv(os.path.join(warehouse_path, "fact_appointments.csv"), index=False)