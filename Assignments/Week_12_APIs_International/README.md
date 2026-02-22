# שבוע 12 – APIs בין-לאומיים: השוואה גלובלית עם בנק עולמי, OECD ו-FRED

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=R67XsEXXGQ8 >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=OPEcI9a5m-c >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=tI8L4c0qH14 >}}

:::
## מה נלמד השבוע?

| נושא | זמן משוער |
|---|---|
| World Bank API: `wbgapi` | 90 דקות |
| OECD SDMX API | 75 דקות |
| FRED API: נתוני ארה"ב | 60 דקות |
| IMF WEO: תחזיות עולמיות | 45 דקות |
| פרויקט: השוואת ישראל ל-OECD | 120 דקות |
| **סה"כ** | **~7 שעות** |

---

## חלק א – World Bank API: `wbgapi`

### התקנה והיכרות

```bash
pip install wbgapi
```

`wbgapi` היא ספרייה רשמית של הבנק העולמי. נוחה מאוד לשימוש.

```python
import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt

# חיפוש אינדיקטורים
results = wb.series.search("GDP growth")
for r in results:
    print(r["id"], "|", r["value"])
# NY.GDP.MKTP.KD.ZG | GDP growth (annual %)
# NY.GDP.PCAP.KD.ZG | GDP per capita growth...

# מידע על מדינה
wb.economy.info("ISR")  # Israel
wb.economy.info("DEU")  # Germany
```

### אינדיקטורים נפוצים

| קוד | תיאור |
|---|---|
| `NY.GDP.MKTP.KD.ZG` | צמיחת תמ"ג שנתית % |
| `NY.GDP.PCAP.CD` | תמ"ג לנפש (USD) |
| `FP.CPI.TOTL.ZG` | אינפלציה CPI % |
| `SL.UEM.TOTL.ZS` | שיעור אבטלה % |
| `NE.EXP.GNFS.ZS` | ייצוא % מתמ"ג |
| `NE.IMP.GNFS.ZS` | ייבוא % מתמ"ג |
| `GC.DOD.TOTL.GD.ZS` | חוב ממשלתי % מתמ"ג |
| `SP.POP.TOTL` | אוכלוסייה |
| `SE.XPD.TOTL.GD.ZS` | הוצאות חינוך % מתמ"ג |
| `SH.XPD.CHEX.GD.ZS` | הוצאות בריאות % מתמ"ג |

### שליפת נתונים

```python
# ישראל בלבד – 10 שנים אחרונות
gdp_isr = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",  # אינדיקטור
    economy="ISR",          # מדינה
    time=range(2014, 2024), # שנים
    labels=True
)
print(gdp_isr)

# כמה מדינות
countries = ["ISR", "DEU", "USA", "GBR", "FRA", "JPN", "KOR"]
gdp_multi = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=countries,
    time=range(2014, 2024),
    labels=True
)
print(gdp_multi)

# כמה אינדיקטורים בבת אחת
indicators = ["NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS"]
multi_indicators = wb.data.DataFrame(
    indicators,
    economy="ISR",
    time=range(2010, 2024)
)
```

### ניקוי ועיבוד

```python
# wbgapi מחזיר בפורמט Wide (שנים כעמודות)
# צריך Transpose ל-Long

gdp_isr = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=countries,
    time=range(2014, 2024)
).T  # Transpose: שנים כשורות, מדינות כעמודות

gdp_isr.index = gdp_isr.index.astype(int)  # שנים כint
gdp_isr.index.name = "year"

print(gdp_isr.head())
#        ISR   DEU   USA   GBR   FRA
# year
# 2014   3.5   2.1   2.5   3.0   1.0
# 2015   2.5   1.5   3.1   2.4   1.1
```

### השוואת ישראל ל-G7

