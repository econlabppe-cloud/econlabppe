# שבוע 10 – Pandas מתקדם: Time Series, Merge, ו-Pipeline מלא

> **רמה:** מתקדם – מניח שסיימת שבועות 8-9
> **מטרת השבוע:** לבצע ניתוח כלכלי מלא – מנתונים גולמיים עד גרפים לפרסום

---

## מה נלמד השבוע?

| נושא | זמן משוער |
|---|---|
| Time Series: תאריכים וזמן | 90 דקות |
| resample, rolling, shift | 75 דקות |
| merge, concat, join | 75 דקות |
| pivot_table, melt, stack/unstack | 60 דקות |
| Matplotlib מלא לפרסום | 60 דקות |
| Pipeline נתונים שלם | 90 דקות |
| **סה"כ** | **~8 שעות** |

---

## חלק א – Time Series: עבודה עם תאריכים

### pd.to_datetime() ו-DatetimeIndex

```python
import pandas as pd
import numpy as np

# יצירת DatetimeIndex
dates = pd.date_range(start="2022-01-01", end="2023-12-31", freq="M")  # חודשי
print(dates[:5])
# DatetimeIndex(['2022-01-31', '2022-02-28', '2022-03-31'...])

# יצירת סדרה עתית
np.random.seed(42)
cpi = pd.Series(
    data=np.cumsum(np.random.normal(0.3, 0.1, len(dates))),
    index=dates,
    name="CPI_monthly_change"
)
print(cpi.head())

# המרת עמודה לתאריך
df = pd.DataFrame({
    "date": ["2022-01", "2022-02", "2022-03"],
    "inflation": [4.1, 4.3, 4.5]
})
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
```

### גישה לרכיבי תאריך

```python
df.index.year      # שנה
df.index.month     # חודש (1-12)
df.index.quarter   # רבעון (1-4)
df.index.dayofweek # יום בשבוע (0=שני)

# הוסף כעמודות
df["year"] = df.index.year
df["quarter"] = df.index.quarter
df["month_name"] = df.index.strftime("%b")  # Jan, Feb...
```

### סינון לפי תאריך

```python
# שנה ספציפית
df_2022 = df["2022"]

# טווח תאריכים
df_range = df["2022-06":"2023-03"]

# חודש ספציפי
df_jan = df[df.index.month == 1]
```

---

## חלק ב – Resampling: שינוי תדירות

```python
# נתונים חודשיים → רבעוניים
df_quarterly = df.resample("Q").mean()   # ממוצע לכל רבעון
df_quarterly = df.resample("Q").sum()    # סכום לכל רבעון
df_quarterly = df.resample("Q").last()   # ערך אחרון ברבעון

# נתונים חודשיים → שנתיים
df_annual = df.resample("A").mean()      # "A" = Annual

# תדרים נפוצים:
# "D" = יומי, "W" = שבועי, "M" = חודשי, "Q" = רבעוני, "A" = שנתי

# דוגמה מלאה: BOI ריבית חודשית → שנתית
interest_monthly = pd.DataFrame({
    "date": pd.date_range("2022-01", "2024-01", freq="M"),
    "interest_rate": [0.1]*5 + [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.25,
                                 3.5, 3.75, 4.0, 4.25, 4.5, 4.75]*1 + [4.5]*5
})
interest_monthly = interest_monthly.set_index("date")
annual_avg_rate = interest_monthly.resample("A").mean()
print(annual_avg_rate)
```

---

## חלק ג – Rolling ו-Shift: ניתוח לאורך זמן

### rolling() – ממוצע נע

```python
# ממוצע נע 3 חודשים
df["inflation_ma3"] = df["inflation"].rolling(window=3).mean()

# ממוצע נע 12 חודשים (מגמה שנתית)
df["inflation_ma12"] = df["inflation"].rolling(window=12).mean()

# סטיית תקן נעה (מדד תנודתיות)
df["inflation_vol"] = df["inflation"].rolling(window=6).std()

# min/max נע
df["inflation_max_12m"] = df["inflation"].rolling(12).max()
```

### shift() – ערך מתקופה קודמת

```python
# שינוי Year-over-Year (השוואה לשנה קודמת)
df["inflation_yoy"] = df["inflation"] - df["inflation"].shift(12)  # 12 חודשים קודם

# שינוי Quarter-over-Quarter
df["gdp_qoq"] = df["gdp"].pct_change(periods=1) * 100

# שינוי YoY אחוזים
df["gdp_yoy_pct"] = df["gdp"].pct_change(periods=4) * 100  # 4 רבעונים קודם
```

