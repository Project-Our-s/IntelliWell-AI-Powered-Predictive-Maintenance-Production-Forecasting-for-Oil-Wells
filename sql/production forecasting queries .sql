--Create Table For Volve-Production-Data & Monthly-Production-Data--
--Volve-Prpduction-Data--
CREATE TABLE production_daily (
    dateprd TEXT,
    well_bore_code TEXT,
    npd_well_bore_code TEXT,
    npd_well_bore_name TEXT,
    npd_field_code TEXT,
    npd_field_name TEXT,
    npd_facility_code TEXT,
    npd_facility_name TEXT,
    on_stream_hrs TEXT,
    avg_downhole_pressure TEXT,
    avg_downhole_temperature TEXT,
    avg_dp_tubing TEXT,
    avg_annulus_press TEXT,
    avg_choke_size_p TEXT,
    avg_choke_uom TEXT,
    avg_whp_p TEXT,
    avg_wht_p TEXT,
    dp_choke_size TEXT,
    bore_oil_vol TEXT,
    bore_gas_vol TEXT,
    bore_wat_vol TEXT,
    bore_wi_vol TEXT,
    flow_kind TEXT,
    well_type TEXT
);

--production monthly--
CREATE TABLE production_monthly (
    wellbore_name TEXT,
    npdcode TEXT,
    year TEXT,
    month TEXT,
    on_stream_hrs TEXT,
    oil_sm3 TEXT,
    gas_sm3 TEXT,
    water_sm3 TEXT,
    gi_sm3 TEXT,
    wi_sm3 TEXT
);


--total rows of production daily--
SELECT COUNT(*) AS total_records
FROM production_daily;

--total rows of production monthly--
SELECT COUNT(*) AS total_records
FROM production_monthly;

--Checking duplicate record--
SELECT dateprd,
       well_bore_code,
       COUNT(*)
FROM production_daily
GROUP BY dateprd, well_bore_code
HAVING COUNT(*) > 1;

--missing values--
SELECT
SUM(CASE WHEN dateprd='' THEN 1 ELSE 0 END) AS missing_date,
SUM(CASE WHEN well_bore_code='' THEN 1 ELSE 0 END) AS missing_well,
SUM(CASE WHEN bore_oil_vol='' THEN 1 ELSE 0 END) AS missing_oil,
SUM(CASE WHEN bore_gas_vol='' THEN 1 ELSE 0 END) AS missing_gas,
SUM(CASE WHEN bore_wat_vol='' THEN 1 ELSE 0 END) AS missing_water
FROM production_daily;

--distinct well--
SELECT COUNT(DISTINCT well_bore_code)
AS total_wells

--flow types--
SELECT
    flow_kind,
    COUNT(*) AS total_records
FROM production_daily
GROUP BY flow_kind;

--well type--
SELECT
    well_type,
    COUNT(*) AS total_records
FROM production_daily
GROUP BY well_type;

--creating clean table--
CREATE TABLE production_daily_clean AS
SELECT
    TO_DATE(dateprd, 'DD-Mon-YY') AS dateprd,
    well_bore_code,
    CAST(npd_well_bore_code AS INTEGER) AS npd_well_bore_code,
    npd_well_bore_name,
    CAST(npd_field_code AS INTEGER) AS npd_field_code,
    npd_field_name,
    CAST(npd_facility_code AS INTEGER) AS npd_facility_code,
    npd_facility_name,

    NULLIF(on_stream_hrs,'')::NUMERIC AS on_stream_hrs,
    NULLIF(avg_downhole_pressure,'')::NUMERIC AS avg_downhole_pressure,
    NULLIF(avg_downhole_temperature,'')::NUMERIC AS avg_downhole_temperature,
    NULLIF(avg_dp_tubing,'')::NUMERIC AS avg_dp_tubing,
    NULLIF(avg_annulus_press,'')::NUMERIC AS avg_annulus_press,
    NULLIF(avg_choke_size_p,'')::NUMERIC AS avg_choke_size_p,

    avg_choke_uom,

    NULLIF(avg_whp_p,'')::NUMERIC AS avg_whp_p,
    NULLIF(avg_wht_p,'')::NUMERIC AS avg_wht_p,
    NULLIF(dp_choke_size,'')::NUMERIC AS dp_choke_size,

    REPLACE(NULLIF(bore_oil_vol,''),',','')::NUMERIC AS bore_oil_vol,
    REPLACE(NULLIF(bore_gas_vol,''),',','')::NUMERIC AS bore_gas_vol,
    REPLACE(NULLIF(bore_wat_vol,''),',','')::NUMERIC AS bore_wat_vol,
    REPLACE(NULLIF(bore_wi_vol,''),',','')::NUMERIC AS bore_wi_vol,

    flow_kind,
    well_type

FROM production_daily;

--checking data types--
SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name='production_daily_clean';

--total oil,gas and water production--
SELECT
SUM(bore_oil_vol) AS total_oil_sm3,
SUM(bore_gas_vol) AS total_gas_sm3,
SUM(bore_wat_vol) AS total_water_sm3
FROM production_daily_clean;

--number of active wells--
SELECT
COUNT(DISTINCT well_bore_code) AS active_wells
FROM production_daily_clean;