```python
g7_and_israel = ["ISR", "USA", "GBR", "FRA", "DEU", "JPN", "ITA", "CAN"]

gdp_comparison = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=g7_and_israel,
    time=range(2018, 2024)
).T

gdp_comparison.columns = [
    "Israel", "USA", "UK", "France", "Germany", "Japan", "Italy", "Canada"
]

# גרף השוואה
fig, ax = plt.subplots(figsize=(12, 6))
for col in gdp_comparison.columns:
    lw = 3 if col == "Israel" else 1
    alpha = 1 if col == "Israel" else 0.6
    color = "red" if col == "Israel" else None
    ax.plot(gdp_comparison.index, gdp_comparison[col],
            label=col, linewidth=lw, alpha=alpha, color=color)

ax.axhline(0, color="black", linewidth=0.8)
ax.axvspan(2019.5, 2020.5, alpha=0.1, color="gray")
ax.set_title("צמיחת תמ\"ג: ישראל מול G7 (2018-2023)", fontsize=14)
ax.set_ylabel("צמיחה שנתית (%)")
ax.legend(bbox_to_anchor=(1.01, 1), fontsize=9)
plt.tight_layout()
plt.savefig("israel_vs_g7_gdp.png", dpi=150)
plt.show()
```

---

## חלק ב – OECD API: השוואת 38 מדינות

### OECD SDMX REST API

OECD מספקת SDMX API (כמו בנק ישראל):

```
https://sdmx.oecd.org/public/rest/data/{datasetId}/{filterExpression}?{queryString}
```

```python
import requests
import pandas as pd

def fetch_oecd(dataset, subject, countries, measure="PC_GDP",
               start_year=2015, end_year=2023):
    """
    שולפת נתונים מ-OECD.

    datasets נפוצים:
    - NAAG: National Accounts (GDP, expenditure)
    - LFS_SEXAGE_I_R: Labour Force Statistics
    - PRICES_CPI: Consumer Prices
    - MEI: Main Economic Indicators
    """
    country_str = "+".join(countries)
    url = (
        f"https://sdmx.oecd.org/public/rest/data/{dataset}/"
        f"{country_str}.{subject}.{measure}.A"
        f"?startPeriod={start_year}&endPeriod={end_year}"
        f"&format=jsondata"
    )

    print(f"שולף OECD: {dataset}/{subject}...")
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"שגיאה: {e}")
        return None

    # פרסור
    obs_vals = data["data"]["dataSets"][0]["series"]
    dim_info = data["data"]["structure"]["dimensions"]["series"]

    country_names = [v["name"] for v in dim_info[0]["values"]]
    periods = [v["name"] for v in
               data["data"]["structure"]["dimensions"]["observation"][0]["values"]]

    records = []
    for series_key, series_data in obs_vals.items():
        c_idx = int(series_key.split(":")[0])
        country = country_names[c_idx]
        for obs_key, obs_val in series_data["observations"].items():
            records.append({
                "country": country,
                "year": int(periods[int(obs_key)]),
                "value": obs_val[0]
            })

    df = pd.DataFrame(records)
    return df.pivot(index="year", columns="country", values="value")

# שימוש: אבטלה ב-OECD
oecd_countries = ["ISR", "USA", "GBR", "DEU", "FRA", "JPN", "KOR", "SWE", "NOR"]
unemployment = fetch_oecd(
    dataset="LFS_SEXAGE_I_R",
    subject="UNE_RATE",
    countries=oecd_countries,
    measure="PC_LABOUR_FORCE",
    start_year=2015,
    end_year=2023
)
print(unemployment)
```

### נתוני OECD דרך ה-package הרשמי

```python
# חלופה פשוטה יותר: pandas_datareader
pip install pandas-datareader

from pandas_datareader import data as pdr
import pandas as pd

# OECD Health Statistics
oecd_health = pdr.get_data_oecd(
    "HEALTH_STAT",
    subject=["HEXP"],      # הוצאות בריאות
    country=["ISR", "DEU", "FRA", "USA"],
    startdt="2010",
    enddt="2023"
)
```

---

## חלק ג – FRED API: נתוני ארה"ב ועולמיים

### FRED = Federal Reserve Economic Data

FRED של הפד של סט לואיס מכיל 800,000+ סדרות נתונים – לא רק ארה"ב!

### התקנה + API Key

