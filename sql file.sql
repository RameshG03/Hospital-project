create database Hospital_db;
show databases;
use Hospital_db;
describe patients;
select * from patients where age >90;
select * from staff where date ='2025-01-01';
select sum(case when age is null then 1 else 0 end)as age_null from patients;
select sum(case when bed_id is null then 1 else 0 end)from patients;
 -- ============================================
-- Step 1: Duplicate Checks and Removal
-- ============================================
-- Patients Dataset
SELECT patient_id, COUNT(*) AS dup_count
FROM patients
GROUP BY patient_id, admission_date, age, wait_time_min, bed_id
HAVING COUNT(*) > 1;

CREATE TABLE temp_patients AS
SELECT DISTINCT * FROM patients;

TRUNCATE TABLE patients;
INSERT INTO patients SELECT * FROM temp_patients;
DROP TABLE temp_patients;

-- Staff Dataset
SELECT staff_id, COUNT(*) AS dup_count
FROM staff
GROUP BY staff_id, date, shift, department
HAVING COUNT(*) > 1;

CREATE TABLE temp_staff AS
SELECT DISTINCT * FROM staff;

TRUNCATE TABLE staff;
INSERT INTO staff SELECT * FROM temp_staff;
DROP TABLE temp_staff;

-- Step 1: Check for Duplicates

DROP TABLE IF EXISTS temp_supply;

SELECT supply_type, COUNT(*) AS dup_count
FROM supply
GROUP BY date, supply_type, used_units, inventory_level
HAVING COUNT(*) > 1;

-- Step 2: Remove Duplicates using Temporary Table
CREATE TABLE temp_supply AS
SELECT DISTINCT * FROM supply;

TRUNCATE TABLE supply;

INSERT INTO supply
SELECT * FROM temp_supply;

DROP TABLE temp_supply;



SELECT
  SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS missing_age,
  SUM(CASE WHEN wait_time_min IS NULL THEN 1 ELSE 0 END) AS missing_wait_time,
  SUM(CASE WHEN bed_id IS NULL THEN 1 ELSE 0 END) AS missing_bed_id
FROM patients;

SELECT
  SUM(CASE WHEN shift IS NULL THEN 1 ELSE 0 END) AS missing_shift,
  SUM(CASE WHEN department IS NULL THEN 1 ELSE 0 END) AS missing_department
FROM staff;

SELECT
  SUM(CASE WHEN used_units IS NULL THEN 1 ELSE 0 END) AS missing_used_units,
  SUM(CASE WHEN inventory_level IS NULL THEN 1 ELSE 0 END) AS missing_inventory_level
FROM supply;

-- ============================================
-- Step 3: Typecasting Example
-- ============================================
SELECT 
  CAST(age AS CHAR(5)) AS age_text,
  CAST(wait_time_min AS DECIMAL(10,2)) AS wait_time_numeric
FROM patients;

-- ============================================
-- Step 4: Dummy Variable Creation
-- ============================================
SELECT
  gender,
  CASE WHEN gender = 'Male' THEN 1 ELSE 0 END AS is_male
FROM patients;

SELECT
  shift,
  CASE WHEN shift = 'Morning' THEN 1 ELSE 0 END AS is_morning,
  CASE WHEN shift = 'Evening' THEN 1 ELSE 0 END AS is_evening,
  CASE WHEN shift = 'Night' THEN 1 ELSE 0 END AS is_night
FROM staff;

-- ============================================
-- Step 5: Normalization (Min-Max Scaling)
-- ============================================
SELECT 
  age,
  (age - (SELECT MIN(age) FROM patients)) / (SELECT MAX(age) - MIN(age) FROM patients) AS normalized_age
FROM patients;

SELECT 
  used_units,
  (used_units - (SELECT MIN(used_units) FROM supply)) / (SELECT MAX(used_units) - MIN(used_units) FROM supply) AS normalized_units
FROM supply;


