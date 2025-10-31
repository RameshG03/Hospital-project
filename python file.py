# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 17:49:58 2025

@author: gkart
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import warnings
warnings.filterwarnings("ignore")

# Load Data
patients_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\patients.csv")
staff_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\staff.csv")
supply_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\supply.csv")

#  Initial EDA
patients_df.info()
patients_df.describe()
patients_df.isnull().sum()

staff_df.info()
staff_df.describe()
staff_df.isnull().sum()

supply_df.info()
supply_df.describe()
supply_df.isnull().sum()

# data type
patients_df.dtypes
staff_df.dtypes
supply_df.dtypes

#  Convert Dates

patients_df['admission_date'] = pd.to_datetime(patients_df['admission_date'], format='%d-%m-%Y',errors='coerce')
patients_df['discharge_time'] = pd.to_datetime(patients_df['discharge_time'], format='%Y-%m-%d', errors='coerce')
patients_df['admission_time'] = pd.to_datetime(patients_df['admission_time'], format='%H:%M:%S', errors='coerce')

patients_df['gender'] = patients_df['gender'].astype('category')
patients_df['severity'] = patients_df['severity'].astype('category')
patients_df['diagnosis'] = patients_df['diagnosis'].astype('category')

staff_df['date'] = pd.to_datetime(staff_df['date'], format='%d-%m-%Y',errors='coerce')
staff_df['department'] =staff_df['department'].astype('category')
staff_df['shift'] = staff_df['shift'].astype('category')

supply_df['date'] = pd.to_datetime(supply_df['date'], format='%Y-%m-%d', errors='coerce')
supply_df['supply_type'] =supply_df['supply_type'].astype('category')
                                                        
# after change data type

patients_df.dtypes
staff_df.dtypes
supply_df.dtypes

# Drop rows with critical nulls for actual columns

patients_df.dropna(subset=['age', 'wait_time_min', 'patient_id'], inplace=True)
staff_df['shift'] = staff_df['shift'].fillna(staff_df['shift'].mode()[0])
supply_df['inventory_level'] = supply_df['inventory_level'].fillna(supply_df['inventory_level'].mode()[0])

# Impute missing numeric columns with median

patients_df.fillna(patients_df.median(numeric_only=True), inplace=True)
staff_df.fillna(staff_df.median(numeric_only=True), inplace=True)
supply_df.fillna(supply_df.median(numeric_only=True), inplace=True)

# Remove duplicate rows

patients_df.drop_duplicates(inplace=True)
staff_df.drop_duplicates(inplace=True)
supply_df.drop_duplicates(inplace=True)

# Final check

print("patients:",patients_df.shape)
print("staff:", staff_df.shape)
print("supply:",supply_df.shape)

# Replace missing values in 'bed_id' with 0, and 'diagnosis' with 'Unknown'

patients_df['bed_id'].fillna(0, inplace=True)
patients_df['diagnosis'] = patients_df['diagnosis'].astype('object').fillna('Unknown').astype('category')
patients_df['discharge_time'].fillna('Missing', inplace=True) 

# Replace missing values in 'shift' with 'Unknown' and 'department' with 'Unassigned'
 
staff_df['department'] = staff_df['department'].astype('object').fillna('Unassigned').astype('category')


# Replace missing values in 'used_units' with 0

supply_df['used_units'].fillna(0, inplace=True)

print("patients:", patients_df.shape)
print("staff:", staff_df.shape)
print("supply:", supply_df.shape)

#  Function to determine the scale of measurement
def determine_scale_of_measurement(series):
    if pd.api.types.is_bool_dtype(series):
        return 'Nominal'
    elif series.dtype == 'object' or series.dtype.name == 'category':
        if series.nunique() < 10:
            return 'Ordinal'   # Ex: Shift: Morning, Evening, Night
        else:
            return 'Nominal'   # Ex: Gender, Diagnosis
    elif pd.api.types.is_numeric_dtype(series):
        if (series.min() >= 0) and (series.dropna() % 1 == 0).all():
            return 'Ratio'     # Ex: Age, Bed ID, Used Units
        else:
            return 'Interval'  # Ex: Scores without true zero
    else:
        return 'Unknown'

#  Function to create data dictionary for one table
def create_data_dictionary(df, table_name):
    return pd.DataFrame({
        'Table': table_name,
        'Column Name': df.columns,
        'Data Type': [df[col].dtype for col in df.columns],
        'Scale of Measurement': [determine_scale_of_measurement(df[col]) for col in df.columns]
    })

#  Create dictionary for each table
dict_patients = create_data_dictionary(patients_df, 'patients')
dict_staff    = create_data_dictionary(staff_df, 'staff')
dict_supply   = create_data_dictionary(supply_df, 'supply')

#  Combine into one final dictionary
final_dict = pd.concat([dict_patients, dict_staff, dict_supply], ignore_index=True)

#  Display or export
print(final_dict)

# calculate mean values for all numeric columns:

patients_mean = patients_df.mean(numeric_only=True)
staff_mean = staff_df.mean(numeric_only=True)
supply_mean= supply_df.mean(numeric_only=True)

patients_mean
staff_mean
supply_mean

# calculate median values for all numeric columns:

patients_median = patients_df.median(numeric_only=True)
staff_median = staff_df.median(numeric_only=True)
supply_median = supply_df.median(numeric_only=True)

patients_median
staff_median
supply_median

# calculate mode values for all numeric colums:

patients_mode = patients_df.mode(numeric_only=True)
staff_mode = staff_df.mode(numeric_only=True)
supply_mode = supply_df.mode(numeric_only=True)

