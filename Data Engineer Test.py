# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#soal Nomor 1
import pandas as pd
import numpy as np
import io
import pandas_profiling
#memanggil data dan menggabungkan data
data1=pd.read_csv("C:/Users/TuF/Downloads/Data Engineer-IDE/Master Data_Data Engineer.csv")
data2=pd.read_csv("C:/Users/TuF/Downloads/Data Engineer-IDE/Scan Record Data.csv")
del data2['Waybill No.']
del data2['Next Location']
del data2['Previous Location']
del data2['Incoming Branch']
del data2['Bagging No.']

data = pd.merge(left=data1, right=data2, how='inner', left_on='Recording Time', right_on='Recording time')
print(data)
#profiling data awal
pandas_profiling.ProfileReport(data)
#DATA CLEANSING
#check kolom missing data
print(data.isnull().any())
#hapus missing data
data=data.dropna()
print(data)
#check Tipe data dan Profiling data akhir
print(data.dtypes)
pandas_profiling.ProfileReport(data)

#SOAL NOMOR 2
#Mengecek data
print(data.info())
#membuat data baru Arrival scan, Delivery Scan, Pick up Scan, dan POD Scan

data['Arrival Scan']= data['Operation Time']
data['Delivery Scan']= data['Recording time']
data['Pickup Scan']= data['Shipping Date']
data['POD Scan']= data['POD Time']
#merubbah ke tipe Datetime
data['Arrival Scan']= pd.to_datetime(data['Arrival Scan'])
data['Delivery Scan']= pd.to_datetime(data['Delivery Scan'])
data['Pickup Scan']= pd.to_datetime(data['Pickup Scan'])
data['POD Scan']= pd.to_datetime(data['POD Scan'])

#buat data terbbaru
master_data=data[['Waybill No.','Origin Branch','POD Branch','Destination','Pickup Scan','Arrival Scan','Delivery Scan','POD Scan']]
print(master_data.set_index(['Waybill No.']))

#SOAL nomor3
#check data
print(data.info())
#buat data baru untuk menghitung rentang waktu yang telah di tentukan
from datetime import time, timedelta as td

master_data['Rentang P-A']= master_data['Pickup Scan']-master_data['Arrival Scan']
master_data['Rentang A-D']= master_data['Delivery Scan']- master_data['Arrival Scan']
master_data['Rentang D-P']= master_data['POD Scan']-master_data['Delivery Scan']
master_data['Rentang P-P']= master_data['POD Scan']-master_data['Pickup Scan']

print(master_data.set_index(['Waybill No.']))

#SOAL NOMOR 4
#Buat data baru untuk menentukan rentang waktu rata2 percabang
import datetime, time

data_CP= master_data.groupby('POD Branch')['Rentang P-P'].mean(numeric_only=False)
data_CP = pd.DataFrame(data_CP)
data_CP['Mean']= data_CP/np.timedelta64(1, 'h')
print(data_CP)


master_data.to_csv('C:/Users/TuF/Downloads/Data Engineer-IDE/Master_data.csv')
data_CP.to_csv('C:/Users/TuF/Downloads/Data Engineer-IDE/Rata-rata Per-Cabang.csv')