-- ========== PATIENTS TABLE EDA ==========
-- 1. Central Tendency (Mean, Median, Mode)
SELECT AVG(age) AS Mean_Age FROM patients;
SELECT age AS Median_Age FROM (
    SELECT age, ROW_NUMBER() OVER (ORDER BY age) AS row_num, COUNT(*) OVER () AS total FROM patients
) AS t WHERE row_num IN (FLOOR((total + 1)/2), CEIL((total + 1)/2));
SELECT age AS Mode_Age FROM (
    SELECT age, COUNT(*) AS freq FROM patients GROUP BY age ORDER BY freq DESC LIMIT 1
) AS t;

-- Dispersion (Variance, SD, Range)
SELECT VARIANCE(age) AS Var_Age, STDDEV(age) AS SD_Age, MAX(age) - MIN(age) AS Range_Age FROM patients;

-- Skewness
SELECT (
    SUM(POWER(age - (SELECT AVG(age) FROM patients), 3)) /
    (COUNT(*) * POWER((SELECT STDDEV(age) FROM patients), 3))
) AS Skewness_Age FROM patients;

-- Kurtosis
SELECT (
    SUM(POWER(age - (SELECT AVG(age) FROM patients), 4)) /
    (COUNT(*) * POWER((SELECT STDDEV(age) FROM patients), 4)) - 3
) AS Kurtosis_Age FROM patients;

-- Repeat above for wait_time_min and bed_id as needed...

-- ========== STAFF TABLE EDA ==========
-- 1. Central Tendency (Mean, Median, Mode)
SELECT AVG(absent) AS Mean_absent FROM staff;
SELECT absent AS Median_absent FROM (
    SELECT absent, ROW_NUMBER() OVER (ORDER BY absent) AS row_num, COUNT(*) OVER () AS total FROM staff
) AS t WHERE row_num IN (FLOOR((total + 1)/2), CEIL((total + 1)/2));
SELECT absent AS Mode_absent FROM (
    SELECT absent, COUNT(*) AS freq FROM staff GROUP BY absent ORDER BY freq DESC LIMIT 1
) AS t;

-- Dispersion
SELECT VARIANCE(absent) AS Var_absent, STDDEV(absent) AS SD_absent, MAX(absent) - MIN(absent) AS Range_absent FROM staff;

-- Skewness
SELECT (
    SUM(POWER(absent - (SELECT AVG(absent) FROM staff), 3)) /
    (COUNT(*) * POWER((SELECT STDDEV(absent) FROM staff), 3))
) AS Skewness_absent FROM staff;

-- Kurtosis
SELECT (
    SUM(POWER(absent - (SELECT AVG(absent) FROM staff), 4)) /
    (COUNT(*) * POWER((SELECT STDDEV(absent) FROM staff), 4)) - 3
) AS Kurtosis_absent FROM staff;

-- ========== SUPPLY TABLE EDA ==========
-- Central Tendency
SELECT AVG(used_units) AS Mean_used_units FROM supply;
SELECT used_units AS Median_used_units FROM (
    SELECT used_units, ROW_NUMBER() OVER (ORDER BY used_units) AS row_num, COUNT(*) OVER () AS total FROM supply
) AS t WHERE row_num IN (FLOOR((total + 1)/2), CEIL((total + 1)/2));
SELECT used_units AS Mode_used_units FROM (
    SELECT used_units, COUNT(*) AS freq FROM supply GROUP BY used_units ORDER BY freq DESC LIMIT 1
) AS t;

-- Dispersion
SELECT VARIANCE(used_units) AS Var_used_units, STDDEV(used_units) AS SD_used_units, MAX(used_units) - MIN(used_units) AS Range_used_units FROM supply;

-- Skewness
SELECT (
    SUM(POWER(used_units - (SELECT AVG(used_units) FROM supply), 3)) /
    (COUNT(*) * POWER((SELECT STDDEV(used_units) FROM supply), 3))
) AS Skewness_used_units FROM supply;

