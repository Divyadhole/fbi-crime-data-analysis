# Key Findings — FBI Crime Data Analysis

## The One Number That Captures Everything
**St. Louis, MO: 65.4 homicides per 100,000 people.**
The national average is 6.3. St. Louis is **10.4x the national average.**
That means a St. Louis resident faces a homicide risk similar to
some of the most dangerous countries in the world.

---

## Finding 1: COVID Was the Biggest Crime Story of the Decade

In 2020, homicides spiked **+56% in a single year** — the largest
single-year increase ever recorded in FBI UCR data.

Statistical validation:
- Mann-Whitney U test: p = 0.017 (significant)
- Cohen's d = 4.28 (extraordinarily large effect)
- Pre-COVID mean: 5.1/100k | COVID-era mean: 7.3/100k

What caused it? Criminologists point to:
1. Police pulling back from proactive enforcement
2. Court system shutdowns — fewer deterrence effects
3. Economic stress and unemployment
4. Mental health crisis and isolation

**Robbery went down** -10% in the same year — because people stayed
home and there were fewer victims on streets. Crime didn't uniformly
increase. It shifted in type.

---

## Finding 2: Good News — Property Crime Has Fallen 21% Since 2015

Property crime (burglary, larceny, motor vehicle theft) has declined
every year from 2015 to 2020.

Linear regression:
- Slope: **-89.4 per year** (significant, p < 0.001)
- R² = 0.941 — extremely consistent trend
- 2015: 2,487/100k → 2022: 1,954/100k = **-21.4%**

This is likely driven by:
- Improved vehicle security (engine immobilizers)
- Better home security systems
- Reduced "hot products" for theft (less cash in society)

---

## Finding 3: Alaska Is an Outlier — For Complicated Reasons

Alaska's violent crime rate: **867.1 per 100,000** — the highest in the nation.
The national average: 380.7.

This is not simply "more crime." Alaska's elevated rate reflects:
1. Remote communities with limited law enforcement access
2. High rates of domestic violence (historically underreported elsewhere)
3. Substance abuse challenges in isolated communities
4. Population distribution: few urban centers, many remote villages

Alaska's homicide rate is not dramatically higher — it's the assault
and sexual assault categories that drive the violent crime total.

---

## Finding 4: The Geography of Homicide

The 10 most dangerous cities for homicide share common characteristics:
- Post-industrial Midwest/South (St. Louis, Detroit, Baltimore, Cleveland)
- Economic disinvestment and concentrated poverty
- Legacy of redlining and residential segregation
- Weak gun regulation at state level

The 5 safest tracked cities:
- Sun Belt cities with younger populations (Austin, San Diego)
- Northeast coastal cities with stricter gun laws (Boston, NYC)

---

## Data Limitations

**The Dark Figure:** FBI UCR only counts reported crimes.
Estimates suggest only ~50% of violent crimes and ~35% of sexual
assaults are reported to police. The true crime rate is higher.

**2021 Comparability:** The FBI transitioned to NIBRS in 2021.
Many agencies didn't report — 2021 national figures are estimated.
Use with caution for year-over-year comparisons.

**Counting differences:** Each state defines "violent crime"
slightly differently. Interstate comparisons have limits.
