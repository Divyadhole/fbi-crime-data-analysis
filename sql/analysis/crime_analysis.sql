-- ============================================================
-- sql/analysis/crime_analysis.sql
-- FBI UCR Crime Data Analysis
-- Source: FBI Uniform Crime Reporting Program
-- ============================================================

-- 1. National crime trend: year-over-year change
SELECT year, violent, property, homicide,
    ROUND(violent  - LAG(violent)  OVER (ORDER BY year), 1) AS violent_yoy,
    ROUND(property - LAG(property) OVER (ORDER BY year), 1) AS property_yoy,
    ROUND(homicide - LAG(homicide) OVER (ORDER BY year), 1) AS homicide_yoy,
    ROUND(100.0*(violent - LAG(violent) OVER (ORDER BY year))
        / LAG(violent) OVER (ORDER BY year), 2)             AS violent_pct_chg
FROM national_crime
ORDER BY year;


-- 2. COVID anomaly: 2020 spike vs 2019
SELECT
    MAX(CASE WHEN year=2019 THEN homicide END)   AS homicide_2019,
    MAX(CASE WHEN year=2020 THEN homicide END)   AS homicide_2020,
    MAX(CASE WHEN year=2021 THEN homicide END)   AS homicide_2021,
    ROUND(100.0*(MAX(CASE WHEN year=2020 THEN homicide END) -
                 MAX(CASE WHEN year=2019 THEN homicide END))
        / MAX(CASE WHEN year=2019 THEN homicide END), 1)    AS pct_surge_2020,
    MAX(CASE WHEN year=2019 THEN robbery END)    AS robbery_2019,
    MAX(CASE WHEN year=2020 THEN robbery END)    AS robbery_2020,
    ROUND(100.0*(MAX(CASE WHEN year=2020 THEN robbery END) -
                 MAX(CASE WHEN year=2019 THEN robbery END))
        / MAX(CASE WHEN year=2019 THEN robbery END), 1)     AS robbery_pct_chg
FROM national_crime;


-- 3. State ranking: most vs least dangerous (violent crime rate 2022)
SELECT state, violent_rate, rank,
    ROUND(violent_rate - 380.7, 1)              AS vs_national_avg,
    CASE
        WHEN violent_rate > 600 THEN 'Danger Zone'
        WHEN violent_rate > 400 THEN 'Above Average'
        WHEN violent_rate > 300 THEN 'Near Average'
        ELSE 'Below Average'
    END                                          AS safety_tier
FROM state_crime
ORDER BY violent_rate DESC;


-- 4. City homicide comparison — multiples of national average
SELECT city, state, homicide_rate, rank, times_national_avg,
    RANK() OVER (ORDER BY homicide_rate DESC)    AS city_rank
FROM city_homicide
ORDER BY homicide_rate DESC;


-- 5. Crime composition: how violent vs property crime changed over time
SELECT year,
    violent, property,
    ROUND(100.0 * violent  / (violent + property), 2) AS violent_share_pct,
    ROUND(100.0 * property / (violent + property), 2) AS property_share_pct,
    ROUND(homicide / violent * 100, 2)                AS homicide_pct_of_violent
FROM national_crime
ORDER BY year;


-- 6. 2015-2022 long-term trends: improving or worsening?
WITH trend AS (
    SELECT
        MIN(CASE WHEN year=2015 THEN violent  END) v_2015,
        MIN(CASE WHEN year=2022 THEN violent  END) v_2022,
        MIN(CASE WHEN year=2015 THEN property END) p_2015,
        MIN(CASE WHEN year=2022 THEN property END) p_2022,
        MIN(CASE WHEN year=2015 THEN homicide END) h_2015,
        MIN(CASE WHEN year=2022 THEN homicide END) h_2022
    FROM national_crime
)
SELECT
    ROUND(100.0*(v_2022-v_2015)/v_2015, 1) AS violent_change_pct,
    ROUND(100.0*(p_2022-p_2015)/p_2015, 1) AS property_change_pct,
    ROUND(100.0*(h_2022-h_2015)/h_2015, 1) AS homicide_change_pct,
    CASE WHEN v_2022 < v_2015 THEN 'Improving' ELSE 'Worsening' END AS violent_trend,
    CASE WHEN p_2022 < p_2015 THEN 'Improving' ELSE 'Worsening' END AS property_trend
FROM trend;


-- 7. Rolling 3-year average for trend smoothing
SELECT year, violent, homicide,
    ROUND(AVG(violent)  OVER (ORDER BY year ROWS 2 PRECEDING), 1) AS violent_3yr_avg,
    ROUND(AVG(homicide) OVER (ORDER BY year ROWS 2 PRECEDING), 2) AS homicide_3yr_avg,
    ROUND(AVG(property) OVER (ORDER BY year ROWS 2 PRECEDING), 1) AS property_3yr_avg
FROM national_crime
ORDER BY year;
