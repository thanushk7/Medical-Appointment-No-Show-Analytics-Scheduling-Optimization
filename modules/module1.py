import pandas as pd
import os 
path=os.getcwd()
filepath= os.path.join(path,"datas","raw")
appointment=os.path.join(filepath,"appointments_data.csv")
patient=os.path.join(filepath,"patient_logs.csv")

apd=pd.read_csv(appointment)
pl=pd.read_csv(patient)
print("Original Dimension of Appointment Data")
print(apd.shape)
print(apd.tail())
print("Original Dimension of Patient Logs")
print(pl.shape)
print(pl.head())