### diff() – הפרש

```python
# שינוי ריבית מחודש לחודש
df["rate_change"] = df["interest_rate"].diff()

# שינוי מצטבר
df["cumulative_inflation"] = df["inflation"].cumsum()
```

---

## חלק ד – Merge: מיזוג DataFrames

### pd.merge() – כמו JOIN ב-SQL

```python
# DataFrame 1: נתוני מאקרו שנתיים
macro_df = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023],
    "gdp_growth": [3.8, -1.9, 8.6, 6.5, 2.0],
    "inflation":  [0.8, -0.6, 1.5, 5.1, 4.2],
})

# DataFrame 2: נתוני ייצוא
exports_df = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023],
    "exports_bn_usd": [68.6, 58.9, 73.5, 82.1, 75.4],
})

# DataFrame 3: דירוג חינוך OECD
education_df = pd.DataFrame({
    "year": [2019, 2021, 2023],  # רק שנים אי-זוגיות!
    "pisa_score": [488, 492, 490],
})

# INNER JOIN (רק שורות שיש בשתיהן)
merged = pd.merge(macro_df, exports_df, on="year", how="inner")
print(merged)

# LEFT JOIN (כל macro, גם אם אין exports)
merged_left = pd.merge(macro_df, education_df, on="year", how="left")
# שנים 2020, 2022 יקבלו NaN ב-pisa_score

# מיזוג על עמודות בשמות שונים
df1 = pd.DataFrame({"yr": [2022, 2023], "gdp": [6.5, 2.0]})
df2 = pd.DataFrame({"year": [2022, 2023], "exports": [82.1, 75.4]})
merged_diff = pd.merge(df1, df2, left_on="yr", right_on="year").drop("year", axis=1)

# מיזוג על כמה עמודות
housing_df = pd.DataFrame({
    "year": [2022, 2022, 2023, 2023],
    "district": ["תל אביב", "ירושלים", "תל אביב", "ירושלים"],
    "avg_price": [4050000, 2720000, 3900000, 2650000]
})
population_df = pd.DataFrame({
    "year": [2022, 2022, 2023, 2023],
    "district": ["תל אביב", "ירושלים", "תל אביב", "ירושלים"],
    "population": [1380000, 1100000, 1400000, 1120000]
})
combined = pd.merge(housing_df, population_df, on=["year", "district"])
combined["price_per_capita"] = combined["avg_price"] / combined["population"]
```

### pd.concat() – הוספת שורות/עמודות

```python
# הוסף שורות (stack vertically)
df_2022 = pd.DataFrame({"year": [2022], "gdp": [6.5]})
df_2023 = pd.DataFrame({"year": [2023], "gdp": [2.0]})
combined = pd.concat([df_2022, df_2023], ignore_index=True)

# הוסף עמודות (stack horizontally)
gdp_col = pd.DataFrame({"gdp_growth": [3.8, -1.9, 8.6]})
inflation_col = pd.DataFrame({"inflation": [0.8, -0.6, 1.5]})
combined = pd.concat([gdp_col, inflation_col], axis=1)
```

---

## חלק ה – pivot_table, melt, stack/unstack

### pivot_table – ניתוח צולב

```python
housing_data = pd.DataFrame({
    "year":     [2022]*4 + [2023]*4,
    "quarter":  [1,2,3,4]*2,
    "district": ["ת''א","ירושלים"]*4,
    "price":    [3800000, 3950000, 4100000, 4050000,
                 3900000, 3850000, 3820000, 3780000],
})

# Pivot: שורות=שנה, עמודות=מחוז, ערכים=ממוצע מחיר
pivot = housing_data.pivot_table(
    values="price",
    index="year",
    columns="district",
    aggfunc="mean"
)
print(pivot)

# עם מספר פונקציות
pivot_detailed = housing_data.pivot_table(
    values="price",
    index="quarter",
    columns=["year", "district"],
    aggfunc=["mean", "max"]
)
```

### melt – Wide → Long (מה שUnpivot עושה ב-Power Query)

```python
wide_df = pd.DataFrame({
    "year":       [2021, 2022, 2023],
    "tel_aviv":   [3700000, 4050000, 3900000],
    "jerusalem":  [2500000, 2720000, 2650000],
    "haifa":      [1600000, 1780000, 1720000],
})

long_df = wide_df.melt(
    id_vars="year",          # עמודות שלא מומסים
    var_name="district",     # שם עמודת הקטגוריה
    value_name="avg_price"   # שם עמודת הערך
)
print(long_df)
# year | district  | avg_price
# 2021 | tel_aviv  | 3700000
# 2021 | jerusalem | 2500000
# ...
```

