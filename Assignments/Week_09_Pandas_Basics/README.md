# שבוע 9 – Pandas בסיסי: Excel של Python
### 🎥 סרטון הדרכה מרכזי
צפו בסרטון הבא שמכסה את ליבת החומר הטכני של שבוע זה:
{{< video https://www.youtube.com/watch?v=ZyhVh-qRZPA >}}


> **רמה:** בינוני-מתחיל – מניח שסיימת שבוע 8 (Python Basics)
> **מטרת השבוע:** לטעון, לנקות ולנתח נתונים כלכליים אמיתיים עם pandas

---

## מה זה pandas ולמה?

`pandas` היא ספריית Python לעבודה עם נתונים טבלאיים. בדיוק כמו Excel, אבל:
- עובדת על מיליוני שורות בלי לקרוס
- אפשר לאוטמט פעולות חוזרות
- משתלבת עם גרפים, מודלים, ו-APIs

**הקונצפט המרכזי:** `DataFrame` = טבלה עם שמות לעמודות ולשורות.

---

## חלק א – ייבוא ו-DataFrame ראשון

### התקנה (אם עוד לא)
```bash
pip install pandas numpy openpyxl
```

### Notebook ראשון

```python
import pandas as pd
import numpy as np

# יצירת DataFrame מ-dictionary
data = {
    "year":          [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "gdp_growth":    [4.2,  3.8,  -1.9, 8.6,  6.5,  2.0,  1.1],
    "inflation":     [0.8,  0.8,  -0.6, 1.5,  5.1,  4.2,  3.5],
    "unemployment":  [4.0,  3.8,  4.3,  5.0,  3.7,  3.5,  4.2],
    "interest_rate": [0.1,  0.25, 0.1,  0.1,  3.25, 4.75, 4.5],
}

df = pd.DataFrame(data)

# בדיקה ראשונה
print(df)
print("---")
print(df.shape)     # (7, 5) = 7 שורות, 5 עמודות
print(df.dtypes)    # טיפוס כל עמודה
print(df.describe()) # סטטיסטיקה בסיסית לכל עמודה
```

---

## חלק ב – קריאת נתונים מקבצים

### מ-CSV

```python
# קרא מקובץ CSV
df = pd.read_csv("macro_data.csv", encoding="utf-8")

# עם אפשרויות:
df = pd.read_csv(
    "macro_data.csv",
    sep=",",              # מפריד (ברירת מחדל: פסיק)
    encoding="utf-8-sig", # לקבצים ישראליים עם BOM
    skiprows=1,           # דלג על שורה ראשונה (אם יש כותרת מוזרה)
    na_values=["N/A", "-", ""],  # ערכים לטפל כ-NaN
)
```

### מ-Excel

```python
df = pd.read_excel(
    "macro_data.xlsx",
    sheet_name="annual_data",  # שם גיליון (ברירת מחדל: הראשון)
    usecols="A:E",             # עמודות ספציפיות
)
```

### ראייה ראשונה בנתונים

```python
print(df.head())       # 5 שורות ראשונות
print(df.tail(3))      # 3 שורות אחרונות
print(df.shape)        # (שורות, עמודות)
print(df.columns)      # שמות עמודות
print(df.dtypes)       # טיפוסי נתונים
print(df.info())       # סיכום מלא
print(df.describe())   # סטטיסטיקה בסיסית
print(df.isnull().sum()) # כמה NaN בכל עמודה
```

---

## חלק ג – בחירת נתונים

### בחירת עמודות

```python
# עמודה אחת → Series
gdp_series = df["gdp_growth"]
print(type(gdp_series))  # pandas.Series

# כמה עמודות → DataFrame
subset = df[["year", "gdp_growth", "inflation"]]

# כל העמודות מלבד...
df.drop(columns=["unemployment"])
```

### בחירת שורות: .loc[] ו-.iloc[]

```python
# .loc[] – לפי label (שם/אינדקס)
df.loc[0]           # שורה 0
df.loc[2:5]         # שורות 2 עד 5 (כולל!)
df.loc[0, "gdp_growth"]  # שורה 0, עמודה gdp_growth

# .iloc[] – לפי מיקום מספרי
df.iloc[0]          # שורה ראשונה
df.iloc[-1]         # שורה אחרונה
df.iloc[0:3, 1:3]   # שורות 0-2, עמודות 1-2

# הגדר year כאינדקס
df = df.set_index("year")
df.loc[2022]             # שורת 2022
df.loc[2020:2023]        # שורות 2020-2023
```

---

## חלק ד – סינון (Filtering)

### Boolean Indexing

```python
# שנים עם צמיחה חיובית
positive_growth = df[df["gdp_growth"] > 0]

# שנים עם אינפלציה מעל 3%
high_inflation = df[df["inflation"] > 3]

# שנות מיתון (צמיחה שלילית)
recession_years = df[df["gdp_growth"] < 0]

# מספר תנאים
stagflation = df[(df["gdp_growth"] < 3) & (df["inflation"] > 3)]
extreme = df[(df["gdp_growth"] > 5) | (df["interest_rate"] > 3)]

# NOT
normal = df[~(df["gdp_growth"] < 0)]  # לא מיתון
```

### .query() – תחביר SQL-like

```python
# זהה לסינון למעלה אבל יותר קריא
positive = df.query("gdp_growth > 0")
stagflation = df.query("gdp_growth < 3 and inflation > 3")
recent = df.query("2020 <= year <= 2024")
```

### isin() – ערכים מרשימה

```python
key_years = df[df.index.isin([2020, 2022, 2023])]
```

---

## חלק ה – עמודות מחושבות

```python
# הוסף עמודת ריבית ריאלית
df["real_interest"] = df["interest_rate"] - df["inflation"]

# סיווג מצב כלכלי
def classify_economy(row):
    if row["gdp_growth"] < 0:
        return "מיתון"
    elif row["gdp_growth"] < 2:
        return "צמיחה איטית"
    elif row["gdp_growth"] < 4:
        return "צמיחה נורמלית"
    else:
        return "צמיחה גבוהה"

df["economic_status"] = df.apply(classify_economy, axis=1)

# גרסה קצרה עם numpy.where
df["is_recession"] = np.where(df["gdp_growth"] < 0, True, False)

# np.select לתנאים מרובים
conditions = [
    df["inflation"] < 0,
    df["inflation"] < 2,
    df["inflation"] < 5,
]
choices = ["דפלציה", "יציבות", "אינפלציה מתונה"]
df["inflation_label"] = np.select(conditions, choices, default="אינפלציה גבוהה")

print(df[["gdp_growth", "inflation", "real_interest", "economic_status", "inflation_label"]])
```

---

## חלק ו – פעולות על עמודות

```python
# שינוי % (Year-over-Year)
df["gdp_yoy_change"] = df["gdp_growth"].diff()  # הפרש משנה קודמת

# שינוי % מהשנה הקודמת
df["exports_pct_change"] = df["inflation"].pct_change() * 100

# ממוצע נע
df["gdp_ma3"] = df["gdp_growth"].rolling(window=3).mean()

# cumulative product (צמיחה מצטברת)
df["cumulative_gdp"] = (1 + df["gdp_growth"] / 100).cumprod()

# rank – דירוג
df["inflation_rank"] = df["inflation"].rank(ascending=False)

print(df.head(10))
```

---

## חלק ז – groupby: ניתוח לפי קטגוריות

```python
# הוסף עמודת תקופה
df["era"] = df.index.map(
    lambda y: "עידן ריבית נמוכה" if y <= 2021 else "עידן ריבית גבוהה"
)

# ממוצעים לפי תקופה
era_stats = df.groupby("era")[["gdp_growth", "inflation", "interest_rate"]].mean()
print(era_stats)

# פעולות מרובות
era_detailed = df.groupby("era").agg({
    "gdp_growth":   ["mean", "std", "min", "max"],
    "inflation":    ["mean", "std"],
    "interest_rate": "mean"
})
print(era_detailed)

# count + sum
df.groupby("economic_status")["gdp_growth"].count()

# reset_index – הפוך ל-DataFrame רגיל
df.groupby("era")["gdp_growth"].mean().reset_index()
```

---

## חלק ח – מיון וסינון מתקדם

```python
# מיון
df_sorted = df.sort_values("inflation", ascending=False)
df_top3 = df.nlargest(3, "gdp_growth")   # 3 שנות הצמיחה הגבוהות
df_bot3 = df.nsmallest(3, "inflation")   # 3 שנות האינפלציה הנמוכות

# בחירת עמודות לפי סוג
numeric_cols = df.select_dtypes(include=[np.number])
text_cols = df.select_dtypes(include=["object"])
```

---

## חלק ט – ניקוי נתונים

```python
# בניית DataFrame עם בעיות
dirty_data = pd.DataFrame({
    "year":        [2019, 2019, 2020, None, 2022],
    "gdp_growth":  [3.8,  3.8,  None, 8.6,  6.5],
    "country":     ["  ישראל ", "ישראל", "ישראל", "ישראל", "ישראל"],
    "source":      ["BOI", "BOI", "CBS", "BOI", None],
})

# 1. מציאת שורות כפולות
print(dirty_data.duplicated())
df_clean = dirty_data.drop_duplicates()

# 2. ערכים חסרים (NaN)
print(df_clean.isnull().sum())   # כמה NaN בכל עמודה
df_clean = df_clean.dropna()     # מחק שורות עם NaN
# או:
df_clean["gdp_growth"] = df_clean["gdp_growth"].fillna(df_clean["gdp_growth"].mean())

# 3. ניקוי טקסט
df_clean["country"] = df_clean["country"].str.strip()  # הסר רווחים

# 4. תיקון טיפוסי נתונים
df_clean["year"] = df_clean["year"].astype(int)

# 5. סינון ערכים לא הגיוניים
df_clean = df_clean[df_clean["gdp_growth"].between(-50, 50)]
```

---

## חלק י – ייצוא נתונים

```python
# שמור ל-CSV
df.to_csv("processed_macro.csv", index=True, encoding="utf-8-sig")

# שמור ל-Excel עם כמה גיליונות
with pd.ExcelWriter("macro_analysis.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Raw Data")
    era_stats.to_excel(writer, sheet_name="Era Analysis")

print("קבצים נשמרו!")
```

---

## חלק יא – ויזואליזציה ראשונה עם pandas

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("נתוני מאקרו ישראל 2018-2024", fontsize=14)

# גרף 1: צמיחת תמ"ג
colors = ["green" if x > 0 else "red" for x in df["gdp_growth"]]
axes[0, 0].bar(df.index, df["gdp_growth"], color=colors)
axes[0, 0].set_title("צמיחת תמ\"ג (%)")
axes[0, 0].axhline(0, color="black", linewidth=0.8)

# גרף 2: אינפלציה
axes[0, 1].plot(df.index, df["inflation"], "o-", color="orange", linewidth=2)
axes[0, 1].axhline(2, color="red", linestyle="--", alpha=0.5, label="יעד 2%")
axes[0, 1].set_title("אינפלציה (%)")
axes[0, 1].legend()

# גרף 3: ריבית
axes[1, 0].step(df.index, df["interest_rate"], color="royalblue", linewidth=2)
axes[1, 0].set_title("ריבית בנק ישראל (%)")

# גרף 4: ריבית ריאלית
df["real_interest"] = df["interest_rate"] - df["inflation"]
real_colors = ["green" if x >= 0 else "red" for x in df["real_interest"]]
axes[1, 1].bar(df.index, df["real_interest"], color=real_colors)
axes[1, 1].axhline(0, color="black", linewidth=0.8)
axes[1, 1].set_title("ריבית ריאלית (%)")

plt.tight_layout()
plt.savefig("macro_overview.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## משימות השבוע

### משימה 1: ניקוי נתונים (25 נקודות)

הורד נתוני תעסוקה מהלמ"ס (csv קטן) או השתמש בנתונים שנוצרו בכיתה.
בצע:
- גלה ודווח על NaN, כפולות, ערכים חריגים
- נקה: `strip()`, `fillna()`, `drop_duplicates()`
- אמת: `df.info()` לפני ואחרי

### משימה 2: ניתוח groupby מלא (35 נקודות)

```python
# נתונים: הורד מבנק ישראל או השתמש בנתוני סמסטר מ-Excel
# → טבלה: year, quarter, district, wage_avg, unemployment

# שאלות:
# 1. ממוצע שכר לפי מחוז (groupby district → mean)
# 2. שינוי שכר שנתי לפי מחוז (groupby + pct_change)
# 3. מחוז עם הירידה הגדולה ביותר באבטלה
# 4. השוואה: pre/post 2022 לפי מחוז (groupby + era column)
```

### משימה 3: Dashboard נתוני מאקרו (40 נקודות)

כתוב Notebook (`.ipynb`) שעושה:
1. טעינת נתוני מאקרו 2015-2024 מ-CSV
2. ניקוי + הוספת עמודות מחושבות
3. 4 גרפים (כמו בחלק יא)
4. טבלת `groupby` "עידן ריבית נמוכה vs גבוהה"
5. ייצוא ל-Excel עם 2 גיליונות

---

## הגשה

```
Members/YourName/Week_09/
├── pandas_basics.ipynb     ← Notebook ראשי
├── economic_analysis.py    ← סקריפט עצמאי
├── macro_overview.png      ← גרף הדשבורד
└── processed_data.xlsx     ← נתונים מעובדים
```

---

**השבוע הבא:** Pandas מתקדם – Time Series, merge, pivot_table, ניתוח מלא → [שבוע 10](../Week_10_Pandas_Advanced/README.md)
