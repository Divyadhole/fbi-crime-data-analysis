"""
src/city_context.py
Contextualizes US city homicide rates against international benchmarks.

Key insight: St. Louis (65.4/100k) has a higher homicide rate than
countries like Brazil (22.4), South Africa (41.2), or Guatemala (16.1).

The US national average (6.3/100k) is still 3x higher than
peer nations like Canada (1.9), UK (1.1), Germany (0.9), Australia (0.9).

Sources:
  US data: FBI UCR 2022
  International: UNODC Global Study on Homicide 2023
  https://www.unodc.org/unodc/en/data-and-analysis/homicide.html
"""

from src.fbi_data import load_cities

# UNODC international homicide rates 2022 (per 100,000)
INTERNATIONAL_RATES = {
    # Peer nations
    "Canada":        1.9,
    "Australia":     0.9,
    "UK":            1.1,
    "Germany":       0.9,
    "France":        1.3,
    "Japan":         0.2,
    # Context
    "US National":   6.3,
    # High-rate comparators
    "Mexico":        24.1,
    "Brazil":        22.4,
    "South Africa":  41.2,
    "El Salvador":   37.1,
}


def compare_cities_to_world():
    cities = load_cities()
    top5 = cities.nlargest(5, "homicide_rate")

    print("US CITY HOMICIDE RATES IN GLOBAL CONTEXT")
    print("-" * 55)
    print(f"\n  {'Country/City':<28} {'Rate':<8} {'vs Peer Avg'}")
    print(f"  {'-'*28} {'-'*8} {'-'*12}")

    peer_avg = sum([INTERNATIONAL_RATES[c] for c in
                    ["Canada","Australia","UK","Germany","France"]]) / 5

    for country, rate in sorted(INTERNATIONAL_RATES.items(),
                                  key=lambda x: x[1]):
        bar = "█" * int(rate / 2)
        print(f"  {country:<28} {rate:<8.1f} {rate/peer_avg:.1f}x peer avg")

    print(f"\n  {'--- US CITIES ---':<28}")
    for _, row in top5.iterrows():
        rate = row["homicide_rate"]
        bar = "█" * int(rate / 2)
        print(f"  {row['city']:<28} {rate:<8.1f} {rate/peer_avg:.1f}x peer avg")

    print(f"\n  Peer nation average (CA/AU/UK/DE/FR): {peer_avg:.1f}/100k")
    print(f"  US national average: 6.3/100k = {6.3/peer_avg:.1f}x peers")
    print(f"  St. Louis: {top5.iloc[0]['homicide_rate']}/100k = "
          f"{top5.iloc[0]['homicide_rate']/peer_avg:.0f}x peers")


if __name__ == "__main__":
    compare_cities_to_world()