```bash
pip install fredapi
```

**קבל API Key חינמי:** [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)

```python
from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))
```

### סדרות נפוצות

| קוד | תיאור |
|---|---|
| `UNRATE` | אבטלה ארה"ב |
| `CPIAUCSL` | CPI ארה"ב |
| `FEDFUNDS` | ריבית הפד |
| `DFF` | Fed Funds Rate יומי |
| `T10Y2Y` | פרמיית סיכון (10Y-2Y) |
| `DEXILUS` | שע"ח ILS/USD |
| `DEXJPUS` | שע"ח JPY/USD |
| `BRENT` | מחיר נפט ברנט |
| `GOLDAMGBD228NLBM` | מחיר זהב |
| `VIXCLS` | מדד VIX (פחד) |

```python
import pandas as pd
import matplotlib.pyplot as plt

# שליפת ריבית הפד
fed_rate = fred.get_series("FEDFUNDS", observation_start="2019-01-01")
fed_rate = fed_rate.resample("Q").mean()

# שליפת CPI ארה"ב
us_cpi = fred.get_series("CPIAUCSL", observation_start="2019-01-01")
us_cpi_yoy = us_cpi.pct_change(12) * 100  # שינוי שנתי
us_cpi_yoy = us_cpi_yoy.resample("Q").mean()

# שליפת מחיר נפט (משפיע על ישראל!)
oil = fred.get_series("DCOILBRENTEU", observation_start="2019-01-01")
oil = oil.resample("Q").mean()

# מיזוג
global_df = pd.concat([fed_rate, us_cpi_yoy, oil], axis=1)
global_df.columns = ["fed_rate", "us_inflation", "brent_oil"]
global_df = global_df.dropna()

print(global_df.tail(8))

# ניתוח: האם מחיר הנפט מסביר אינפלציה?
corr = global_df[["us_inflation", "brent_oil"]].corr()
print(f"\nקורלציה נפט-אינפלציה: {corr.loc['us_inflation', 'brent_oil']:.3f}")
```

---

## חלק ד – IMF World Economic Outlook

### WEO Dataset

ה-IMF מפרסם תחזיות מאקרו לכ-190 מדינות פעמיים בשנה.

```python
import pandas as pd
import requests

def fetch_imf_weo(country_code, indicator, years):
    """
    שולפת נתוני WEO מ-IMF.

    indicators נפוצים:
    NGDP_RPCH = GDP growth rate %
    PCPIPCH   = Inflation %
    LUR       = Unemployment %
    GGXWDG_NGDP = Government debt % of GDP
    BCA_NGDPD = Current account % of GDP
    """
    base = "https://www.imf.org/external/datamapper/api/v1"
    url = f"{base}/{indicator}/{country_code}"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()
        values = data["values"][indicator][country_code]
        df = pd.DataFrame.from_dict(values, orient="index", columns=[indicator])
        df.index = df.index.astype(int)
        df.index.name = "year"
        return df[df.index.isin(years)]
    except Exception as e:
        print(f"שגיאה: {e}")
        return None

# שליפת תחזיות לישראל
years = range(2020, 2026)  # כולל תחזיות עתידיות!
gdp_isr = fetch_imf_weo("ISR", "NGDP_RPCH", years)
inflation_isr = fetch_imf_weo("ISR", "PCPIPCH", years)
debt_isr = fetch_imf_weo("ISR", "GGXWDG_NGDP", years)

imf_israel = pd.concat([gdp_isr, inflation_isr, debt_isr], axis=1)
imf_israel.columns = ["gdp_growth", "inflation", "govt_debt_pct_gdp"]
print(imf_israel)
```

---

## חלק ה – פרויקט מסכם: Israel in the World