-- Kurtosis
SELECT (
    SUM(POWER(used_units - (SELECT AVG(used_units) FROM supply), 4)) /
    (COUNT(*) * POWER((SELECT STDDEV(used_units) FROM supply), 4)) - 3
) AS Kurtosis_used_units FROM supply;

-- ===================== PATIENTS: age =====================
WITH ranked_age AS (
  SELECT age, NTILE(4) OVER (ORDER BY age) AS quartile FROM patients
), iqr_stats AS (
  SELECT 
    MIN(CASE WHEN quartile = 1 THEN age END) AS Q1,
    MAX(CASE WHEN quartile = 3 THEN age END) AS Q3
  FROM ranked_age
)
    
SELECT * FROM patients
WHERE age < (SELECT Q1 - 1.5 * (Q3 - Q1) FROM iqr_stats)
   OR age > (SELECT Q3 + 1.5 * (Q3 - Q1) FROM iqr_stats);

-- ===================== PATIENTS: wait_time_min =====================
WITH ordered AS (
  SELECT wait_time_min,
         ROW_NUMBER() OVER (ORDER BY wait_time_min) AS rn,
         COUNT(*) OVER () AS total
  FROM patients
),
iqr_values AS (
  SELECT
    MAX(CASE WHEN rn = FLOOR(total * 0.25) THEN wait_time_min END) AS Q1,
    MAX(CASE WHEN rn = FLOOR(total * 0.75) THEN wait_time_min END) AS Q3
  FROM ordered
)
SELECT *
FROM patients
WHERE wait_time_min < (SELECT Q1 - 1.5 * (Q3 - Q1) FROM iqr_values)
   OR wait_time_min > (SELECT Q3 + 1.5 * (Q3 - Q1) FROM iqr_values);

-- ===================== PATIENTS: bed_id =====================
WITH ordered AS (
  SELECT bed_id,
         ROW_NUMBER() OVER (ORDER BY bed_id) AS rn,
         COUNT(*) OVER () AS total
  FROM patients
),
iqr_values AS (
  SELECT
    MAX(CASE WHEN rn = FLOOR(total * 0.25) THEN bed_id END) AS Q1,
    MAX(CASE WHEN rn = FLOOR(total * 0.75) THEN bed_id END) AS Q3
  FROM ordered
)
SELECT * FROM iqr_values;

SELECT * FROM patients
WHERE bed_id < (SELECT Q1 - 1.5 * (Q3 - Q1) FROM iqr_stats)
   OR bed_id > (SELECT Q3 + 1.5 * (Q3 - Q1) FROM iqr_stats);

-- ===================== SUPPLY: used_units =====================
WITH ranked_units AS (
  SELECT used_units, NTILE(4) OVER (ORDER BY used_units) AS quartile FROM supply
), iqr_stats AS (
  SELECT 
    MIN(CASE WHEN quartile = 1 THEN used_units END) AS Q1,
    MAX(CASE WHEN quartile = 3 THEN used_units END) AS Q3
  FROM ranked_units
)
SELECT * FROM supply
WHERE used_units < (SELECT Q1 - 1.5 * (Q3 - Q1) FROM iqr_stats)
   OR used_units > (SELECT Q3 + 1.5 * (Q3 - Q1) FROM iqr_stats);

-- ===================== SUPPLY: inventory_level =====================
WITH ordered AS (
  SELECT inventory_level,
         ROW_NUMBER() OVER (ORDER BY inventory_level) AS rn,
         COUNT(*) OVER () AS total
  FROM supply
),
iqr_stats AS (
  SELECT
    MAX(CASE WHEN rn = FLOOR(total * 0.25) THEN inventory_level END) AS Q1,
    MAX(CASE WHEN rn = FLOOR(total * 0.75) THEN inventory_level END) AS Q3
  FROM ordered
)
SELECT * FROM iqr_stats;
SELECT * FROM supply
WHERE inventory_level < (SELECT Q1 - 1.5 * (Q3 - Q1) FROM iqr_stats)
   OR inventory_level > (SELECT Q3 + 1.5 * (Q3 - Q1) FROM iqr_stats);


