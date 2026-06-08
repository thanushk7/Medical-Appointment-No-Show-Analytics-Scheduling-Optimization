import pandas as pd
import os


path = os.getcwd()
clean_path = os.path.join(path, "cleaning")

appointments = pd.read_csv(os.path.join(clean_path, "appointments_cleaned.csv"))
patients = pd.read_csv(os.path.join(clean_path, "patient_logs_cleaned.csv"))


appointments['Appointment_Date'] = pd.to_datetime(appointments['Appointment_Date'])

time_dim = appointments[['Appointment_Date']].drop_duplicates().copy()

time_dim['Time_ID'] = range(1, len(time_dim) + 1)
time_dim['Day'] = time_dim['Appointment_Date'].dt.day
time_dim['Month'] = time_dim['Appointment_Date'].dt.month
time_dim['Weekday'] = time_dim['Appointment_Date'].dt.day_name()

time_dim.rename(columns={'Appointment_Date': 'Date'}, inplace=True)

doctor_dim = appointments[['Doctor_ID']].drop_duplicates().copy()

specialties = ['Cardiology', 'Dermatology', 'Neurology', 'Orthopedics', 'General']

doctor_dim['Specialty'] = [specialties[i % len(specialties)] for i in range(len(doctor_dim))]


fact = appointments.merge(
    time_dim,
    left_on='Appointment_Date',
    right_on='Date',
    how='left'
)

fact_table = fact[[
    'Patient_ID',
    'Doctor_ID',
    'Time_ID',
    'Status'
]].copy()

fact_table['Appointment_ID'] = range(1, len(fact_table) + 1)

fact_table = fact_table[
    ['Appointment_ID', 'Patient_ID', 'Doctor_ID', 'Time_ID', 'Status']
]


warehouse_path = os.path.join(path, "warehouse")
os.makedirs(warehouse_path, exist_ok=True)

fact_table.to_csv(os.path.join(warehouse_path, "fact_appointments.csv"), index=False)
doctor_dim.to_csv(os.path.join(warehouse_path, "dim_doctor.csv"), index=False)
time_dim.to_csv(os.path.join(warehouse_path, "dim_time.csv"), index=False)