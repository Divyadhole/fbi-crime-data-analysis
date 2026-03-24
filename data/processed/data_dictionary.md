# Data Dictionary — FBI UCR Crime Analysis

## Data Sources

| Source | Description | URL |
|---|---|---|
| FBI UCR | Uniform Crime Reporting Program | https://ucr.fbi.gov/ |
| FBI CDE | Crime Data Explorer | https://cde.ucr.cjis.gov/ |
| FBI CDE API | Programmatic data access | https://api.usa.gov/crime/fbi/cde/ |

---

## Tables

### `national_crime`
| Column | Unit | Description |
|---|---|---|
| year | INT | 2015-2022 |
| violent | FLOAT | Violent crime rate per 100,000 population |
| property | FLOAT | Property crime rate per 100,000 population |
| homicide | FLOAT | Homicide rate per 100,000 population |
| rape | FLOAT | Rape rate per 100,000 (legacy definition) |
| robbery | FLOAT | Robbery rate per 100,000 |
| agg_assault | FLOAT | Aggravated assault rate per 100,000 |
| burglary | FLOAT | Burglary rate per 100,000 |
| larceny | FLOAT | Larceny-theft rate per 100,000 |
| mvt | FLOAT | Motor vehicle theft rate per 100,000 |
| total_crime | FLOAT | violent + property combined |

### `state_crime`
| Column | Unit | Description |
|---|---|---|
| state | VARCHAR | State name |
| violent_rate | FLOAT | Violent crime rate per 100,000 (2022) |
| rank | INT | Rank 1=most dangerous |
| vs_national | FLOAT | % above/below national average |

### `city_homicide`
| Column | Unit | Description |
|---|---|---|
| city | VARCHAR | City name and state abbreviation |
| homicide_rate | FLOAT | Homicide rate per 100,000 (2022) |
| times_national_avg | FLOAT | Multiples of the 6.3 national average |
| rank | INT | Rank 1=highest rate |

---

## Key Definitions

**Violent Crime (FBI UCR):** Murder/non-negligent manslaughter, rape,
robbery, and aggravated assault.

**Property Crime:** Burglary, larceny-theft, motor vehicle theft,
and arson (arson not included in aggregate totals).

**Rate:** Incidents per 100,000 population — allows comparison
across different-sized jurisdictions.

**NIBRS Transition (2021):** The FBI transitioned from Summary UCR
to NIBRS in 2021. Some agencies did not participate in 2021,
affecting comparability. Use 2021 data with caution.

---

## Important Caveats

1. **Reporting varies:** Not all agencies report to UCR every year.
2. **Definitions differ:** "Rape" uses legacy FBI definition in this dataset.
3. **Dark figure:** All crime data undercounts actual crime — unreported crimes
   are not captured. Estimates suggest only 50-60% of violent crimes are reported.
4. **Population denominators:** Rates use Census Bureau population estimates.
5. **Alaska anomaly:** Alaska's high violent crime rate is partly explained by
   remote population distribution and high rates of domestic violence reporting.
