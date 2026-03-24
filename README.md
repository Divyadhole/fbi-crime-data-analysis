# Crime in America — FBI UCR Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-SQLite-lightgrey?logo=sqlite)](https://sqlite.org)
[![Data](https://img.shields.io/badge/Data-FBI%20UCR%20Program-red)](https://ucr.fbi.gov/)
[![Dashboard](https://img.shields.io/badge/🌐%20Live%20Dashboard-Click%20Here-brightgreen)](https://divyadhole.github.io/fbi-crime-data-analysis/)
[![CI](https://github.com/Divyadhole/fbi-crime-data-analysis/workflows/FBI%20Crime%20Analysis%20Validation/badge.svg)](https://github.com/Divyadhole/fbi-crime-data-analysis/actions)

## Live Dashboard

**[https://divyadhole.github.io/fbi-crime-data-analysis/](https://divyadhole.github.io/fbi-crime-data-analysis/)**

---

## What This Is

I pulled 8 years of FBI Uniform Crime Reporting data (2015-2022) and ran it through a full analysis pipeline — national trends, state rankings, city homicide comparisons, and a deep look at what COVID actually did to crime patterns.

The finding that stopped me: St. Louis has a homicide rate of 65.4 per 100,000. The US national average is 6.3. St. Louis is 10 times that. It's higher than Brazil, higher than Mexico, higher than South Africa by the same metric.

---

## Data

**FBI Uniform Crime Reporting Program** — https://ucr.fbi.gov/

The UCR has been running since 1930. Every local law enforcement agency in the country voluntarily submits crime counts to the FBI. The data is public, updated annually, and available through the Crime Data Explorer API at no cost.

```python
# Pull it yourself — no key needed for basic queries
import requests
resp = requests.get(
    "https://api.usa.gov/crime/fbi/cde/estimate/national/violent-crime/2015/2022",
    params={"API_KEY": "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"}
)
```

One important caveat: 2021 numbers are fuzzy. The FBI switched from Summary UCR to NIBRS in 2021 and many agencies didn't participate, so national estimates for that year are interpolated. I've noted this in the data dictionary.

---

## What I Found

**COVID spiked homicides by 56% in a single year.** That's not a rounding error. Mann-Whitney U test confirmed it (p=0.017, Cohen's d=4.28 — large effect). At the same time, robbery fell 10% and burglary fell 7.7%. People stayed home, so street crime dropped. But whatever drove the homicide spike — police pullback, economic stress, court system shutdowns — it overwhelmed everything else.

**Property crime has been falling consistently since 2015.** Linear regression gives a slope of -89 per year, R²=0.94. At that pace the rate hits ~1,600/100k by 2025. Better car locks, home security cameras, and a more cashless society probably all contribute.

**Alaska isn't just "dangerous" — it's a specific kind of dangerous.** Its violent crime rate (867/100k) is the highest in the country, but it's not driven by homicide. It's assault and domestic violence in remote communities with limited law enforcement access. Treating it the same as a high-homicide city misses the point.

---

## Numbers at a Glance

| Metric | Value |
|---|---|
| Most dangerous city | St. Louis, MO — 65.4/100k |
| St. Louis vs national avg | 10.4x |
| COVID homicide surge (2020) | +56% in one year |
| Property crime trend | -21.4% from 2015 to 2022 |
| Most dangerous state | Alaska — 867/100k |
| Safest tracked state | Maine — 122/100k |
| St. Louis vs Germany | 73x Germany's homicide rate |

---

## SQL That Does the Work

```sql
-- Year-over-year homicide change with LAG()
SELECT year, homicide,
    ROUND(homicide - LAG(homicide) OVER (ORDER BY year), 2) AS yoy_change,
    ROUND(100.0 * (homicide - LAG(homicide) OVER (ORDER BY year))
        / LAG(homicide) OVER (ORDER BY year), 1) AS pct_change
FROM national_crime ORDER BY year;

-- COVID pivot: exactly what went up and what went down
SELECT
    MAX(CASE WHEN year=2019 THEN homicide END) homicide_2019,
    MAX(CASE WHEN year=2020 THEN homicide END) homicide_2020,
    MAX(CASE WHEN year=2019 THEN robbery  END) robbery_2019,
    MAX(CASE WHEN year=2020 THEN robbery  END) robbery_2020
FROM national_crime;

-- Rolling 3-year average to smooth noise
SELECT year, violent,
    ROUND(AVG(violent) OVER (ORDER BY year ROWS 2 PRECEDING), 1) AS rolling_avg
FROM national_crime;
```

---

## Project Layout

```
fbi-crime-data-analysis/
├── src/
│   ├── fbi_data.py          # National, state, and city data tables
│   ├── fetch_fbi.py         # Live FBI CDE API fetcher
│   ├── charts.py            # 6 charts
│   ├── stats_analysis.py    # Mann-Whitney, regression, Cohen's d
│   ├── city_context.py      # US cities vs international rates
│   └── build_website.py     # GitHub Pages generator
├── sql/
│   └── analysis/crime_analysis.sql   # 7 queries
├── .github/workflows/
│   └── validate.yml         # CI — asserts stats are significant
├── data/
│   └── processed/
│       └── data_dictionary.md
├── docs/index.html          # Live dashboard
├── outputs/
│   ├── charts/              # 6 PNGs
│   └── excel/               # 6-sheet workbook
├── FINDINGS.md
└── run_analysis.py
```

---

## Run It

```bash
git clone https://github.com/Divyadhole/fbi-crime-data-analysis.git
cd fbi-crime-data-analysis
pip install -r requirements.txt
python run_analysis.py
```

---

*Project 12 of 40 — FBI UCR data is public domain, no restrictions on use.*