### stack / unstack

```python
# stack: עמודות → שורות (Wide → Long)
stacked = pivot.stack()

# unstack: שורות → עמודות (Long → Wide)
unstacked = stacked.unstack("district")
```

---

## חלק ו – Matplotlib מלא לפרסום

### מבנה Figure/Axes

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Figure מורכב עם GridSpec
fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])    # כל השורה הראשונה
ax2 = fig.add_subplot(gs[1, 0])    # שמאל תחתון
ax3 = fig.add_subplot(gs[1, 1])    # אמצע תחתון
ax4 = fig.add_subplot(gs[1, 2])    # ימין תחתון
```

### עיצוב מקצועי

```python
# Economist-style plot
plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,      # ללא מסגרת עליונה
    "axes.spines.right": False,    # ללא מסגרת ימנית
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

fig, ax = plt.subplots(figsize=(10, 5))

# צמיחה עם background shading
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
gdp = [4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1]

ax.bar(years, gdp,
       color=["#2ca02c" if g > 0 else "#d62728" for g in gdp],
       alpha=0.8, edgecolor="white", linewidth=0.5)

# הדגשת שנת הקורונה
ax.axvspan(2019.5, 2020.5, alpha=0.1, color="gray", label="קורונה")

# קו ממוצע
avg = sum(gdp) / len(gdp)
ax.axhline(avg, color="navy", linestyle="--", linewidth=1.5,
           label=f"ממוצע: {avg:.1f}%")

# אנוטציות
ax.annotate("קורונה", xy=(2020, -1.9), xytext=(2020.5, -1.5),
            arrowprops=dict(arrowstyle="->", color="gray"),
            color="gray", fontsize=9)

