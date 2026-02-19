# Cookbook: Pandas לכלכלנים

> Pandas הוא ה-Excel של Python – רק עם כוח עיבוד של מדען נתונים.
> המדריך הזה מכסה את 90% ממה שתצטרך בניתוח כלכלי יומיומי.

---

## הכנה

```bash
pip install pandas numpy openpyxl xlrd
```

---

## 1. טעינת נתונים

```python
import pandas as pd
import numpy as np

# ---- CSV ----
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_csv("data_hebrew.csv", encoding="utf-8-sig")  # עברית עם BOM

# ---- Excel ----
df = pd.read_excel("boi_data.xlsx", sheet_name=0, skiprows=3)

# ---- מה יש בתוך ה-DataFrame ----
print(df.shape)           # (שורות, עמודות)
print(df.dtypes)          # סוגי נתונים
print(df.head(5))         # 5 שורות ראשונות
print(df.describe())      # סטטיסטיקה בסיסית
print(df.isnull().sum())  # כמה ערכים חסרים בכל עמודה
```

---

## 2. ניקוי נתונים

```python
# ---- שמות עמודות ----
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ---- הסרת כפילויות ----
df = df.drop_duplicates()

# ---- ערכים חסרים ----
df = df.dropna(subset=["gdp_growth"])           # הסר שורות ללא gdp
df["inflation"] = df["inflation"].fillna(0)    # מלא ב-0
df["value"] = df["value"].interpolate()         # אינטרפולציה לינארית

# ---- המרת טיפוסים ----
df["year"] = df["year"].astype(int)
df["gdp_growth"] = pd.to_numeric(df["gdp_growth"], errors="coerce")

# ---- עמודות מחרוזת לתאריך ----
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
```

---

## 3. סינון ובחירה

```python
# ---- סינון שורות ----
df_positive = df[df["gdp_growth"] > 0]
df_recent   = df[df["year"] >= 2020]
df_combined = df[(df["year"] >= 2015) & (df["inflation"] > 1)]

# ---- בחירת עמודות ----
df_subset = df[["year", "gdp_growth", "inflation"]]

# ---- loc (לפי תווית) ----
df.loc[df["year"] == 2022, "gdp_growth"]

# ---- iloc (לפי מיקום) ----
df.iloc[0:5, 0:3]  # 5 שורות ראשונות, 3 עמודות ראשונות
```

---

## 4. עיבוד וחישוב

```python
# ---- עמודות חדשות ----
df["real_growth"]    = df["gdp_growth"] - df["inflation"]  # צמיחה ריאלית
df["high_inflation"] = df["inflation"] > 3                  # Boolean

# ---- שינוי YoY ----
df["gdp_yoy_change"] = df["gdp_growth"].diff()       # שינוי מוחלט
df["gdp_yoy_pct"]    = df["gdp_growth"].pct_change() # שינוי %

# ---- Cumulative Growth ----
df["cum_growth"] = (1 + df["gdp_growth"] / 100).cumprod()

# ---- Rolling Average (ממוצע נע) ----
df["gdp_3yr_avg"] = df["gdp_growth"].rolling(window=3).mean()
```

---

## 5. GroupBy ואגרגציה

```python
# ---- ממוצע לפי עשור ----
df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

summary = df.groupby("decade").agg(
    avg_growth    = ("gdp_growth",  "mean"),
    avg_inflation = ("inflation",   "mean"),
    num_years     = ("year",        "count"),
    max_growth    = ("gdp_growth",  "max"),
).round(2)
print(summary)

# ---- apply: פונקציה מותאמת ----
def classify_period(row):
    if row["gdp_growth"] > 3 and row["inflation"] < 2:
        return "golden"
    elif row["gdp_growth"] < 0:
        return "recession"
    return "normal"

df["period_type"] = df.apply(classify_period, axis=1)
print(df["period_type"].value_counts())
```

---

## 6. סדרות עתיות

```python
# ---- הגדרת DatetimeIndex ----
df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01")
df = df.set_index("date")

# ---- Resampling ----
# אם יש נתונים חודשיים – ממוצע רבעוני:
df_quarterly = df["inflation"].resample("QE").mean()
# ממוצע שנתי:
df_annual    = df["inflation"].resample("YE").mean()

# ---- Lag ----
df["inflation_lag1"]  = df["inflation"].shift(1)   # חודש קודם
df["inflation_lead1"] = df["inflation"].shift(-1)  # חודש הבא
```

---

## 7. מיזוג נתונים (כמו JOIN ב-SQL)

```python
df_gdp = pd.DataFrame({"year": [2020, 2021, 2022], "gdp": [100, 108, 115]})
df_cpi = pd.DataFrame({"year": [2020, 2021, 2022], "cpi": [99.4, 101.0, 106.2]})

# INNER JOIN
df_merged = pd.merge(df_gdp, df_cpi, on="year", how="inner")

# LEFT JOIN (שמור את כל שורות df_gdp)
df_left = pd.merge(df_gdp, df_cpi, on="year", how="left")

# שרשור (UNION)
df_all = pd.concat([df_2022, df_2023], ignore_index=True)
```

---

## 8. ייצוא

```python
# ---- CSV (לא ל-Git – שמור ב-Google Drive!) ----
df.to_csv("output.csv", index=False, encoding="utf-8-sig")

# ---- Excel ----
df.to_excel("output.xlsx", index=False)

# ---- Parquet (יעיל לקבצים גדולים) ----
df.to_parquet("output.parquet", index=False)
```

---

## 9. פונקציות שימושיות לכלכלנים

```python
# ---- מתאם בין משתנים ----
corr = df[["gdp_growth", "inflation", "unemployment"]].corr()
print(corr)

# ---- Percentiles ----
p25    = df["gdp_growth"].quantile(0.25)
median = df["gdp_growth"].median()

# ---- Z-Score (נרמול) ----
df["gdp_z"] = (df["gdp_growth"] - df["gdp_growth"].mean()) / df["gdp_growth"].std()

# ---- זיהוי חריגים (Outliers) ----
outliers = df[df["gdp_z"].abs() > 2]
print("שנים חריגות:", list(outliers.index))
```

---

*עודכן: 2025*
