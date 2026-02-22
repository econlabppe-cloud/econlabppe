# שבוע 7 – SQL מתקדם: Window Functions, CTEs, ו-Python+SQL


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=Ww71knvhQ-s](https://www.youtube.com/watch?v=Ww71knvhQ-s) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=cNgMWD2mMWU](https://www.youtube.com/watch?v=cNgMWD2mMWU) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=zAmJTGEGzAM](https://www.youtube.com/watch?v=zAmJTGEGzAM) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=cNgMWD2mMWU >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=Ww71knvhQ-s >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=zAmJTGEGzAM >}}

:::
## מה נלמד השבוע?

| נושא | זמן משוער |
|---|---|
| CTEs – WITH clause | 60 דקות |
| Window Functions: ROW_NUMBER, RANK, DENSE_RANK | 75 דקות |
| Window Functions: LAG, LEAD – שינויים לאורך זמן | 75 דקות |
| Window Functions: Running Totals, Moving Averages | 60 דקות |
| String + Date Functions | 45 דקות |
| Python + SQLite: pandas + sqlite3 | 90 דקות |
| פרויקט מסכם: ניתוח מאקרו-כלכלי מלא | 90 דקות |
| **סה"כ** | **~8.5 שעות** |

---

## חלק א – CTEs: Common Table Expressions

### מה זה CTE?

CTE הוא "שאילתה זמנית" שנותנים לה שם. מאפשר לשבור שאילתה מורכבת לחלקים קריאים.

**בלי CTE (קשה לקרוא):**
```sql
SELECT year, district, avg_price,
       (avg_price - (SELECT AVG(avg_price) FROM housing_market)) / (SELECT AVG(avg_price) FROM housing_market) * 100 AS pct_above_avg
FROM housing_market
WHERE avg_price > (SELECT AVG(avg_price) FROM housing_market);
```

**עם CTE (קריא):**
```sql
WITH market_avg AS (
    SELECT AVG(avg_price) AS overall_avg
    FROM housing_market
)
SELECT
    h.year,
    h.district,
    h.avg_price,
    ROUND((h.avg_price - ma.overall_avg) / ma.overall_avg * 100, 1) AS pct_above_avg
FROM housing_market AS h
CROSS JOIN market_avg AS ma
WHERE h.avg_price > ma.overall_avg
ORDER BY pct_above_avg DESC;
```

### מבנה CTE

```sql
WITH
    cte_name_1 AS (
        SELECT ... FROM ... WHERE ...
    ),
    cte_name_2 AS (
        SELECT ... FROM cte_name_1 ...
    )
SELECT ...
FROM cte_name_1
JOIN cte_name_2 ON ...;
```

### CTE מרובות – ניתוח מדיניות ריבית

```sql
WITH
    -- שלב 1: ממוצעים לפי תקופה
    period_averages AS (
        SELECT
            CASE
                WHEN year <= 2021 THEN 'low_rate_era'
                ELSE                   'high_rate_era'
            END AS era,
            ROUND(AVG(gdp_growth), 2)    AS avg_growth,
            ROUND(AVG(inflation), 2)     AS avg_inflation,
            ROUND(AVG(unemployment), 2)  AS avg_unemployment,
            ROUND(AVG(interest_rate), 2) AS avg_rate
        FROM macro_annual
        GROUP BY era
    ),

    -- שלב 2: ממוצעי דיור לפי תקופה
    housing_by_era AS (
        SELECT
            CASE
                WHEN year <= 2021 THEN 'low_rate_era'
                ELSE                   'high_rate_era'
            END AS era,
            ROUND(AVG(avg_price), 0)    AS avg_housing_price,
            SUM(transactions)           AS total_transactions
        FROM housing_market
        GROUP BY era
    )

-- שלב 3: מיזוג
SELECT
    pa.era,
    pa.avg_growth,
    pa.avg_inflation,
    pa.avg_rate,
    hb.avg_housing_price,
    hb.total_transactions
FROM period_averages AS pa
JOIN housing_by_era AS hb ON pa.era = hb.era;
```

---

## חלק ב – Window Functions: הכלי הכי עוצמתי ב-SQL

### מה זה Window Function?

Window Function מחשב ערך לכל שורה **תוך הסתכלות על שורות אחרות**. בניגוד ל-GROUP BY שמקטינה שורות, Window Function **שומרת את כל השורות**.

```sql
-- הסינטקס:
function_name() OVER (
    PARTITION BY column   -- חלוקה לקבוצות (אופציונלי)
    ORDER BY column       -- סדר בתוך הקבוצה
    ROWS/RANGE BETWEEN ...  -- חלון (אופציונלי)
)
```

### ROW_NUMBER, RANK, DENSE_RANK

```sql
SELECT
    year,
    district,
    avg_price,

    -- מספור ברציפות (1,2,3,4...)
    ROW_NUMBER() OVER (PARTITION BY year ORDER BY avg_price DESC) AS row_num,

    -- דירוג (1,2,2,4 – עם קפיצה)
    RANK() OVER (PARTITION BY year ORDER BY avg_price DESC) AS price_rank,

    -- דירוג צפוף (1,2,2,3 – ללא קפיצה)
    DENSE_RANK() OVER (PARTITION BY year ORDER BY avg_price DESC) AS price_dense_rank

FROM housing_market
ORDER BY year, avg_price DESC;
```

**שאלה כלכלית:** מהו הדירוג של כל מחוז לפי מחיר דיור לכל שנה?

### הצג רק את מקום 1 מכל קבוצה (TOP N per group)

```sql
-- הרבעון הכי יקר לכל מחוז
WITH ranked AS (
    SELECT
        year,
        quarter,
        district,
        avg_price,
        ROW_NUMBER() OVER (
            PARTITION BY district
            ORDER BY avg_price DESC
        ) AS rn
    FROM housing_market
)
SELECT year, quarter, district, avg_price
FROM ranked
WHERE rn = 1
ORDER BY avg_price DESC;
```

---

## חלק ג – LAG ו-LEAD: שינויים לאורך זמן

### LAG – ערך מהשורה הקודמת

`LAG(column, n)` = הערך מ-n שורות לפנינו.

```sql
-- שינוי ייצוא שנה לשנה
SELECT
    year,
    exports_bn_usd,
    LAG(exports_bn_usd, 1) OVER (ORDER BY year) AS prev_year_exports,
    ROUND(
        exports_bn_usd - LAG(exports_bn_usd, 1) OVER (ORDER BY year),
    1) AS exports_change,
    ROUND(
        (exports_bn_usd - LAG(exports_bn_usd, 1) OVER (ORDER BY year)) /
        LAG(exports_bn_usd, 1) OVER (ORDER BY year) * 100,
    1) AS exports_pct_change
FROM exports
ORDER BY year;
```

### LEAD – ערך מהשורה הבאה

```sql
-- לכל שנה, כמה אינפלציה צפויה בשנה הבאה? (עם LAG לצפייה לאחור)
SELECT
    year,
    inflation,
    LAG(inflation, 1)  OVER (ORDER BY year) AS prev_inflation,
    LEAD(inflation, 1) OVER (ORDER BY year) AS next_inflation
FROM macro_annual
ORDER BY year;
```

### LAG עם PARTITION BY

```sql
-- שינוי מחיר דיור לפי מחוז (לא לערבב בין מחוזות!)
SELECT
    year,
    quarter,
    district,
    avg_price,
    LAG(avg_price, 1) OVER (
        PARTITION BY district  -- ← חשוב! LAG בתוך כל מחוז בנפרד
        ORDER BY year, quarter
    ) AS prev_period_price,
    ROUND(
        (avg_price - LAG(avg_price, 1) OVER (
            PARTITION BY district ORDER BY year, quarter
        )) / LAG(avg_price, 1) OVER (
            PARTITION BY district ORDER BY year, quarter
        ) * 100,
    1) AS price_change_pct
FROM housing_market
ORDER BY district, year, quarter;
```

---

## חלק ד – Running Totals ו-Moving Averages

### Running Total (סכום מצטבר)

```sql
-- ייצוא מצטבר לאורך השנים
SELECT
    year,
    exports_bn_usd,
    ROUND(
        SUM(exports_bn_usd) OVER (ORDER BY year),
    1) AS cumulative_exports
FROM exports
ORDER BY year;
```

### Moving Average (ממוצע נע)

```sql
-- ממוצע צמיחה נע (3 שנים)
SELECT
    year,
    gdp_growth,
    ROUND(
        AVG(gdp_growth) OVER (
            ORDER BY year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW  -- 3 שנים: 2 קודמות + נוכחית
        ),
    2) AS moving_avg_3yr
FROM macro_annual
ORDER BY year;
```

**ROWS BETWEEN:**
```
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW  ← 3 שנים אחורה
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING  ← שנה קודמת + נוכחית + שנה הבאה
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ← מהתחלה עד עכשיו
```

### Percentile מצטבר

```sql
-- לכל שנה – מה האחוזון של הצמיחה?
SELECT
    year,
    gdp_growth,
    ROUND(
        PERCENT_RANK() OVER (ORDER BY gdp_growth) * 100,
    1) AS percentile
FROM macro_annual
ORDER BY year;
```

---

## חלק ה – String & Date Functions

### String Functions

```sql
-- עיבוד טקסט
SELECT
    district,
    LENGTH(district)         AS name_length,
    UPPER(district)          AS upper_name,
    LOWER(district)          AS lower_name,
    TRIM('  תל אביב  ')      AS trimmed,
    SUBSTR(district, 1, 2)   AS first_two_chars,
    REPLACE(district, 'תל ', 'ת"א ') AS replaced
FROM housing_market
GROUP BY district;

-- שרשור מחרוזות
SELECT
    year || '-Q' || quarter AS period_label,
    district,
    avg_price
FROM housing_market
ORDER BY year, quarter;
```

### Date Functions (SQLite)

```sql
-- עבודה עם תאריכים (SQLite)
SELECT
    date('now')              AS today,
    strftime('%Y', date('now')) AS current_year,
    date('now', '-1 year')   AS one_year_ago;

-- אם יש עמודת תאריך אמיתית
SELECT
    date_col,
    strftime('%Y', date_col) AS year,
    strftime('%m', date_col) AS month,
    strftime('%Q', date_col) AS quarter
FROM some_table;
```

---

## חלק ו – Python + SQL: שילוב עוצמתי

### למה לשלב?

- **SQL** מצוין ל: שאילתות, סינון, JOIN, אגרגציה
- **Python/Pandas** מצוין ל: גרפים, מודלים סטטיסטיים, API, ייצוא

**הגישה הטובה ביותר:** SQL לשאוב נתונים → Pandas לניתוח/גרפים.

### חיבור Python ל-SQLite

```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Arial'  # לתמיכה בעברית

# התחבר לבסיס הנתונים
conn = sqlite3.connect("israel_economy.db")

# --- שאילתה 1: נתוני מאקרו בסיסיים ---
df_macro = pd.read_sql_query("""
    SELECT year, gdp_growth, inflation, interest_rate
    FROM macro_annual
    ORDER BY year
""", conn)

print(df_macro.head())
print(df_macro.describe())  # סטטיסטיקה בסיסית
```

### שאילתות מורכבות דרך Python

```python
# --- שאילתה 2: ניתוח עם Window Functions ---
df_trends = pd.read_sql_query("""
    WITH base AS (
        SELECT
            year,
            gdp_growth,
            inflation,
            interest_rate,
            LAG(gdp_growth, 1) OVER (ORDER BY year) AS prev_growth,
            AVG(gdp_growth) OVER (
                ORDER BY year
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS moving_avg_3yr
        FROM macro_annual
    )
    SELECT *,
        ROUND(gdp_growth - prev_growth, 2) AS growth_change
    FROM base
    WHERE year >= 2016
    ORDER BY year
""", conn)

print(df_trends)
```

### גרפים: SQL → Pandas → Matplotlib

```python
# --- גרף 1: מגמות מאקרו-כלכליות ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("מדדי מאקרו-כלכלה ישראל 2015-2024", fontsize=16, fontweight='bold')

# תמ"ג
axes[0, 0].bar(df_macro['year'], df_macro['gdp_growth'],
               color=['green' if x > 0 else 'red' for x in df_macro['gdp_growth']])
axes[0, 0].set_title("צמיחת תמ\"ג (%)")
axes[0, 0].axhline(y=0, color='black', linewidth=0.5)

# אינפלציה
axes[0, 1].plot(df_macro['year'], df_macro['inflation'], 'o-', color='orange', linewidth=2)
axes[0, 1].set_title("אינפלציה (%)")
axes[0, 1].axhline(y=2, color='red', linewidth=0.5, linestyle='--', label='יעד 2%')
axes[0, 1].legend()

# ריבית
axes[1, 0].step(df_macro['year'], df_macro['interest_rate'], color='royalblue', linewidth=2)
axes[1, 0].set_title("ריבית בנק ישראל (%)")

# ריבית ריאלית
df_macro['real_rate'] = df_macro['interest_rate'] - df_macro['inflation']
colors = ['green' if x >= 0 else 'red' for x in df_macro['real_rate']]
axes[1, 1].bar(df_macro['year'], df_macro['real_rate'], color=colors)
axes[1, 1].axhline(y=0, color='black', linewidth=1)
axes[1, 1].set_title("ריבית ריאלית (%)")

plt.tight_layout()
plt.savefig("macro_dashboard.png", dpi=150, bbox_inches='tight')
plt.show()

print("גרף נשמר!")
```

### ניתוח שוק הדיור מ-SQL

```python
# --- ניתוח שוק הדיור ---
df_housing = pd.read_sql_query("""
    SELECT
        h.year,
        h.quarter,
        h.district,
        h.avg_price,
        h.transactions,
        m.interest_rate
    FROM housing_market AS h
    JOIN macro_annual AS m ON h.year = m.year
    ORDER BY h.year, h.quarter, h.district
""", conn)

# Pivot: מחיר ממוצע לפי מחוז לאורך זמן
df_housing['period'] = df_housing['year'].astype(str) + '-Q' + df_housing['quarter'].astype(str)
pivot = df_housing.pivot_table(
    values='avg_price',
    index='period',
    columns='district',
    aggfunc='mean'
)

print("פיבוט מחירי דיור:")
print(pivot.to_string())

# גרף השוואת מחוזות
fig, ax = plt.subplots(figsize=(14, 6))
for district in pivot.columns:
    ax.plot(pivot.index, pivot[district] / 1_000_000,
            marker='o', linewidth=2, markersize=4, label=district)

ax.set_title("מחירי דיור לפי מחוז 2022-2023 (מיליון ₪)", fontsize=14)
ax.set_xlabel("רבעון")
ax.set_ylabel("מחיר ממוצע (מיליון ₪)")
ax.legend(loc='upper right')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig("housing_by_district.png", dpi=150)
plt.show()

conn.close()
print("ניתוח הסתיים!")
```

---

## חלק ז – ניתוח מלא: תגובת שוק הדיור להעלאות הריבית

### הגישה: מחקר כלכלי מלא ב-SQL + Python

```python
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

conn = sqlite3.connect("israel_economy.db")

# שלב 1: CTE מורכב לנתונים מוכנים לניתוח
df_analysis = pd.read_sql_query("""
    WITH
        macro_with_lags AS (
            SELECT
                year,
                interest_rate,
                inflation,
                gdp_growth,
                LAG(interest_rate, 1) OVER (ORDER BY year) AS prev_rate,
                interest_rate - LAG(interest_rate, 1) OVER (ORDER BY year) AS rate_change
            FROM macro_annual
        ),
        housing_annual AS (
            SELECT
                year,
                AVG(avg_price)    AS avg_price,
                SUM(transactions) AS total_transactions,
                COUNT(DISTINCT district) AS num_districts
            FROM housing_market
            GROUP BY year
        )
    SELECT
        ml.year,
        ml.interest_rate,
        ml.rate_change,
        ml.inflation,
        ml.gdp_growth,
        ha.avg_price,
        ha.total_transactions
    FROM macro_with_lags AS ml
    JOIN housing_annual AS ha ON ml.year = ha.year
    WHERE ml.rate_change IS NOT NULL
    ORDER BY ml.year
""", conn)

# שלב 2: ניתוח סטטיסטי
print("=== קורלציות ===")
correlations = df_analysis[['interest_rate', 'avg_price', 'total_transactions', 'gdp_growth']].corr()
print(correlations.to_string())

# שלב 3: רגרסיה פשוטה (ריבית → מחיר דיור)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df_analysis['interest_rate'],
    df_analysis['avg_price']
)

print(f"\n=== רגרסיה: ריבית → מחיר דיור ===")
print(f"מקדם (slope): {slope:,.0f} ₪ לכל 1% ריבית")
print(f"R²: {r_value**2:.3f}")
print(f"p-value: {p_value:.4f}")

# שלב 4: גרף עם קו רגרסיה
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# scatter: ריבית vs מחיר דיור
axes[0].scatter(df_analysis['interest_rate'], df_analysis['avg_price'] / 1_000_000,
                s=100, color='royalblue', zorder=5)
for _, row in df_analysis.iterrows():
    axes[0].annotate(str(int(row['year'])),
                     (row['interest_rate'], row['avg_price']/1_000_000),
                     textcoords="offset points", xytext=(5, 5), fontsize=8)

# קו רגרסיה
x_line = np.linspace(df_analysis['interest_rate'].min(),
                     df_analysis['interest_rate'].max(), 100)
y_line = (slope * x_line + intercept) / 1_000_000
axes[0].plot(x_line, y_line, 'r--', alpha=0.7)
axes[0].set_xlabel("ריבית בנק ישראל (%)")
axes[0].set_ylabel("מחיר ממוצע (מיליון ₪)")
axes[0].set_title(f"ריבית vs מחיר דיור\nR²={r_value**2:.3f}, p={p_value:.3f}")

# עסקאות לאורך זמן
axes[1].bar(df_analysis['year'], df_analysis['total_transactions'],
            color='steelblue', alpha=0.7)
ax2 = axes[1].twinx()
ax2.plot(df_analysis['year'], df_analysis['interest_rate'],
         'ro-', linewidth=2, markersize=6, label='ריבית')
axes[1].set_xlabel("שנה")
axes[1].set_ylabel("מספר עסקאות")
ax2.set_ylabel("ריבית (%)")
axes[1].set_title("עסקאות דיור vs ריבית")
ax2.legend()

plt.tight_layout()
plt.savefig("rate_housing_analysis.png", dpi=150)
plt.show()

conn.close()
```

---

## משימות השבוע – פרויקט מסכם SQL

### פרויקט: "ניתוח שוק הדיור הישראלי 2022-2023"

**הנחיות:**

**חלק א: שאילתות SQL (40 נקודות)**

1. **CTE מורכבת:** צור CTE בת 3 שלבים:
   - שלב 1: ממוצע מחיר דיור לכל מחוז לכל שנה
   - שלב 2: דירוג מחוזות לפי מחיר (RANK)
   - שלב 3: סינון ל-3 המחוזות היקרים ביותר

2. **Window Functions:** לכל רבעון ומחוז, חשב:
   - מחיר נוכחי
   - מחיר רבעון קודם (LAG)
   - שינוי % מרבעון קודם
   - ממוצע נע של 4 רבעונים

3. **ניתוח ריבית-דיור:** צור טבלה שמשלבת:
   - ריבית בנק ישראל
   - ממוצע מחיר דיור
   - מספר עסקאות
   - שינוי % בכל המדדים שנה לשנה

**חלק ב: Python + SQL (60 נקודות)**

כתוב סקריפט Python שעושה:

1. שולף נתונים מ-SQLite עם שאילתה מורכבת (כולל CTE)
2. יוצר 4 גרפים:
   - גרף קו: מחיר דיור ממוצע לפי מחוז לאורך זמן
   - גרף scatter: ריבית vs עסקאות (עם שנה כ-label)
   - גרף עמודות: שינוי % ברבעון לפי מחוז
   - Heat map: מחיר דיור (שנה × מחוז)
3. מחשב:
   - קורלציה פירסון בין ריבית לעסקאות
   - בדיקה: האם ירידת מחירים אחרי 2022-Q3 מובהקת?
4. שומר גרפים כ-PNG ומסכם ממצאים ב-Markdown

---

## הגשה

```
Members/YourName/Week_07/
├── week07_advanced_queries.sql    ← כל שאילתות SQL
├── housing_analysis.py            ← סקריפט Python מלא
├── macro_dashboard.png            ← גרף 1
├── housing_by_district.png        ← גרף 2
├── rate_housing_analysis.png      ← גרף 3
└── housing_research_report.md     ← דוח מחקר
```

**בדוח המחקר:**
```markdown
# ניתוח שוק הדיור הישראלי: השפעת מדיניות הריבית 2022-2023

## 1. תקציר מנהלים
[4-5 משפטים]

## 2. שאלות מחקר
1. האם העלאות הריבית 2022 הובילו לירידת מחירי דיור?
2. כיצד הגיבו העסקאות לשינויי הריבית?
3. האם ההשפעה אחידה בין מחוזות?

## 3. נתונים ומתודולוגיה
- מקורות: בנק ישראל, הלמ"ס
- כלים: SQLite, Python (pandas, scipy, matplotlib)
- תקופה: 2022 Q1 – 2023 Q4

## 4. ממצאים

### 4.1 מחירי דיור
[ניתוח + גרף]

### 4.2 נפח עסקאות
[ניתוח + גרף]

### 4.3 פערים מחוזיים
[ניתוח]

## 5. מגבלות
...

## 6. מסקנות ומדיניות מוצעת
...
```

---

## טיפים מקצועיים

1. **הוסף הערות לכל שאילתה:** `-- מחשב ממוצע נע של 3 שנים`
2. **Format קוד SQL:** כל עמודה בשורה נפרדת, UPPERCASE לפקודות
3. **בדוק ביניים:** הרץ כל CTE בנפרד לפני המיזוג הסופי
4. **נקה ל-NULL:** תמיד בדוק `WHERE column IS NOT NULL` לפני Window Functions
5. **אל תאמין לתוצאות בלי בדיקה:** השווה ל-Excel אם יש ספק

---

## מה הלאה?

סיימת את מודול ה-SQL! בשלב הבא נעבור ל-**Python ו-Pandas** – שם נממש את הניתוחים של SQL אבל עם ספריית pandas מלאה, גרפים מתקדמים, ו-APIs של נתונים כלכליים.

---

**המודול הבא:** Python ו-Pandas – ניתוח נתונים מלא → [שבוע 8](../Week_08_Python_Basics/README.md)

### 💻 תרגול מעשי (Hands-on)

<p>לחצו על המשולש (Play) כדי להפעיל את סביבת הפיתוח בתוך העמוד, או פתחו בלשונית חדשה לנוחות מירבית.</p>
<iframe src="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_07_SQL_Advanced/starter_notebook.ipynb" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
<p><br><em>* אם המסך לא נטען או מבקש הרשאות אבטחה, <a href="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_07_SQL_Advanced/starter_notebook.ipynb" target="_blank">לחצו כאן לפתיחת המחברת במסך מלא</a>.</em></p>
---
### 🧠 בחן את עצמך (שאלות סיכום)
פונקציות חלון הן ה"נשק הסודי" של אנליסטים בכירים. בדקו את עצמכם:

<details>
<summary><b>שאלה 1: מה ההבדל המהותי בין GROUP BY לבין פונקציית חלון (OVER)?</b> 👁️ לחץ לתשובה</summary>
<br>
<b>GROUP BY</b> מכווץ את השורות (אם היו 100 עובדים ב-3 מחלקות, נקבל רק 3 שורות עם הממוצע של כל מחלקה).
<br><b>פונקציית חלון</b> מחשבת את הממוצע אבל <b>שומרת על השורות המקוריות</b>, כך שאפשר לראות את השכר של כל עובד <i>לצד</i> הממוצע של המחלקה שלו באותה השורה.
</details>

<details>
<summary><b>שאלה 2: מה ההבדל בין RANK לבין ROW_NUMBER בדירוג נתונים?</b> 👁️ לחץ לתשובה</summary>
<br>
<b>ROW_NUMBER</b> מחלק מספר רציף וייחודי לכל שורה (1, 2, 3, 4), גם אם יש ערכים זהים.
<br><b>RANK</b> ייתן את אותו הדירוג לערכים זהים, וידלג על המספרים הבאים (למשל: שני עובדים עם אותו שכר יקבלו דירוג 1, והעובד הבא אחריהם יקבל דירוג 3).
</details>


---

### 💬 הערות, שאלות ודיונים
יש לכם שאלה על החומר של פרק זה? משהו לא עבד במחברת התרגול? מצאתם דרך יעילה יותר לכתוב את הקוד?
**כתבו לנו כאן למטה!** המערכת מחוברת ישירות לגיטהאב של הקורס. כל שאלה שתשאלו כאן תישמר אוטומטית בצורה מסודרת תחת נושא זה, והצוות (או סטודנטים אחרים) יוכלו לענות לכם ולעזור.