# עיצוב
ax.set_title("צמיחת תמ\"ג ישראל 2018-2024", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("שיעור צמיחה (%)", fontsize=11)
ax.set_xlabel("שנה", fontsize=11)
ax.legend(loc="upper right")
ax.set_ylim(-4, 11)

# מקור נתונים
fig.text(0.01, 0.01, "מקור: בנק ישראל", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("gdp_publication.png", dpi=300, bbox_inches="tight",
            facecolor="white")
plt.show()
```

---

## חלק ז – Pipeline מלא: מנתונים גולמיים לניתוח

### הגישה המקצועית

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================
# STEP 1: LOAD & VALIDATE
# =============================================================
print("שלב 1: טעינת נתונים...")

macro = pd.read_csv("macro_annual.csv", parse_dates=False)
housing = pd.read_csv("housing_quarterly.csv")

assert not macro.isnull().all().any(), "עמודה שלמה ריקה ב-macro!"
print(f"  Macro: {macro.shape[0]} שורות")
print(f"  Housing: {housing.shape[0]} שורות")

# =============================================================
# STEP 2: CLEAN
# =============================================================
print("\nשלב 2: ניקוי נתונים...")

# macro
macro = macro.drop_duplicates(subset=["year"])
macro = macro[macro["year"].between(2015, 2024)]
macro["year"] = macro["year"].astype(int)

# housing
housing["district"] = housing["district"].str.strip()
housing = housing[housing["avg_price"].between(500000, 10000000)]

print("  ✓ ניקוי הסתיים")

# =============================================================
# STEP 3: ENGINEER FEATURES
# =============================================================
print("\nשלב 3: חישוב פיצ'רים...")

macro["real_interest"] = macro["interest_rate"] - macro["inflation"]
macro["era"] = macro["year"].apply(
    lambda y: "ריבית נמוכה" if y <= 2021 else "ריבית גבוהה"
)

housing_annual = housing.groupby(["year", "district"]).agg(
    avg_price=("avg_price", "mean"),
    total_transactions=("transactions", "sum")
).reset_index()

# =============================================================
# STEP 4: MERGE
# =============================================================
print("\nשלב 4: מיזוג נתונים...")

combined = pd.merge(macro, housing_annual, on="year", how="left")
print(f"  תוצאה: {combined.shape[0]} שורות")

# =============================================================
# STEP 5: ANALYZE
# =============================================================
print("\nשלב 5: ניתוח...")

era_summary = combined.groupby("era").agg({
    "gdp_growth":     ["mean", "std"],
    "inflation":      "mean",
    "real_interest":  "mean",
    "avg_price":      "mean",
    "total_transactions": "sum"
}).round(2)

print(era_summary)

# קורלציות
corr_matrix = combined[
    ["interest_rate", "inflation", "gdp_growth", "avg_price", "total_transactions"]
].corr().round(2)
print("\nמטריצת קורלציות:")
print(corr_matrix)

# =============================================================
# STEP 6: VISUALIZE
# =============================================================
print("\nשלב 6: ויזואליזציה...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("ניתוח שוק הדיור ומדיניות הריבית – ישראל 2015-2024",
             fontsize=14, fontweight="bold")

# גרף 1: ריבית לאורך זמן
ax = axes[0, 0]
ax.step(macro["year"], macro["interest_rate"], color="royalblue", linewidth=2.5)
ax.fill_between(macro["year"], macro["interest_rate"], alpha=0.15, color="royalblue", step="pre")
ax.set_title("ריבית בנק ישראל (%)")
ax.axhline(macro["interest_rate"].mean(), color="gray", linestyle=":", label="ממוצע")
ax.legend()

# גרף 2: אינפלציה vs ריבית
ax = axes[0, 1]
ax.plot(macro["year"], macro["inflation"], "o-", color="orange", label="אינפלציה", linewidth=2)
ax.plot(macro["year"], macro["real_interest"], "s--", color="darkred", label="ריבית ריאלית", linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("אינפלציה מול ריבית ריאלית (%)")
ax.legend()

# גרף 3: מחיר דיור לפי מחוז
if "avg_price" in combined.columns and not combined["avg_price"].isna().all():
    district_price = combined.groupby(["year", "district"])["avg_price"].mean().unstack()
    for col in district_price.columns:
        axes[1, 0].plot(district_price.index, district_price[col] / 1_000_000,
                        marker="o", linewidth=1.5, markersize=4, label=col)
    axes[1, 0].set_title("מחיר דיור ממוצע לפי מחוז (מ' ₪)")
    axes[1, 0].legend(fontsize=8)

# גרף 4: scatter ריבית vs עסקאות
if "total_transactions" in combined.columns:
    ax = axes[1, 1]
    ax.scatter(combined["interest_rate"], combined["total_transactions"] / 1000,
               c=combined["year"], cmap="viridis", s=80, alpha=0.8)
    ax.set_xlabel("ריבית (%)")
    ax.set_ylabel("עסקאות (אלפים)")
    ax.set_title("ריבית vs נפח עסקאות")

plt.tight_layout()
plt.savefig("full_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# =============================================================
# STEP 7: EXPORT
# =============================================================
print("\nשלב 7: ייצוא...")

with pd.ExcelWriter("analysis_results.xlsx", engine="openpyxl") as writer:
    macro.to_excel(writer, sheet_name="Macro Data", index=False)
    era_summary.to_excel(writer, sheet_name="Era Analysis")
    corr_matrix.to_excel(writer, sheet_name="Correlations")

print("✓ הניתוח הסתיים! כל הקבצים נשמרו.")
```

---

## משימות השבוע – פרויקט מסכם Python/Pandas

### פרויקט: "ניתוח מאקרו-כלכלי ישראל 2015-2024"

**מה להגיש:**

```
Members/YourName/Week_10/
├── data_pipeline.py           ← Pipeline מלא (7 שלבים)
├── economic_analysis.ipynb    ← Notebook עם הסברים
├── macro_analysis_report.md   ← דוח ממצאים
├── full_analysis.png          ← גרף לפרסום
└── analysis_results.xlsx      ← נתונים מעובדים
```

**דרישות:**

1. **נתונים:** ייבא מ-2 מקורות לפחות (נתוני מאקרו + שוק הדיור/תעסוקה)
2. **ניקוי:** תעד כל שלב ניקוי עם `print` + אסרטים
3. **פיצ'רים:** ריבית ריאלית, ממוצע נע 3 שנים, סיווג עידן
4. **ניתוח:** `groupby`, `corr()`, ניתוח Pre/Post העלאת ריבית
5. **גרפים:** לפחות 4 גרפים שמוכנים לפרסום (עיצוב מקצועי, כותרות, מקור)
6. **דוח:** 5 תובנות כלכליות מבוססות-נתונים

---

**המודול הבא:** APIs – גישה אוטומטית לנתוני בנק ישראל, הלמ"ס, OECD → [שבוע 11](../Week_11_APIs_Israel/README.md)
