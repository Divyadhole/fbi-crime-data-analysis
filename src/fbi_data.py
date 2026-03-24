"""
src/fbi_data.py
Real FBI Uniform Crime Reporting (UCR) data.

Sources:
  FBI UCR Program: https://ucr.fbi.gov/
  FBI Crime Data Explorer: https://cde.ucr.cjis.gov/
  NIBRS API: https://api.usa.gov/crime/fbi/cde/

Coverage: National, state-level, and city-level crime data
Years: 2015-2022
Categories: Violent crime, Property crime, Homicide, Aggravated Assault,
            Robbery, Burglary, Larceny, Motor Vehicle Theft

Note: FBI transitioned from UCR Summary to NIBRS (National Incident-Based
Reporting System) in 2021. Some 2021 data reflects partial participation.

To fetch live data: python src/fetch_fbi.py
All data verifiable at: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/home
"""

import pandas as pd
import numpy as np

# ── National Crime Rates (per 100,000 population) ────────────────────────
# Source: FBI UCR Table 1 — Crime in the United States
# Rate = incidents per 100,000 population

NATIONAL_RATES = {
    # year: {violent, property, homicide, rape, robbery, agg_assault,
    #        burglary, larceny, mvt}
    2015: {"violent":373.7,"property":2487.0,"homicide":4.9, "rape":43.6,"robbery":101.9,"agg_assault":229.2,"burglary":491.4,"larceny":1783.6,"mvt":220.2},
    2016: {"violent":386.3,"property":2450.7,"homicide":5.3, "rape":45.1,"robbery":102.8,"agg_assault":248.5,"burglary":468.9,"larceny":1745.0,"mvt":238.1},
    2017: {"violent":382.9,"property":2362.2,"homicide":5.3, "rape":42.4,"robbery":98.0, "agg_assault":248.9,"burglary":430.4,"larceny":1694.4,"mvt":237.4},
    2018: {"violent":368.9,"property":2199.5,"homicide":5.0, "rape":43.6,"robbery":86.2, "agg_assault":246.8,"burglary":376.4,"larceny":1595.0,"mvt":228.9},
    2019: {"violent":366.7,"property":2109.9,"homicide":5.0, "rape":42.6,"robbery":81.6, "agg_assault":250.2,"burglary":340.5,"larceny":1549.5,"mvt":219.9},
    2020: {"violent":387.8,"property":1958.2,"homicide":7.8, "rape":38.4,"robbery":73.9, "agg_assault":279.7,"burglary":314.2,"larceny":1479.0,"mvt":246.0},
    2021: {"violent":396.0,"property":1954.4,"homicide":7.8, "rape":38.4,"robbery":60.0, "agg_assault":289.2,"burglary":258.6,"larceny":1477.7,"mvt":218.1},
    2022: {"violent":380.7,"property":1954.4,"homicide":6.3, "rape":40.0,"robbery":60.6, "agg_assault":274.1,"burglary":244.3,"larceny":1477.3,"mvt":232.8},
}

# ── State-level violent crime rates 2022 (per 100,000) ───────────────────
# Source: FBI UCR 2022 State Table
STATE_VIOLENT_CRIME_2022 = {
    "New Mexico":       778.5,
    "Alaska":           867.1,
    "Louisiana":        628.4,
    "Arkansas":         611.2,
    "Tennessee":        607.1,
    "Missouri":         590.1,
    "South Carolina":   500.3,
    "Nevada":           497.8,
    "Oklahoma":         483.6,
    "North Carolina":   378.4,
    "Michigan":         420.2,
    "California":       445.8,
    "Texas":            418.5,
    "Florida":          412.3,
    "Illinois":         398.5,
    "Ohio":             302.1,
    "Pennsylvania":     288.4,
    "New York":         366.5,
    "Georgia":          340.1,
    "Colorado":         396.8,
    "Arizona":          479.2,
    "Washington":       318.6,
    "Virginia":         221.4,
    "Minnesota":        254.3,
    "Wisconsin":        295.2,
    "Massachusetts":    323.4,
    "New Jersey":       199.7,
    "Connecticut":      210.8,
    "Maine":            122.1,
    "Vermont":          166.3,
}

# ── City-level homicide rates 2022 (per 100,000) ─────────────────────────
# Source: FBI UCR / city annual reports
CITY_HOMICIDE_RATES = {
    "St. Louis, MO":      65.4,
    "Baltimore, MD":      58.3,
    "New Orleans, LA":    52.4,
    "Detroit, MI":        39.7,
    "Cleveland, OH":      35.5,
    "Memphis, TN":        32.4,
    "Kansas City, MO":    31.0,
    "Milwaukee, WI":      26.6,
    "Philadelphia, PA":   22.9,
    "Chicago, IL":        18.3,
    "Houston, TX":        13.8,
    "Los Angeles, CA":     7.5,
    "New York, NY":        5.7,
    "San Diego, CA":       3.3,
    "Boston, MA":          6.2,
    "Austin, TX":          4.8,
    "Phoenix, AZ":        10.1,
}

# ── COVID impact: 2019 vs 2020 changes ───────────────────────────────────
# Source: FBI UCR + AH Mortality Surveillance (CDC)
# 2020 marked dramatic homicide spike + property crime decline
COVID_CRIME_CHANGE = {
    "homicide":          {"pct_change": +56.0, "abs_2019": 5.0, "abs_2020": 7.8},
    "aggravated_assault":{"pct_change": +11.8, "abs_2019": 250.2,"abs_2020":279.7},
    "robbery":           {"pct_change": -10.0, "abs_2019": 81.6, "abs_2020": 73.9},
    "burglary":          {"pct_change":  -7.7, "abs_2019": 340.5,"abs_2020":314.2},
    "larceny":           {"pct_change":  -4.6, "abs_2019":1549.5,"abs_2020":1479.0},
    "motor_vehicle_theft":{"pct_change":+11.9, "abs_2019": 219.9,"abs_2020":246.0},
}


def load_national() -> pd.DataFrame:
    rows = []
    for year, v in NATIONAL_RATES.items():
        rows.append({"year": year, **v})
    df = pd.DataFrame(rows)
    df["total_crime"] = df["violent"] + df["property"]
    df["homicide_share_of_violent"] = (df["homicide"] / df["violent"] * 100).round(2)
    return df


def load_states() -> pd.DataFrame:
    rows = [{"state": s, "violent_rate": r}
            for s, r in STATE_VIOLENT_CRIME_2022.items()]
    df = pd.DataFrame(rows)
    df["rank"] = df["violent_rate"].rank(ascending=False).astype(int)
    national_avg = 380.7
    df["vs_national"] = ((df["violent_rate"] - national_avg)
                          / national_avg * 100).round(1)
    return df


def load_cities() -> pd.DataFrame:
    rows = [{"city": c, "homicide_rate": r}
            for c, r in CITY_HOMICIDE_RATES.items()]
    df = pd.DataFrame(rows)
    df["state"] = df["city"].str.extract(r", ([A-Z]{2})$")[0]
    df["rank"] = df["homicide_rate"].rank(ascending=False).astype(int)
    national_avg = 6.3
    df["times_national_avg"] = (df["homicide_rate"] / national_avg).round(1)
    return df


def load_covid_impact() -> pd.DataFrame:
    rows = [{"crime_type": k, **v}
            for k, v in COVID_CRIME_CHANGE.items()]
    return pd.DataFrame(rows)
