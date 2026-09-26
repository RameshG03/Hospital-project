# 🏥 Hospital Resource Optimization

## 📌 Project Overview

This project focuses on improving operational efficiency in a hospital environment by analyzing patient records, staff schedules, and supply usage data.

The objective is to use data analysis and visualization to support better decisions related to patient wait times, bed utilization, staff allocation, and supply inventory management.

---

## 🎯 Business Problem

The hospital has centralized operational data covering patient records, staff schedules, bed occupancy, and supply usage. However, the lack of proper analysis and actionable insights creates operational challenges such as:

- High patient wait times
- Underutilization or overbooking of beds
- Inconsistent staff deployment
- Unpredictable supply demand
- Increased operational costs

The project aims to transform the available data into useful insights for hospital decision-making.

---

## 📂 Dataset

This project uses three datasets:

- **Patients Dataset**
- **Staff Dataset**
- **Supply Dataset**

The datasets were cleaned, analyzed, and prepared for SQL integration and visualization.

---

## 🧠 Python Analysis

Python was used for data preprocessing, exploratory data analysis, statistical analysis, and visualization.

### 🔹 Data Preprocessing

- Loaded `patients.csv`, `staff.csv`, and `supply.csv`
- Checked data types and missing values
- Converted date and time columns into appropriate formats
- Converted categorical columns such as gender, severity, diagnosis, department, shift, and supply type
- Handled missing values using dropping, median imputation, mode imputation, and default values where appropriate
- Removed duplicate records
- Applied outlier treatment using the IQR method
- Encoded gender numerically for analysis

### 🔹 Exploratory Data Analysis (EDA)

The project calculated descriptive statistics including:

- Mean
- Median
- Mode
- Range
- Variance
- Standard Deviation
- Skewness
- Kurtosis

### 🔹 Visualization

Python visualizations included:

- Histogram
- Boxplot
- Q-Q Plot

The analysis focused particularly on patient `wait_time_min`, `bed_id`, and staff shift-related data.

---

## 🗄️ SQL Analysis

MySQL was used for database storage, data cleaning, statistical analysis, and preprocessing.

### 🔹 Data Cleaning

- Checked for duplicate records
- Removed duplicates using temporary tables and `DISTINCT`
- Checked missing values using `CASE WHEN ... IS NULL`
- Performed type casting
- Created dummy variables using `CASE`
- Applied Min-Max normalization to selected numeric fields

### 🔹 Statistical Analysis

SQL queries were used to calculate:

- Mean
- Median
- Mode
- Variance
- Standard Deviation
- Range
- Skewness
- Kurtosis

### 🔹 Outlier Analysis

The IQR method was used to identify potential outliers in:

- Patient age
- Patient wait time
- Bed ID
- Supply used units
- Inventory level

---

## 📊 Power BI Dashboard

The cleaned hospital data was prepared for data visualization and dashboard-based analysis.

The project focuses on visualizing and understanding:

- Patient wait-time patterns
- Bed utilization
- Staff allocation and shift information
- Supply consumption
- Inventory patterns

The Power BI component supports decision-making by converting analyzed hospital data into visual insights.

---

## 🧰 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- MySQL
- SQLAlchemy
- PyMySQL
- Power BI

---

## 🔑 Key Insights

The project analysis identified several operational areas that can support hospital management decisions:

- Patient wait-time analysis can help identify periods with higher delays.
- Bed utilization analysis can highlight underused areas and support better space management.
- Staff shift analysis can help identify staffing gaps and support resource planning.
- Supply usage patterns can support better inventory management and reduce waste.
- Statistical analysis and outlier treatment improve the reliability of the cleaned dataset.
- Data-driven analysis can support better resource allocation and operational planning.

---

## 🏗️ Project Architecture

**Data Collection → MySQL Database → EDA & Data Cleansing → Python EDA & Preprocessing → Visualization → Decision Making**

The project architecture combines data collection, database storage, Python-based preprocessing and analysis, and visualization to generate insights for hospital operations.

---

## 🔄 Project Pipeline

```text
Hospital Datasets
      ↓
Data Collection
      ↓
Load Data into MySQL
      ↓
Data Cleaning & EDA
      ↓
Python Preprocessing & Statistical Analysis
      ↓
SQL Analysis
      ↓
Power BI Visualization
      ↓
Hospital Decision Making
```

---

## 📋 Data Preparation Workflow

1. Load hospital datasets
2. Inspect structure and missing values
3. Convert data types
4. Handle missing values
5. Remove duplicate records
6. Perform descriptive statistical analysis
7. Detect and treat outliers
8. Load cleaned data into MySQL
9. Perform SQL-based analysis
10. Prepare data for visualization
11. Generate business insights for decision-making

---

## 📌 Business Applications

The insights from this project can support hospital administrators in:

- Improving patient flow
- Reducing patient delays
- Managing bed utilization
- Planning staff deployment
- Monitoring supply consumption
- Improving inventory planning
- Supporting operational cost management

---

## 📁 Project Files

```text
Hospital Resource Optimization/
│
├── Dataset/
│   ├── patients.csv
│   ├── staff.csv
│   └── supply.csv
│
├── python file.py
├── sql file.sql
├── power bi tool.pbix
├── FINAL POWER BI PRESENTATION.pptx
└── README.md
```

---

## 📌 Tags

Hospital Analytics | Data Analytics | Python | Pandas | NumPy | SQL | MySQL | Power BI | EDA | Data Cleaning | Data Visualization