patients_mode
staff_mode
supply_mode

# Calculate Range for all numeric columns:

patients_range = patients_df.select_dtypes(include='number').max()
staff_range = staff_df.select_dtypes(include='number').max()
supply_range = supply_df.select_dtypes(include='number').max()

patients_range
staff_range
supply_range

# Calculate variance of all numeric columns

patients_variance = patients_df.select_dtypes(include='number').var()
staff_variance = staff_df.select_dtypes(include='number').var()
supply_variance = supply_df.select_dtypes(include='number').var()

patients_variance
staff_variance
supply_variance

# Calculate standard deviation for all numeric columns:

patients_std = patients_df.std(numeric_only=True)
staff_std = staff_df.std(numeric_only=True)
supply_std = supply_df.std(numeric_only=True)

patients_std
staff_std
supply_std

# Calculate skewness for all numeric columns:

patients_skew = patients_df.skew(numeric_only=True)
staff_skew = staff_df.skew(numeric_only=True)
supply_skew = supply_df.skew(numeric_only=True)

patients_skew
staff_skew
supply_skew

# Calculate kurtosis for all numeric columns:
    
patients_kurtosis = patients_df.kurt(numeric_only=True)
staff_kurtosis = staff_df.kurt(numeric_only=True)
supply_kurtosis = supply_df.kurt(numeric_only=True)

patients_kurtosis
staff_kurtosis
supply_kurtosis

#  Visualizations - PATIENT WAIT TIME
# Histogram plot:
    
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
patients_df['wait_time_min'].hist(bins=20)
plt.title('Histogram - Wait Time min')
plt.show()

# Boxplot:
    
plt.subplot(3, 1,  2)
sns.boxplot(x=patients_df['wait_time_min'])
plt.title('Boxplot - Wait Time min')
plt.show()

# Q-Q plot:
    
plt.subplot(1, 2, 3)
stats.probplot(patients_df['wait_time_min'], dist="norm", plot=plt)
plt.title('Q-Q Plot - Wait Time min')
plt.tight_layout()
plt.show()

# Histogram plot : bed_id

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
patients_df['bed_id'].hist(bins=20)
plt.title('Histogram - bed id')
plt.show()

# box plot : bed_id

plt.subplot(3, 1, 2)
sns.boxplot(x=patients_df['bed_id'])
plt.title('Boxplot - bed id')
plt.show()

# Q-Q plot : bed_id

plt.subplot(1, 3, 3)
stats.probplot(patients_df['bed_id'], dist="norm", plot=plt)
plt.title('Q-Q Plot - bed id')
plt.tight_layout()
plt.show()


# Histogram plot : Staff_id
    
plt.figure(figsize=(13, 4))
plt.subplot(1, 2, 1)
staff_df['shift'].hist(bins=20)
plt.title('Histogram - staff id')
plt.show()

# Box plot : staff_id
plt.subplot(2, 2,  1)
sns.boxplot(x=staff_df['shift'])
plt.title('Boxplot - staff id')
plt.show()

# Fill missing values
patients_df['age'].fillna(patients_df['age'].median(), inplace=True)
patients_df['wait_time_min'].fillna(patients_df['wait_time_min'].median(), inplace=True)
patients_df['gender'].fillna(patients_df['gender'].mode()[0], inplace=True)
patients_df['severity'].fillna(patients_df['severity'].mode()[0], inplace=True)

# Outlier Removal (IQR method) for wait_time_min
Q1 = patients_df['wait_time_min'].quantile(0.25)
Q3 = patients_df['wait_time_min'].quantile(0.75)
IQR = Q3 - Q1
patients_df = patients_df[(patients_df['wait_time_min'] >= Q1 - 1.5*IQR) & (patients_df['wait_time_min'] <= Q3 + 1.5*IQR)]

# Encode gender
patients_df['gender'] = patients_df['gender'].map({'Male': 0, 'Female': 1})

#  Re-EDA After Preprocessing
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
patients_df['wait_time_min'].hist(bins=20)
plt.title('Post-Clean Histogram - Wait Time min')
plt.show()

plt.subplot(3, 2, 2)
sns.boxplot(x=patients_df['wait_time_min'])
plt.title('Post-Clean Boxplot - Wait Time Min')
plt.tight_layout()
plt.show()

------------------------------------------------------------------------------------------------------
# sql

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote

# Load CSV files
patients_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\patients.csv")
staff_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\staff.csv")
supply_df = pd.read_csv(r"C:\DATA ANALYSIS\PROJECT\Dataset\supply.csv")

# Connection details
user = 'user70'
pw = 'user70'
port='3306'
db = 'Hospital'

# Create engine (for SQLAlchemy < 2.x)
encoded_pw = quote(pw)
engine = create_engine(f"mysql+pymysql://{user}:{encoded_pw}@localhost/{db}")

# Save to separate tables
patients_df.to_sql('patients', con=engine, if_exists='replace', index=False)
staff_df.to_sql('staff', con=engine, if_exists='replace', index=False)
supply_df.to_sql('supply', con=engine, if_exists='replace', index=False)

# Read back from MySQL
sql1 = "SELECT * FROM patients"
sql2 = "SELECT * FROM staff"
sql3 = "SELECT * FROM supply"

# Use text() for SQLAlchemy 2.x compatibility
patients_df_sql = pd.read_sql_query(text(sql1), engine.connect())
staff_df_sql = pd.read_sql_query(text(sql2), engine.connect())
supply_df_sql = pd.read_sql_query(text(sql3), engine.connect())
