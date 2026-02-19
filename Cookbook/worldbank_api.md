# Cookbook: API הבנק העולמי (World Bank)

> הבנק העולמי מספק נתונים על **200+ מדינות** מ-1960 ועד היום.
> החבילה `wbgapi` היא הדרך הנוחה ביותר ב-Python.

---

## התקנה

```bash
pip install wbgapi pandas matplotlib
```

---

## אינדיקטורים חשובים

| קוד | תיאור |
|---|---|
| `NY.GDP.MKTP.KD.ZG` | צמיחת תמ"ג (%, מחירים קבועים) |
| `NY.GDP.PCAP.KD` | תמ"ג לנפש (דולר קבוע 2015) |
| `FP.CPI.TOTL.ZG` | אינפלציה (CPI, % שנתי) |
| `SL.UEM.TOTL.ZS` | אחוז האבטלה (מכלל כוח העבודה) |
| `NE.TRD.GNFS.ZS` | סחר בין-לאומי (% מ-GDP) |
| `GC.DOD.TOTL.GD.ZS` | חוב ממשלתי (% מ-GDP) |
| `SP.POP.TOTL` | אוכלוסייה כוללת |
| `SI.POV.GINI` | מדד ג'יני (אי-שוויון) |

> חיפוש אינדיקטורים: `wb.series.search("unemployment")`

---

## קוד Python מלא

```python
"""
worldbank_api.py – נתוני הבנק העולמי
======================================
pip install wbgapi pandas matplotlib
"""

import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# דוגמה 1: נתוני ישראל
# ==========================================

# צמיחת תמ"ג ישראל 2000–2024
df_isr = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy="ISR",
    time=range(2000, 2025)
)
df_isr.index.name = "year"
df_isr.columns = ["gdp_growth"]
df_isr = df_isr.dropna().reset_index()
print("צמיחת תמ\"ג ישראל:")
print(df_isr.tail(10))


# ==========================================
# דוגמה 2: השוואה בין-מדינתית
# ==========================================

countries = {
    "ISR": "ישראל",
    "USA": "ארה\"ב",
    "DEU": "גרמניה",
    "TUR": "טורקיה",
    "GRC": "יוון",
}

df_compare = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=list(countries.keys()),
    time=range(2010, 2025)
).T  # שנים בשורות, מדינות בעמודות

df_compare.index.name = "year"
df_compare.index = df_compare.index.str.replace("YR", "").astype(int)
df_compare.columns = [countries.get(c, c) for c in df_compare.columns]
print("\nהשוואה בין-מדינתית:")
print(df_compare.tail(5))


# ==========================================
# דוגמה 3: מדדים מרובים עבור ישראל
# ==========================================

indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG":    "inflation",
    "SL.UEM.TOTL.ZS":    "unemployment",
    "GC.DOD.TOTL.GD.ZS": "govt_debt_pct_gdp",
}

frames = []
for code, name in indicators.items():
    df_tmp = wb.data.DataFrame(code, economy="ISR",
                                time=range(2010, 2025))
    df_tmp.index.name = "year"
    df_tmp.columns = [name]
    frames.append(df_tmp)

df_multi = pd.concat(frames, axis=1).dropna(how="all").reset_index()
df_multi["year"] = df_multi["year"].str.replace("YR", "").astype(int)
print("\nמדדים מרובים ישראל:")
print(df_multi)


# ==========================================
# גרף: השוואה בין-מדינתית
# ==========================================

fig, ax = plt.subplots(figsize=(12, 6))
colors = ["steelblue", "tomato", "green", "purple", "orange"]

for (col, label), color in zip(df_compare.items(), colors):
    ax.plot(df_compare.index, col, label=label, color=color,
            linewidth=2, marker="o", markersize=4)

ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("השוואת צמיחת תמ\"ג 2010–2024", fontsize=14)
ax.set_xlabel("שנה")
ax.set_ylabel("% שינוי שנתי")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
fig.text(0.5, 0.01, "מקור: World Bank Open Data",
         ha="center", fontsize=9, color="gray")
plt.tight_layout()
plt.savefig("worldbank_compare.png", dpi=150)
plt.show()
```

---

## חיפוש אינדיקטורים

```python
import wbgapi as wb

# חפש לפי מילת מפתח
results = wb.series.search("unemployment")
for r in list(results)[:5]:
    print(r['id'], '-', r['value'])

# מידע על מדינה
print(wb.economy.get("ISR"))

# רשימת כל מדינות ה-OECD
oecd_members = wb.region.members("OEC")
print(oecd_members[:10])
```

---

## שמירה לקובץ (Google Drive)

```python
# שמור ל-CSV (לא ל-Git!)
df_multi.to_csv("israel_macro_worldbank.csv", index=False, encoding="utf-8-sig")
print("נשמר – העלה ל-Google Drive!")
```

---

*עודכן: 2025 | מקור: [data.worldbank.org](https://data.worldbank.org)*
