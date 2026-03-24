"""
src/charts.py — FBI Crime Data visualizations
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
import seaborn as sns
from pathlib import Path

P = {"red":"#A32D2D","teal":"#1D9E75","blue":"#185FA5","amber":"#BA7517",
     "purple":"#534AB7","coral":"#D85A30","neutral":"#5F5E5A","mid":"#B4B2A9",
     "green":"#2d7d2d","orange":"#c2571a"}

BASE = {"figure.facecolor":"white","axes.facecolor":"#FAFAF8",
        "axes.spines.top":False,"axes.spines.right":False,
        "axes.spines.left":False,"axes.grid":True,
        "axes.grid.axis":"y","grid.color":"#ECEAE4","grid.linewidth":0.6,
        "font.family":"DejaVu Sans","axes.titlesize":12,
        "axes.titleweight":"bold","axes.labelsize":10,
        "xtick.labelsize":8.5,"ytick.labelsize":9,
        "xtick.bottom":False,"ytick.left":False}

def save(fig, path):
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {Path(path).name}")


def chart_national_trend(df, path):
    """Violent vs property crime rates 2015-2022."""
    with plt.rc_context({**BASE,"axes.grid.axis":"both"}):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

        # Violent crime
        ax1.plot(df["year"], df["violent"], "o-", color=P["red"],
                 lw=2.5, markersize=7, label="Violent Crime")
        ax1.fill_between(df["year"], df["violent"], alpha=0.1, color=P["red"])
        ax1.axvspan(2019.6, 2020.4, alpha=0.12, color=P["amber"])
        ax1.text(2020, df["violent"].max()*0.92, "COVID\n+5.7%", ha="center",
                 fontsize=8.5, color=P["amber"], fontweight="bold")
        ax1.set_ylabel("Rate per 100,000 population")
        ax1.set_title("Violent Crime Rate 2015-2022")
        ax1.spines["left"].set_visible(True); ax1.spines["bottom"].set_visible(True)
        ax1.set_xticks(df["year"]); ax1.tick_params(axis="x", rotation=45)

        # Property crime (long-term decline)
        ax2.plot(df["year"], df["property"], "o-", color=P["blue"],
                 lw=2.5, markersize=7, label="Property Crime")
        ax2.fill_between(df["year"], df["property"], alpha=0.1, color=P["blue"])
        drop = (df[df["year"]==2022]["property"].values[0] -
                df[df["year"]==2015]["property"].values[0])
        ax2.annotate(f"{drop:+.0f}\nsince 2015",
                    xy=(2022, df[df["year"]==2022]["property"].values[0]),
                    xytext=(2021, 2300), fontsize=8.5, color=P["blue"],
                    fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=P["blue"], lw=1))
        ax2.set_ylabel("Rate per 100,000 population")
        ax2.set_title("Property Crime Rate 2015-2022\n(Steady Long-Term Decline)")
        ax2.spines["left"].set_visible(True); ax2.spines["bottom"].set_visible(True)
        ax2.set_xticks(df["year"]); ax2.tick_params(axis="x", rotation=45)

        fig.suptitle("US Crime Rates 2015-2022 — FBI UCR\n"
                     "Violent crime spiked in 2020 · Property crime declining long-term",
                     fontsize=12, fontweight="bold")
        fig.tight_layout()
        save(fig, path)


def chart_homicide_trend(df, path):
    """Homicide rate with COVID spike highlighted."""
    with plt.rc_context({**BASE,"axes.grid.axis":"both"}):
        fig, ax = plt.subplots(figsize=(11, 5.5))
        ax.plot(df["year"], df["homicide"], "o-", color=P["red"],
                lw=2.8, markersize=8, zorder=4)
        ax.fill_between(df["year"], df["homicide"], alpha=0.15, color=P["red"])

        # 3-year rolling avg
        rolling = df["homicide"].rolling(3, min_periods=1).mean()
        ax.plot(df["year"], rolling, "--", color=P["neutral"],
                lw=1.5, alpha=0.7, label="3-yr rolling avg")

        # Annotate the COVID spike
        ax.annotate("COVID-19 pandemic\nHomicide +56% in 2020",
                    xy=(2020, 7.8), xytext=(2017.5, 7.6),
                    fontsize=9, color=P["red"], fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=P["red"], lw=1.5))

        # Annotate peak
        ax.scatter([2020, 2021], [7.8, 7.8], color=P["red"], s=120,
                   zorder=5, edgecolors="white", linewidths=1.5)

        ax.set_ylabel("Homicides per 100,000 population")
        ax.set_title("US Homicide Rate 2015-2022 — FBI UCR\n"
                     "Largest single-year spike (+56%) since tracking began")
        ax.legend(fontsize=9)
        ax.spines["left"].set_visible(True); ax.spines["bottom"].set_visible(True)
        ax.set_xticks(df["year"])
        fig.tight_layout()
        save(fig, path)


def chart_state_ranking(df_state, path):
    """State violent crime rankings 2022."""
    top = df_state.sort_values("violent_rate", ascending=True).tail(15)
    tier_colors = {
        "Danger Zone":    P["red"],
        "Above Average":  P["coral"],
        "Near Average":   P["amber"],
        "Below Average":  P["teal"],
    }

    def tier(r):
        if r > 600: return "Danger Zone"
        if r > 400: return "Above Average"
        if r > 300: return "Near Average"
        return "Below Average"

    colors = [tier_colors[tier(r)] for r in top["violent_rate"]]

    with plt.rc_context({**BASE,"axes.grid.axis":"x"}):
        fig, ax = plt.subplots(figsize=(11, 6.5))
        bars = ax.barh(top["state"], top["violent_rate"],
                       color=colors, height=0.65, alpha=0.88)
        ax.axvline(380.7, color=P["neutral"], lw=1.5, linestyle="--",
                   label="National avg: 380.7")
        for bar, v in zip(bars, top["violent_rate"]):
            ax.text(v+4, bar.get_y()+bar.get_height()/2,
                    f"{v:.0f}", va="center", fontsize=9, fontweight="bold")
        patches = [mpatches.Patch(color=v, alpha=0.88, label=k)
                   for k,v in tier_colors.items()]
        ax.legend(handles=patches+[
            plt.Line2D([0],[0],color=P["neutral"],lw=1.5,
                       linestyle="--",label="National avg 380.7")],
            fontsize=8.5)
        ax.set_xlabel("Violent Crime Rate per 100,000 (2022)")
        ax.set_title("Top 15 Most Dangerous States by Violent Crime Rate 2022\n"
                     "Source: FBI UCR — Alaska & New Mexico lead nation")
        fig.tight_layout()
        save(fig, path)


def chart_city_homicides(df_city, path):
    """City homicide rate comparison."""
    df_city = df_city.sort_values("homicide_rate", ascending=True)
    colors = [P["red"] if r > 20 else P["coral"] if r > 10
              else P["amber"] if r > 6 else P["teal"]
              for r in df_city["homicide_rate"]]

    with plt.rc_context({**BASE,"axes.grid.axis":"x"}):
        fig, ax = plt.subplots(figsize=(11, 7))
        bars = ax.barh(df_city["city"], df_city["homicide_rate"],
                       color=colors, height=0.65, alpha=0.88)
        ax.axvline(6.3, color=P["neutral"], lw=1.5, linestyle="--",
                   label="National avg: 6.3")
        for bar, v in zip(bars, df_city["homicide_rate"]):
            mult = v / 6.3
            ax.text(v+0.3, bar.get_y()+bar.get_height()/2,
                    f"{v:.1f}  ({mult:.1f}x)", va="center",
                    fontsize=8.5, fontweight="bold")
        ax.legend(fontsize=9)
        ax.set_xlabel("Homicides per 100,000 population (2022)")
        ax.set_title("City Homicide Rates 2022 vs National Average\n"
                     "Source: FBI UCR — St. Louis 65.4/100k = 10x national avg")
        fig.tight_layout()
        save(fig, path)


def chart_covid_crime_shift(df_covid, path):
    """COVID impact: which crimes went up vs down."""
    df_covid = df_covid.sort_values("pct_change", ascending=True)
    colors = [P["red"] if v > 0 else P["teal"]
              for v in df_covid["pct_change"]]
    labels = df_covid["crime_type"].str.replace("_", " ").str.title()

    with plt.rc_context({**BASE,"axes.grid.axis":"x"}):
        fig, ax = plt.subplots(figsize=(11, 5))
        bars = ax.barh(labels, df_covid["pct_change"],
                       color=colors, height=0.6, alpha=0.88)
        ax.axvline(0, color="#333", lw=0.8)
        for bar, v in zip(bars, df_covid["pct_change"]):
            xpos = v+0.5 if v >= 0 else v-0.5
            ha = "left" if v >= 0 else "right"
            ax.text(xpos, bar.get_y()+bar.get_height()/2,
                    f"{v:+.1f}%", va="center", fontsize=9.5,
                    fontweight="bold", ha=ha)
        ax.set_xlabel("% Change 2019 vs 2020 (COVID year)")
        ax.set_title("COVID-19 Changed Crime in Opposite Directions\n"
                     "Red = increased · Green = decreased | FBI UCR 2020")
        fig.tight_layout()
        save(fig, path)


def chart_crime_composition(df, path):
    """How crime composition (violent vs property) shifted 2015-2022."""
    with plt.rc_context({**BASE,"axes.grid.axis":"both"}):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

        crimes = ["robbery","agg_assault","burglary","larceny","mvt","homicide"]
        labels = ["Robbery","Agg Assault","Burglary","Larceny","MVT","Homicide"]
        colors = [P["purple"],P["red"],P["blue"],P["teal"],P["amber"],P["coral"]]

        for ax, (crime, label, color) in zip(axes[:2], zip(
                ["violent","property"], ["Violent","Property"],
                [P["red"],P["blue"]])):
            ax.plot(df["year"], df[crime], "o-", color=color,
                    lw=2.5, markersize=7)
            ax.fill_between(df["year"], df[crime], alpha=0.1, color=color)
            ax.set_title(f"{label} Crime Rate")
            ax.set_ylabel("per 100,000"); ax.set_xlabel("")
            ax.spines["left"].set_visible(True)
            ax.spines["bottom"].set_visible(True)
            ax.set_xticks(df["year"]); ax.tick_params(axis="x", rotation=45)

        # Sub-crime breakdown 2022 bar
        ax3 = axes[2]
        vals_2022 = [df[df["year"]==2022][c].values[0] for c in crimes]
        ax3.barh(labels, vals_2022, color=colors, height=0.6, alpha=0.88)
        for v, label in zip(vals_2022, labels):
            ax3.text(v+1, labels.index(label),
                     f"{v:.0f}", va="center", fontsize=8.5)
        ax3.set_xlabel("Rate per 100,000 (2022)")
        ax3.set_title("Crime Category Breakdown\n2022")
        ax3.spines["bottom"].set_visible(True)
        ax3.grid(axis="x")
        ax3.grid(axis="y", visible=False)

        fig.suptitle("FBI UCR Crime Composition 2015-2022",
                     fontsize=12, fontweight="bold")
        fig.tight_layout()
        save(fig, path)