```python
"""
israel_global_analysis.py

שאלת מחקר: האם ישראל ביצעה טוב יחסית למדינות ה-OECD
בתקופת הריבית הגבוהה 2022-2024?
"""

import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import requests
import time

print("=" * 60)
print("פרויקט: ישראל בעולם – השוואת ביצועים מאקרו-כלכליים")
print("=" * 60)

# ---- 1. הגדרת מדינות ----
COUNTRIES = {
    "ISR": "Israel",
    "USA": "USA",
    "DEU": "Germany",
    "GBR": "UK",
    "FRA": "France",
    "KOR": "South Korea",
    "CHE": "Switzerland",
    "AUS": "Australia",
}
YEARS = range(2019, 2025)

# ---- 2. שליפת נתונים ----
print("\n[1] שולפת נתוני World Bank...")
wb_indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG":    "inflation",
    "SL.UEM.TOTL.ZS":    "unemployment",
    "GC.DOD.TOTL.GD.ZS": "govt_debt",
    "NE.EXP.GNFS.ZS":    "exports_pct_gdp",
}

all_dfs = {}
for wb_code, name in wb_indicators.items():
    try:
        df = wb.data.DataFrame(
            wb_code,
            economy=list(COUNTRIES.keys()),
            time=list(YEARS)
        ).T
        df.columns = [COUNTRIES.get(c, c) for c in df.columns]
        df.index = df.index.astype(int)
        all_dfs[name] = df
        print(f"  ✓ {name}")
        time.sleep(0.2)
    except Exception as e:
        print(f"  ✗ {name}: {e}")

# ---- 3. ניתוח: ישראל vs. ממוצע OECD ----
print("\n[2] מנתחת ביצועי ישראל...")

gdp = all_dfs.get("gdp_growth")
if gdp is not None:
    gdp["OECD_avg"] = gdp.drop("Israel", axis=1).mean(axis=1)
    gdp["Israel_vs_OECD"] = gdp["Israel"] - gdp["OECD_avg"]

    print("\nצמיחת תמ\"ג: ישראל vs. ממוצע מדינות הנדגמות")
    print(gdp[["Israel", "OECD_avg", "Israel_vs_OECD"]].round(2).to_string())

# ---- 4. ויזואליזציה ----
print("\n[3] יוצרת גרפים...")

fig = plt.figure(figsize=(16, 12))
fig.suptitle("ישראל בעולם: השוואת ביצועים מאקרו-כלכליים 2019-2024",
             fontsize=14, fontweight="bold", y=0.98)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

# גרף 1: צמיחת תמ"ג השוואתית
ax1 = fig.add_subplot(gs[0, :])
if gdp is not None:
    for col in gdp.columns:
        if col == "Israel":
            ax1.plot(gdp.index, gdp[col], "r-o", linewidth=3,
                     markersize=7, label=col, zorder=5)
        elif col in ("OECD_avg", "Israel_vs_OECD"):
            continue
        else:
            ax1.plot(gdp.index, gdp[col], "-", linewidth=1,
                     alpha=0.5, label=col)

    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.axvspan(2021.5, 2022.5, alpha=0.12, color="red",
                label="העלאת ריבית")
    ax1.set_title("צמיחת תמ\"ג שנתית (%)")
    ax1.set_ylabel("% צמיחה")
    ax1.legend(bbox_to_anchor=(1.01, 1), fontsize=8, ncol=1)

# גרף 2: אינפלציה
ax2 = fig.add_subplot(gs[1, 0])
inflation = all_dfs.get("inflation")
if inflation is not None:
    for col in inflation.columns:
        lw = 3 if col == "Israel" else 1
        color = "red" if col == "Israel" else None
        ax2.plot(inflation.index, inflation[col],
                 linewidth=lw, alpha=0.8 if col == "Israel" else 0.5,
                 color=color, label=col)
    ax2.axhline(2, color="gray", linestyle=":", label="יעד 2%")
    ax2.set_title("אינפלציה (%)")
    ax2.set_ylabel("%")
    ax2.legend(fontsize=7)

# גרף 3: אבטלה
ax3 = fig.add_subplot(gs[1, 1])
unemployment = all_dfs.get("unemployment")
if unemployment is not None:
    # boxplot השוואתי
    data_2023 = unemployment.loc[2023].dropna() if 2023 in unemployment.index else None
    if data_2023 is not None:
        ax3.barh(data_2023.index, data_2023.values,
                 color=["red" if c == "Israel" else "steelblue" for c in data_2023.index],
                 alpha=0.8)
        ax3.set_title("שיעור אבטלה 2023 (%)")
        ax3.set_xlabel("%")
        ax3.axvline(data_2023.mean(), color="gray", linestyle="--",
                    label=f"ממוצע: {data_2023.mean():.1f}%")
        ax3.legend()

plt.savefig("israel_global_comparison.png", dpi=150, bbox_inches="tight")
plt.show()

# ---- 5. סיכום מספרי ----
print("\n[4] סיכום ממצאים:")
if gdp is not None and "Israel_vs_OECD" in gdp.columns:
    avg_diff = gdp["Israel_vs_OECD"].mean()
    sign = "עודף" if avg_diff > 0 else "גרעון"
    print(f"  ישראל: {sign} ביצועים ממוצע של {abs(avg_diff):.2f}% לעומת מדינות מדגם")

    pre_2022 = gdp.loc[gdp.index <= 2021, "Israel_vs_OECD"].mean()
    post_2022 = gdp.loc[gdp.index >= 2022, "Israel_vs_OECD"].mean()
    print(f"  לפני 2022: ישראל ב-{pre_2022:+.2f}% ממדינות המדגם")
    print(f"  אחרי 2022: ישראל ב-{post_2022:+.2f}% ממדינות המדגם")

# שמור נתונים
with pd.ExcelWriter("israel_global_data.xlsx", engine="openpyxl") as writer:
    for name, df in all_dfs.items():
        df.to_excel(writer, sheet_name=name[:31])

print("\n✓ הכל נשמר!")
```

