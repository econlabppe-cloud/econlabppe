# משימה 3 – SQL: שאילתות על נתונים כלכליים

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=m0wI61ahfvY >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=igSovq_H24A >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=sUxrA8NIVK0 >}}

:::
## חלק א – הכנה: צור בסיס נתונים מקומי

פתח DBeaver וצור **בסיס נתונים SQLite חדש**:
`File → New Database Connection → SQLite → צור קובץ israel_macro.db`

### צור את הטבלאות הבאות ב-DBeaver:

```sql
-- טבלת נתוני מאקרו שנתיים
CREATE TABLE macro_annual (
    year        INTEGER PRIMARY KEY,
    gdp_growth  REAL,    -- צמיחת תמ"ג %
    inflation   REAL,    -- אינפלציה %
    unemployment REAL,   -- אבטלה %
    interest_rate REAL   -- ריבית בנק ישראל %
);

-- טבלת אוכלוסייה לפי מחוז
CREATE TABLE population_district (
    year        INTEGER,
    district    TEXT,
    population  INTEGER,
    PRIMARY KEY (year, district)
);
```

### הכנס נתונים לדוגמה:

```sql
INSERT INTO macro_annual VALUES
(2019, 3.8, 0.8, 3.8, 0.25),
(2020, -1.9, -0.6, 4.3, 0.1),
(2021, 8.6, 1.5, 5.0, 0.1),
(2022, 6.5, 5.1, 3.7, 3.25),
(2023, 2.0, 4.2, 3.5, 4.75),
(2024, 1.1, 3.5, 4.2, 4.5);
```

---

## חלק ב – שאילתות בסיסיות

**תרגיל 1:** הצג את כל השנים עם צמיחה חיובית, ממוינות מהגבוהה לנמוכה.
```sql
SELECT year, gdp_growth
FROM macro_annual
WHERE gdp_growth > 0
ORDER BY gdp_growth DESC;
```

**תרגיל 2:** מה ממוצע האינפלציה בשנים 2020–2024?
```sql
-- כתוב את השאילתה שלך:


```

**תרגיל 3:** כמה שנים הייתה ריבית מעל 1%?
```sql
-- כתוב את השאילתה שלך:


```

---

## חלק ג – GROUP BY ואגרגציה

**תרגיל 4:** חלק את השנים ל-2 קבוצות: "לפני קורונה" (≤2019) ו-"אחרי קורונה" (>2019).
הצג את ממוצע האינפלציה לכל קבוצה.

```sql
SELECT
    CASE WHEN year <= 2019 THEN 'Pre-COVID' ELSE 'Post-COVID' END AS period,
    AVG(inflation) AS avg_inflation,
    AVG(gdp_growth) AS avg_growth,
    COUNT(*) AS num_years
FROM macro_annual
GROUP BY period;
```

---

## חלק ד – JOIN בין טבלאות

הוסף טבלת נתוני ייצוא שנתיים:
```sql
CREATE TABLE exports (
    year    INTEGER PRIMARY KEY,
    exports_bn_usd REAL  -- ייצוא במיליארד דולר
);

INSERT INTO exports VALUES
(2019, 68.6), (2020, 58.9), (2021, 73.5),
(2022, 82.1), (2023, 75.4), (2024, 71.2);
```

**תרגיל 5:** צור שאילתה שמחברת בין `macro_annual` ל-`exports` ומחשבת יחס ייצוא/תמ"ג (הנח תמ"ג ≈ 500 מיליארד ₪).
```sql
-- כתוב את השאילתה שלך:

```

---

## חלק ה – Python + SQL (בונוס)

```python
import sqlite3
import pandas as pd

# התחבר לבסיס הנתונים
conn = sqlite3.connect("israel_macro.db")

# הרץ שאילתה וטען לתוך DataFrame
df = pd.read_sql_query("""
    SELECT year, gdp_growth, inflation, interest_rate
    FROM macro_annual
    WHERE year >= 2020
    ORDER BY year
""", conn)

print(df)
conn.close()
```

שמור כ-`Members/YourName/Week_03/sql_analysis.py`

---

## הגשה

תיקיית ההגשה: `Members/YourName/Week_03/`

**מה להגיש:**
- [ ] `queries.sql` – כל השאילתות שכתבת (תרגילים 2, 3, 5)
- [ ] `sql_analysis.py` – קוד Python שמריץ שאילתה ומציג DataFrame
- [ ] `summary.md` – 3 תובנות שגילית על הנתונים

---

**השבוע הבא:** Python + Pandas → [משימה 4](../Week_04_Python_Pandas/README.md)
