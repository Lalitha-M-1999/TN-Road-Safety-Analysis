SELECT TOP (1000) [accident_id]
      ,[accident_date]
      ,[accident_time]
      ,[location_id]
      ,[cause_id]
      ,[vehicle_type]
      ,[killed]
      ,[injured]
  FROM [TN_ROAD_SAFETY].[dbo].[accidents]


  1. Year-over-Year Growth (Trend Analysis)


  SELECT 
    YEAR(CAST(accident_date AS DATE)) AS accident_year,
    COUNT(*) AS total_accidents,
    SUM(killed) AS total_killed,
    LAG(COUNT(*)) OVER (ORDER BY YEAR(CAST(accident_date AS DATE))) AS prev_year_accidents,
    CONCAT(ROUND((COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY YEAR(CAST(accident_date AS DATE)))) * 100.0 / LAG(COUNT(*)) OVER (ORDER BY YEAR(CAST(accident_date AS DATE))), 2), '%') AS yoy_growth
FROM accidents
GROUP BY YEAR(CAST(accident_date AS DATE))
ORDER BY accident_year;


2. Most Dangerous Hotspots in Tamil Nadu (Ranking)

SELECT 
    l.city,
    l.district,
    COUNT(*) AS total_accidents,
    SUM(killed) AS fatalities,
    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS danger_rank
FROM accidents a
JOIN locations l ON a.location_id = l.location_id
GROUP BY l.city, l.district
ORDER BY total_accidents DESC;

3. Cause-wise Fatality Rate - What REALLY kills?

SELECT 
    c.cause_name,
    COUNT(*) AS total_accidents,
    SUM(killed) AS total_killed,
    CAST(SUM(killed) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS fatality_rate_per_100_acc,
    AVG(killed + injured) AS avg_severity
FROM accidents a
JOIN causes c ON a.cause_id = c.cause_id
GROUP BY c.cause_name
ORDER BY fatality_rate_per_100_acc DESC;

4. Night vs Day - When is it most dangerous? (CTE + CASE)

WITH time_analysis AS (
    SELECT *,
        CASE 
            WHEN CAST(LEFT(accident_time, 2) AS INT) BETWEEN 5 AND 11 THEN 'Morning (5AM-11AM)'
            WHEN CAST(LEFT(accident_time, 2) AS INT) BETWEEN 12 AND 16 THEN 'Afternoon (12PM-4PM)'
            WHEN CAST(LEFT(accident_time, 2) AS INT) BETWEEN 17 AND 20 THEN 'Evening (5PM-8PM)'
            ELSE 'Night (9PM-4AM)'
        END AS time_slot
    FROM accidents
)
SELECT 
    time_slot,
    COUNT(*) AS accidents,
    SUM(killed) AS killed,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM accidents) AS DECIMAL(5,2)) AS pct_of_total
FROM time_analysis
GROUP BY time_slot
ORDER BY accidents DESC;


5. Your City Gummidipundi vs Chennai - Comparison

SELECT 
    l.city,
    DATENAME(MONTH, CAST(accident_date AS DATE)) AS month_name,
    MONTH(CAST(accident_date AS DATE)) AS month_num,
    COUNT(*) AS accidents
FROM accidents a
JOIN locations l ON a.location_id = l.location_id
WHERE l.city IN ('Gummidipundi', 'Chennai')
GROUP BY l.city, DATENAME(MONTH, CAST(accident_date AS DATE)), MONTH(CAST(accident_date AS DATE))
ORDER BY l.city, month_num;


6. Top 3 Causes per City (PARTITION BY - Very Advanced)

WITH city_cause AS (
    SELECT 
        l.city,
        c.cause_name,
        COUNT(*) AS cnt,
        ROW_NUMBER() OVER (PARTITION BY l.city ORDER BY COUNT(*) DESC) AS rn
    FROM accidents a
    JOIN locations l ON a.location_id = l.location_id
    JOIN causes c ON a.cause_id = c.cause_id
    GROUP BY l.city, c.cause_name
)
SELECT city, cause_name, cnt
FROM city_cause
WHERE rn <= 3
ORDER BY city, cnt DESC;


7. Vehicle Type Risk Analysis


SELECT 
    vehicle_type,
    COUNT(*) AS total_accidents,
    SUM(killed) AS killed,
    SUM(injured) AS injured,
    SUM(killed + injured) AS total_casualties,
    CAST(AVG(killed + injured) AS DECIMAL(5,2)) AS avg_casualty_per_accident
FROM accidents
GROUP BY vehicle_type
ORDER BY total_casualties DESC;



8. Monthly Trend for Dashboard

SELECT 
    YEAR(CAST(accident_date AS DATE)) AS yr,
    MONTH(CAST(accident_date AS DATE)) AS mn,
    COUNT(*) AS accidents,
    SUM(killed) AS killed
FROM accidents
GROUP BY YEAR(CAST(accident_date AS DATE)), MONTH(CAST(accident_date AS DATE))
ORDER BY yr, mn;

9. Critical KPI View for Power BI

CREATE VIEW vw_dashboard_kpi AS
SELECT 
    a.accident_id,
    CAST(a.accident_date AS DATE) AS accident_date,
    a.accident_time,
    l.city,
    l.district,
    c.cause_name,
    a.vehicle_type,
    a.killed,
    a.injured,
    (a.killed + a.injured) AS total_casualty
FROM accidents a
JOIN locations l ON a.location_id = l.location_id
JOIN causes c ON a.cause_id = c.cause_id;

select * from vw_dashboard_kpi

10. Stored Procedure - Recruiter Favorite

CREATE PROCEDURE GetCitySafetyReport @CityName VARCHAR(50)
AS
BEGIN
    SELECT 
        @CityName AS city,
        COUNT(*) AS total_accidents,
        SUM(killed) AS total_deaths,
        (SELECT cause_name FROM causes WHERE cause_id = 
            (SELECT TOP 1 cause_id FROM accidents a2 
             JOIN locations l2 ON a2.location_id=l2.location_id 
             WHERE l2.city=@CityName GROUP BY cause_id ORDER BY COUNT(*) DESC)
        ) AS top_cause
    FROM accidents a
    JOIN locations l ON a.location_id = l.location_id
    WHERE l.city = @CityName;
END;


EXEC GetCitySafetyReport 'Gummidipundi';
EXEC GetCitySafetyReport 'Chennai';


11. Index for Performance (Show you know optimization)

CREATE INDEX idx_acc_date ON accidents(accident_date);
CREATE INDEX idx_location ON accidents(location_id);

EXEC sp_helpindex 'accidents';

-- Show execution plan before/after

12. Data Quality Check (Shows you are real analyst)

SELECT 'Total Accidents' AS metric, COUNT(*) AS value FROM accidents
UNION ALL
SELECT 'Duplicate IDs', COUNT(*) - COUNT(DISTINCT accident_id) FROM accidents
UNION ALL
SELECT 'Zero Casualty Records', COUNT(*) FROM accidents WHERE killed=0 AND injured=0;




SELECT 
    COUNT(*) AS total,
    SUM(killed) AS deaths,
    (SELECT city FROM locations WHERE location_id = (SELECT TOP 1 location_id FROM accidents GROUP BY location_id ORDER BY COUNT(*) DESC)) AS most_dangerous_city
FROM accidents;


























































