---

## משימות השבוע

### משימה 1: World Bank – ניתוח אי-שוויון (30 נקודות)

```python
# שאלת מחקר: כיצד אי-שוויון (Gini) קשור לצמיחה בין מדינות?
# אינדיקטור Gini: SI.POV.GINI

# שלוף Gini + GDP per capita + Unemployment
# לכ-30 מדינות OECD לשנת 2022 (הנתון האחרון זמין)
# צור scatter plot: Gini vs GDP per capita (עם ישראל מודגשת)
# כתוב: מה מיקומה של ישראל?
```

### משימה 2: FRED – גלובל מאקרו (30 נקודות)

שלוף מ-FRED:
- ריבית הפד
- CPI ארה"ב
- VIX (מדד פחד)
- מחיר נפט ברנט
- שע"ח דולר-שקל

ניתח: האם קיים קשר בין ריבית הפד ושע"ח הדולר-שקל?

### משימה 3: Pipeline מאוחד (40 נקודות)

בנה `global_data_hub.py` עם פונקציות:

```python
class GlobalEconomyHub:
    """מאגר נתונים גלובלי."""

    def get_world_bank(self, indicator, countries, years): ...
    def get_fred(self, series_ids): ...
    def compare_israel_to_oecd(self, indicator, year=2023): ...
    def plot_comparison(self, metric, countries, title): ...
    def export_to_excel(self, filename): ...
```

**שאלת מחקר לדוח:**
"האם ישראל הצליחה לגבות ריבית גבוהה מבלי לגרום לנזק גדול יחסית לכלכלות ה-OECD האחרות?"

---

## הגשה

```
Members/YourName/Week_12/
├── global_data_hub.py
├── israel_global_analysis.py
├── israel_global_comparison.png
├── israel_global_data.xlsx
└── global_research_report.md
```

**בדוח:**
```markdown
# ישראל בעולם: השוואת ביצועים מאקרו-כלכליים

## 1. שאלת מחקר
## 2. מתודולוגיה ומקורות
## 3. ממצאים עיקריים
   ### 3.1 צמיחה יחסית
   ### 3.2 ניהול אינפלציה
   ### 3.3 שוק העבודה
## 4. מסקנות
## 5. מגבלות המחקר
```

---

**המודול הבא:** R – אקונומטריקה ומודלים סטטיסטיים → [שבוע 13](../Week_13_R_Basics/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_12_APIs_International/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

