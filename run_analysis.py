"""
run_analysis.py — FBI Crime Data Analysis Pipeline
Real data: FBI Uniform Crime Reporting (UCR) Program
"""
import sys, os, sqlite3
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from src.fbi_data import (load_national, load_states,
                            load_cities, load_covid_impact)
from src.charts import (chart_national_trend, chart_homicide_trend,
                         chart_state_ranking, chart_city_homicides,
                         chart_covid_crime_shift, chart_crime_composition)

CHARTS = "outputs/charts"
EXCEL  = "outputs/excel"
DB     = "data/fbi_crime.db"

for d in [CHARTS, EXCEL, "data/raw", "docs"]:
    os.makedirs(d, exist_ok=True)

print("=" * 62)
print("  FBI CRIME DATA ANALYSIS — UCR PROGRAM")
print("  Source: FBI Uniform Crime Reporting Program")
print("=" * 62)

print("\n[1/5] Loading FBI UCR data...")
df_nat    = load_national()
df_states = load_states()
df_cities = load_cities()
df_covid  = load_covid_impact()
print(f"  ✓ National: {len(df_nat)} years (2015-2022)")
print(f"  ✓ States:   {len(df_states)} state records (2022)")
print(f"  ✓ Cities:   {len(df_cities)} city homicide rates")
print(f"  ✓ COVID:    {len(df_covid)} crime categories analyzed")

print("\n[2/5] Loading to SQLite...")
conn = sqlite3.connect(DB)
df_nat.to_sql("national_crime", conn, if_exists="replace", index=False)
df_states.to_sql("state_crime",  conn, if_exists="replace", index=False)
df_cities.to_sql("city_homicide",conn, if_exists="replace", index=False)
df_covid.to_sql("covid_impact",  conn, if_exists="replace", index=False)
conn.close()
print(f"  ✓ DB → {DB}")

print("\n[3/5] Key findings...")
national_22 = 6.3
worst_city  = df_cities.nlargest(1,"homicide_rate").iloc[0]
safest_city = df_cities.nsmallest(1,"homicide_rate").iloc[0]
worst_state = df_states.nlargest(1,"violent_rate").iloc[0]
safest_state= df_states.nsmallest(1,"violent_rate").iloc[0]

hom_2019 = df_nat[df_nat["year"]==2019]["homicide"].values[0]
hom_2020 = df_nat[df_nat["year"]==2020]["homicide"].values[0]
hom_spike = (hom_2020 - hom_2019) / hom_2019 * 100

prop_2015 = df_nat[df_nat["year"]==2015]["property"].values[0]
prop_2022 = df_nat[df_nat["year"]==2022]["property"].values[0]
prop_drop  = (prop_2022 - prop_2015) / prop_2015 * 100

print(f"  Most dangerous city:  {worst_city['city']} ({worst_city['homicide_rate']}/100k)")
print(f"  Safest city:          {safest_city['city']} ({safest_city['homicide_rate']}/100k)")
print(f"  Worst state:          {worst_state['state']} ({worst_state['violent_rate']}/100k)")
print(f"  Safest state:         {safest_state['state']} ({safest_state['violent_rate']}/100k)")
print(f"  COVID homicide spike: +{hom_spike:.0f}% (2019→2020)")
print(f"  Property crime drop:  {prop_drop:+.1f}% (2015→2022)")
print(f"  St. Louis vs national:{worst_city['homicide_rate']/national_22:.1f}x the national average")

print("\n[4/5] Generating charts...")
chart_national_trend   (df_nat,    f"{CHARTS}/01_national_crime_trend.png")
chart_homicide_trend   (df_nat,    f"{CHARTS}/02_homicide_spike_covid.png")
chart_state_ranking    (df_states, f"{CHARTS}/03_state_violent_ranking.png")
chart_city_homicides   (df_cities, f"{CHARTS}/04_city_homicide_rates.png")
chart_covid_crime_shift(df_covid,  f"{CHARTS}/05_covid_crime_shift.png")
chart_crime_composition(df_nat,    f"{CHARTS}/06_crime_composition.png")

print("\n[5/5] Building Excel workbook...")
conn = sqlite3.connect(DB)
sheets = {
    "Key Findings": pd.DataFrame([
        {"Metric":"Most dangerous city 2022",    "Value":f"{worst_city['city']} — {worst_city['homicide_rate']}/100k"},
        {"Metric":"National homicide rate 2022", "Value":"6.3 per 100,000"},
        {"Metric":"St. Louis vs national",       "Value":f"{worst_city['homicide_rate']/national_22:.1f}x national avg"},
        {"Metric":"COVID homicide surge 2020",   "Value":f"+{hom_spike:.0f}%"},
        {"Metric":"Property crime trend",        "Value":f"{prop_drop:+.1f}% decline 2015-2022"},
        {"Metric":"Most dangerous state",        "Value":f"{worst_state['state']} ({worst_state['violent_rate']}/100k)"},
        {"Metric":"Safest state tracked",        "Value":f"{safest_state['state']} ({safest_state['violent_rate']}/100k)"},
        {"Metric":"Data source",                 "Value":"FBI UCR — https://ucr.fbi.gov/"},
        {"Metric":"API",                         "Value":"https://api.usa.gov/crime/fbi/cde/"},
    ]),
    "National Trend": df_nat,
    "State Rankings": df_states.sort_values("violent_rate", ascending=False),
    "City Homicides": df_cities.sort_values("homicide_rate", ascending=False),
    "COVID Impact":   df_covid,
    "SQL Queries":    pd.read_sql("""
        SELECT year, violent, property, homicide,
            ROUND(violent - LAG(violent) OVER (ORDER BY year),1) violent_yoy,
            ROUND(100.0*(homicide - LAG(homicide) OVER (ORDER BY year))
                / LAG(homicide) OVER (ORDER BY year),1) homicide_pct_chg
        FROM national_crime ORDER BY year
    """, conn),
}
excel_path = f"{EXCEL}/fbi_crime_analysis.xlsx"
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    for name, dfs in sheets.items():
        dfs.to_excel(writer, sheet_name=name, index=False)
        ws = writer.sheets[name]
        for col in ws.columns:
            w = max(len(str(c.value or "")) for c in col) + 3
            ws.column_dimensions[col[0].column_letter].width = min(w, 38)
conn.close()
print(f"  ✓ Excel → {excel_path}")

print("\n" + "=" * 62)
print("  PIPELINE COMPLETE")
print("=" * 62)
print(f"  Worst city:    {worst_city['city']} — {worst_city['homicide_rate']}/100k")
print(f"  COVID spike:   +{hom_spike:.0f}% homicides in 2020")
print(f"  Property drop: {prop_drop:+.1f}% since 2015")
print(f"  Charts → {CHARTS}/")
