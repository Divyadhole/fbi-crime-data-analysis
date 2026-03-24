"""
src/fetch_fbi.py
Fetches real data from FBI Crime Data Explorer API.

Free API key: https://api.usa.gov/crime/fbi/cde/
Register at: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/home

Docs: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi
Rate limit: No strict limit — be respectful (1-2 req/sec)
"""

import requests
import pandas as pd
import os

FBI_BASE = "https://api.usa.gov/crime/fbi/cde"
API_KEY  = os.getenv("FBI_API_KEY", "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv")
# ^ public demo key from FBI CDE docs — replace with your own for production

OFFENSE_MAP = {
    "violent-crime":    "Violent Crime",
    "homicide":         "Homicide",
    "rape-legacy":      "Rape",
    "robbery":          "Robbery",
    "aggravated-assault":"Aggravated Assault",
    "property-crime":   "Property Crime",
    "burglary":         "Burglary",
    "larceny":          "Larceny",
    "motor-vehicle-theft":"Motor Vehicle Theft",
}


def fetch_national_trend(offense: str = "violent-crime",
                          start: int = 2015,
                          end: int   = 2022) -> pd.DataFrame:
    """Fetch national crime trend for a specific offense."""
    url = f"{FBI_BASE}/estimate/national/{offense}/{start}/{end}"
    resp = requests.get(url, params={"API_KEY": API_KEY}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data.get("results", []))


def fetch_state_data(state_abbr: str = "CA",
                     offense: str = "violent-crime",
                     year: int = 2022) -> dict:
    """Fetch crime data for a specific state."""
    url = f"{FBI_BASE}/estimate/state/{state_abbr}/{offense}/{year}/{year}"
    resp = requests.get(url, params={"API_KEY": API_KEY}, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_agency_data(ori: str = "CA0197200") -> dict:
    """Fetch crime data for a specific agency by ORI code."""
    url = f"{FBI_BASE}/summarized/agency/{ori}/offenses/2022/2022"
    resp = requests.get(url, params={"API_KEY": API_KEY}, timeout=20)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    print("FBI Crime Data Explorer API Fetcher")
    print("API Key source: https://api.usa.gov/crime/fbi/cde/")
    print()
    print("Environment variable: FBI_API_KEY")
    print("Demo key included for testing.")
    print()
    try:
        df = fetch_national_trend("violent-crime", 2019, 2022)
        print(f"National violent crime trend: {len(df)} years fetched")
    except Exception as e:
        print(f"Note: {e}")
        print("Using embedded data from src/fbi_data.py")