--Production by well--
SELECT
well_bore_code,
SUM(bore_oil_vol) AS total_oil
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY total_oil DESC;

--Top 10 oil producing well--
SELECT
well_bore_code,
SUM(bore_oil_vol) AS total_oil
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY total_oil DESC
LIMIT 10;

--top 10 gas producing well--
SELECT
well_bore_code,
SUM(bore_gas_vol) AS total_gas
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY total_gas DESC
LIMIT 10;

--higher water producing well--
SELECT
well_bore_code,
SUM(bore_wat_vol) AS total_water
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY total_water DESC;

--Average downhole pressure by well--
SELECT
well_bore_code,
ROUND(AVG(avg_downhole_pressure),2) AS avg_pressure
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY avg_pressure DESC;

--Average wellhead pressure--
SELECT
well_bore_code,
ROUND(AVG(avg_whp_p),2) AS avg_whp
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY avg_whp DESC;

--Average on stream hour--
SELECT
well_bore_code,
ROUND(AVG(on_stream_hrs),2) AS avg_stream_hours
FROM production_daily_clean
GROUP BY well_bore_code
ORDER BY avg_stream_hours DESC;

--production by flow type--
SELECT
flow_kind,
SUM(bore_oil_vol) AS oil,
SUM(bore_gas_vol) AS gas,
SUM(bore_wat_vol) AS water
FROM production_daily_clean
GROUP BY flow_kind;


--Check for text 'NULL' values in numeric columns before data type conversion--
SELECT
    wellbore_name,
    npdcode,
    year,
    month,
    on_stream_hrs,
    oil_sm3,
    gas_sm3,
    water_sm3,
    gi_sm3,
    wi_sm3
FROM production_monthly
WHERE
      UPPER(TRIM(COALESCE(on_stream_hrs,''))) = 'NULL'
   OR UPPER(TRIM(COALESCE(oil_sm3,''))) = 'NULL'
   OR UPPER(TRIM(COALESCE(gas_sm3,''))) = 'NULL'
   OR UPPER(TRIM(COALESCE(water_sm3,''))) = 'NULL'
   OR UPPER(TRIM(COALESCE(gi_sm3,''))) = 'NULL'
   OR UPPER(TRIM(COALESCE(wi_sm3,''))) = 'NULL';


--Replace text 'NULL' values with SQL NULL to enable numeric conversion--
UPDATE production_monthly
SET
    on_stream_hrs = NULLIF(TRIM(on_stream_hrs), 'NULL'),
    oil_sm3       = NULLIF(TRIM(oil_sm3), 'NULL'),
    gas_sm3       = NULLIF(TRIM(gas_sm3), 'NULL'),
    water_sm3     = NULLIF(TRIM(water_sm3), 'NULL'),
    gi_sm3        = NULLIF(TRIM(gi_sm3), 'NULL'),
    wi_sm3        = NULLIF(TRIM(wi_sm3), 'NULL');


--Creating clean production monthly table--
CREATE TABLE production_monthly_clean AS
SELECT
    wellbore_name,
    npdcode::INTEGER,
    year::INTEGER,
    month::INTEGER,

    NULLIF(on_stream_hrs,'')::NUMERIC AS on_stream_hrs,

    REPLACE(oil_sm3,',','')::NUMERIC AS oil_sm3,
    REPLACE(gas_sm3,',','')::NUMERIC AS gas_sm3,
    REPLACE(water_sm3,',','')::NUMERIC AS water_sm3,

    CASE
        WHEN gi_sm3 IS NULL OR gi_sm3='' THEN NULL
        ELSE REPLACE(gi_sm3,',','')::NUMERIC
    END AS gi_sm3,

    CASE
        WHEN wi_sm3 IS NULL OR wi_sm3='' THEN NULL
        ELSE REPLACE(wi_sm3,',','')::NUMERIC
    END AS wi_sm3

FROM production_monthly;


-- Preview cleaned monthly production data
SELECT *
FROM production_monthly_clean
LIMIT 10;

-- Year-wise production summary
SELECT
    year,
    SUM(oil_sm3) AS total_oil,
    SUM(gas_sm3) AS total_gas,
    SUM(water_sm3) AS total_water
FROM production_monthly_clean
GROUP BY year


-- Monthly production trend--
SELECT
    year,
    month,
    SUM(oil_sm3) AS total_oil,
    SUM(gas_sm3) AS total_gas,
    SUM(water_sm3) AS total_water
FROM production_monthly_clean
GROUP BY year, month
ORDER BY year, month;


-- Highest oil production month in each year--
SELECT DISTINCT ON (year)
    year,
    month,
    SUM(oil_sm3) AS total_oil
FROM production_monthly_clean
GROUP BY year, month
ORDER BY year, total_oil DESC;


-- Oil produced per operating hour--
SELECT
    wellbore_name,
    year,
    month,
    ROUND(oil_sm3 / NULLIF(on_stream_hrs,0),2) AS oil_per_hour
FROM production_monthly_clean
ORDER BY oil_per_hour DESC;


-- Water to oil production ratio
SELECT
    wellbore_name,
    year,
    month,
    ROUND((water_sm3 / NULLIF(oil_sm3,0))*100,2) AS water_cut_percent
FROM production_monthly_clean
ORDER BY water_cut_percent DESC;