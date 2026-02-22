# שבוע 6 – SQL בינוני: GROUP BY, JOINs, ושאילתות מורכבות


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=9yeOJ0ZMUYw](https://www.youtube.com/watch?v=9yeOJ0ZMUYw) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=0UQJC_FEQ_A](https://www.youtube.com/watch?v=0UQJC_FEQ_A) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=CJzeKzKz_KU](https://www.youtube.com/watch?v=CJzeKzKz_KU) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=0OQJC_FEQ_A >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=9yeOJ0ZMUYw >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=CJzeKzKz_KU >}}

:::
## מה נלמד השבוע?

| נושא | זמן משוער |
|---|---|
| GROUP BY + HAVING | 90 דקות |
| JOIN: INNER, LEFT, RIGHT | 120 דקות |
| Subqueries בסיסיות | 60 דקות |
| NULL handling | 30 דקות |
| CREATE TABLE AS SELECT | 30 דקות |
| שאילתות כלכליות מורכבות | 90 דקות |
| **סה"כ** | **~7 שעות** |

---

## הכנה: הרחבת בסיס הנתונים

לפני שמתחילים, הוסף עוד טבלאות לבסיס הנתונים מ-Week 5:

```sql
-- נתוני ייצוא שנתיים
CREATE TABLE exports (
    year              INTEGER PRIMARY KEY,
    exports_bn_usd    REAL,    -- ייצוא במיליארד דולר
    hi_tech_share_pct REAL,    -- חלק הייצוא עתיר טכנולוגיה %
    main_destination  TEXT     -- יעד ייצוא עיקרי
);

INSERT INTO exports VALUES
(2015, 55.2, 45.0, 'ארה"ב'),
(2016, 54.0, 46.2, 'ארה"ב'),
(2017, 60.1, 47.5, 'ארה"ב'),
(2018, 65.4, 48.1, 'ארה"ב'),
(2019, 68.6, 49.3, 'ארה"ב'),
(2020, 58.9, 52.1, 'ארה"ב'),
(2021, 73.5, 53.4, 'ארה"ב'),
(2022, 82.1, 54.2, 'ארה"ב'),
(2023, 75.4, 55.0, 'ארה"ב'),
(2024, 71.2, 54.8, 'ארה"ב');

-- נתוני שוק הדיור (רבעוני)
CREATE TABLE housing_market (
    year      INTEGER,
    quarter   INTEGER,
    district  TEXT,
    avg_price INTEGER,   -- מחיר ממוצע לדירה 4 חדרים (₪)
    transactions INTEGER, -- מספר עסקאות
    PRIMARY KEY (year, quarter, district)
);

INSERT INTO housing_market VALUES
(2022, 1, 'תל אביב',   3800000, 2100),
(2022, 1, 'ירושלים',   2600000, 1800),
(2022, 1, 'חיפה',      1700000, 1200),
(2022, 1, 'מרכז',      2900000, 3200),
(2022, 2, 'תל אביב',   3950000, 1950),
(2022, 2, 'ירושלים',   2700000, 1700),
(2022, 2, 'חיפה',      1750000, 1150),
(2022, 2, 'מרכז',      3050000, 3000),
(2022, 3, 'תל אביב',   4100000, 1800),
(2022, 3, 'ירושלים',   2780000, 1650),
(2022, 3, 'חיפה',      1800000, 1100),
(2022, 3, 'מרכז',      3150000, 2850),
(2022, 4, 'תל אביב',   4050000, 1750),
(2022, 4, 'ירושלים',   2720000, 1620),
(2022, 4, 'חיפה',      1780000, 1080),
(2022, 4, 'מרכז',      3100000, 2800),
(2023, 1, 'תל אביב',   3900000, 1500),
(2023, 1, 'ירושלים',   2650000, 1400),
(2023, 1, 'חיפה',      1720000, 950),
(2023, 1, 'מרכז',      3000000, 2400),
(2023, 2, 'תל אביב',   3850000, 1450),
(2023, 2, 'ירושלים',   2630000, 1380),
(2023, 2, 'חיפה',      1710000, 930),
(2023, 2, 'מרכז',      2980000, 2350),
(2023, 3, 'תל אביב',   3820000, 1420),
(2023, 3, 'ירושלים',   2610000, 1360),
(2023, 3, 'חיפה',      1700000, 910),
(2023, 3, 'מרכז',      2960000, 2300),
(2023, 4, 'תל אביב',   3780000, 1380),
(2023, 4, 'ירושלים',   2590000, 1340),
(2023, 4, 'חיפה',      1690000, 890),
(2023, 4, 'מרכז',      2940000, 2250);
```

---

## חלק א – GROUP BY: ניתוח לפי קטגוריות

### הבעיה שGROUP BY פותרת

`SELECT AVG(avg_price) FROM housing_market` מחזיר ממוצע כולל.
אבל מה אם רוצים ממוצע **לכל מחוז בנפרד**?

```sql
-- ממוצע מחיר דיור לפי מחוז
SELECT
    district,
    AVG(avg_price)     AS avg_price,
    SUM(transactions)  AS total_transactions,
    COUNT(*)           AS num_quarters
FROM housing_market
GROUP BY district;
```

**כלל ברזל:** כל עמודה ב-SELECT שאינה פונקציית אגרגציה **חייבת** להופיע ב-GROUP BY.

### GROUP BY על מספר עמודות

```sql
-- ממוצע מחיר לפי שנה ומחוז
SELECT
    year,
    district,
    AVG(avg_price)    AS avg_price,
    SUM(transactions) AS total_transactions
FROM housing_market
GROUP BY year, district
ORDER BY year, avg_price DESC;
```

### HAVING – סינון אחרי אגרגציה

**ההבדל המהותי:**
- `WHERE` → מסנן **לפני** האגרגציה (על שורות בודדות)
- `HAVING` → מסנן **אחרי** האגרגציה (על קבוצות)

```sql
-- מחוזות שממוצע מחירם מעל 2.5M
SELECT
    district,
    AVG(avg_price) AS avg_price
FROM housing_market
GROUP BY district
HAVING AVG(avg_price) > 2500000;

-- שנים עם יותר מ-10,000 עסקאות סה"כ
SELECT
    year,
    SUM(transactions) AS total_transactions
FROM housing_market
GROUP BY year
HAVING SUM(transactions) > 10000;
```

### שאילתת GROUP BY מלאה עם WHERE + HAVING

```sql
-- מחוזות (לא חיפה) עם ממוצע מחיר מעל 2M בשנת 2023
SELECT
    district,
    AVG(avg_price)    AS avg_price,
    SUM(transactions) AS total_transactions
FROM housing_market
WHERE year = 2023
  AND district != 'חיפה'
GROUP BY district
HAVING AVG(avg_price) > 2000000
ORDER BY avg_price DESC;
```

**סדר פעולות ב-SQL (חשוב להבין):**
```
1. FROM       ← מאיזו טבלה
2. WHERE      ← סנן שורות
3. GROUP BY   ← קבץ
4. HAVING     ← סנן קבוצות
5. SELECT     ← בחר עמודות
6. ORDER BY   ← מיין
7. LIMIT      ← הגבל
```

---

## חלק ב – JOIN: מיזוג טבלאות

### למה JOIN?

כי נתונים אמיתיים מפוצלים בין טבלאות רבות. JOIN מחבר ביניהן.

```
macro_annual          exports
+-----------+         +-----------+
| year 2022 |---JOIN--|  year 2022|
| gdp: 6.5% |    |    | exp: 82.1B|
+-----------+    |    +-----------+
                 |
                 על בסיס year = year
```

### INNER JOIN

מחזיר **רק שורות שיש להן התאמה בשתי הטבלאות**.

```sql
-- מיזוג נתוני מאקרו עם נתוני ייצוא
SELECT
    m.year,
    m.gdp_growth,
    m.inflation,
    e.exports_bn_usd,
    e.hi_tech_share_pct
FROM macro_annual AS m
INNER JOIN exports AS e ON m.year = e.year
ORDER BY m.year;
```

**טיפ:** השתמש ב-aliases (`m`, `e`) לשמות קצרים. הופך שאילתות קלות לקריאה.

### שאילתה עם JOIN + WHERE + ORDER

```sql
-- שנים עם צמיחה > 3% וייצוא > 65B
SELECT
    m.year,
    m.gdp_growth,
    e.exports_bn_usd
FROM macro_annual AS m
JOIN exports AS e ON m.year = e.year
WHERE m.gdp_growth > 3
  AND e.exports_bn_usd > 65
ORDER BY m.gdp_growth DESC;
```

### שאילתה כלכלית: האם ייצוא גבוה מוביל לצמיחה?

```sql
SELECT
    m.year,
    m.gdp_growth,
    e.exports_bn_usd,
    ROUND(e.exports_bn_usd / m.gdp_growth, 1) AS exports_per_gdp_point
FROM macro_annual AS m
JOIN exports AS e ON m.year = e.year
WHERE m.gdp_growth > 0
ORDER BY exports_per_gdp_point;
```

### LEFT JOIN

מחזיר **כל השורות מהטבלה השמאלית**, גם אם אין התאמה בטבלה הימנית.

**מתי שימושי?** כשנתוני ייצוא חסרים לחלק מהשנים:

```sql
SELECT
    m.year,
    m.gdp_growth,
    e.exports_bn_usd  -- יהיה NULL אם אין נתוני ייצוא
FROM macro_annual AS m
LEFT JOIN exports AS e ON m.year = e.year
ORDER BY m.year;
```

### ויזואליזציה של סוגי JOIN

```
                INNER JOIN:
תמ"ג:   [2015][2016][2017][2018][2019][2020][2021][2022][2023][2024]
ייצוא:  [2015][2016][2017][2018][2019][2020][2021][2022][2023][2024]
תוצאה: [████][████][████][████][████][████][████][████][████][████]

                LEFT JOIN (macro LEFT JOIN exports):
תמ"ג:   [2015][2016][2017][████][2018][...]
ייצוא:  [2015][2016][2017][ -- ][2018][...]  ← 2018 חסר מהייצוא
תוצאה: [2015][2016][2017][2018,NULL][2018][...]

                RIGHT JOIN:
הופכי LEFT JOIN – כל הטבלה הימנית + NULL לשמאלית
```

### JOIN שלישי – מיזוג שלוש טבלאות

```sql
SELECT
    m.year,
    m.gdp_growth,
    m.inflation,
    e.exports_bn_usd,
    p.district,
    p.population
FROM macro_annual AS m
JOIN exports AS e ON m.year = e.year
JOIN population_district AS p ON m.year = p.year
WHERE m.year >= 2022
ORDER BY m.year, p.district;
```

---

## חלק ג – Subqueries

### מה זה Subquery?

שאילתה **בתוך** שאילתה. מאפשרת לחשב ביניים ולהשתמש בתוצאה.

### 1. Subquery ב-WHERE

```sql
-- שנים עם ייצוא מעל הממוצע
SELECT year, exports_bn_usd
FROM exports
WHERE exports_bn_usd > (SELECT AVG(exports_bn_usd) FROM exports)
ORDER BY exports_bn_usd DESC;
```

הסבר: קודם מחשב `SELECT AVG(...)` ← מקבל 66.5 (לדוגמה) ← אחר כך מסנן WHERE > 66.5.

### 2. Subquery ב-FROM (Derived Table)

```sql
-- ממוצע מחיר דיור לפי מחוז, ואז מיין לפי מחיר
SELECT district, avg_price
FROM (
    SELECT
        district,
        AVG(avg_price) AS avg_price
    FROM housing_market
    GROUP BY district
) AS district_averages
WHERE avg_price > 2000000
ORDER BY avg_price DESC;
```

### 3. Correlated Subquery: שאילתה בתוך שאילתה שתלויה בשורה החיצונית

```sql
-- לכל מחוז, מצא את הרבעון עם המחיר הגבוה ביותר
SELECT
    h1.district,
    h1.year,
    h1.quarter,
    h1.avg_price
FROM housing_market AS h1
WHERE h1.avg_price = (
    SELECT MAX(h2.avg_price)
    FROM housing_market AS h2
    WHERE h2.district = h1.district  -- תלוי בשורה החיצונית
);
```

### Subquery עם IN

```sql
-- כל השנים שהייצוא בהן היה מעל 70B (גישה אלטרנטיבית ל-JOIN)
SELECT year, gdp_growth, inflation
FROM macro_annual
WHERE year IN (
    SELECT year FROM exports WHERE exports_bn_usd > 70
);
```

---

## חלק ד – NULL Handling

### מה זה NULL?

`NULL` ≠ 0, ≠ "", ≠ כלום. NULL = **ערך חסר/לא ידוע**.

```sql
-- בדיקה ל-NULL
SELECT * FROM housing_market
WHERE avg_price IS NULL;

SELECT * FROM housing_market
WHERE avg_price IS NOT NULL;
```

### COALESCE – ערך ברירת מחדל ל-NULL

```sql
-- אם exports_bn_usd חסר, השתמש ב-0
SELECT
    m.year,
    m.gdp_growth,
    COALESCE(e.exports_bn_usd, 0) AS exports_or_zero
FROM macro_annual AS m
LEFT JOIN exports AS e ON m.year = e.year;
```

### NULL בפונקציות אגרגציה

חשוב לדעת: `AVG()`, `SUM()`, `COUNT(column)` מתעלמים מ-NULL אוטומטית.
`COUNT(*)` סופר **את כל השורות** כולל NULL.

---

## חלק ה – שאילתות כלכליות מורכבות

### ניתוח 1: מחזור כלכלי ישראלי

```sql
-- חלק את השנים לתקופות ונתח
SELECT
    CASE
        WHEN year BETWEEN 2015 AND 2019 THEN 'לפני קורונה'
        WHEN year = 2020               THEN 'קורונה'
        WHEN year BETWEEN 2021 AND 2021 THEN 'התאוששות'
        WHEN year BETWEEN 2022 AND 2024 THEN 'אחרי קורונה + מלחמה'
    END AS period,
    COUNT(*) AS num_years,
    ROUND(AVG(gdp_growth), 2)    AS avg_gdp_growth,
    ROUND(AVG(inflation), 2)     AS avg_inflation,
    ROUND(AVG(unemployment), 2)  AS avg_unemployment,
    ROUND(AVG(interest_rate), 2) AS avg_interest_rate
FROM macro_annual
GROUP BY period
ORDER BY MIN(year);
```

### ניתוח 2: קורלציה ריבית-מחירי דיור

```sql
-- כיצד הריבית הגבוהה ב-2022-2023 השפיעה על שוק הדיור?
SELECT
    m.year,
    m.interest_rate,
    AVG(h.avg_price)      AS avg_housing_price,
    SUM(h.transactions)   AS total_transactions
FROM macro_annual AS m
JOIN housing_market AS h ON m.year = h.year
GROUP BY m.year, m.interest_rate
ORDER BY m.year;
```

### ניתוח 3: ייצוא ותמ"ג

```sql
-- האם ייצוא מסביר צמיחה? חשב את תרומת הייצוא
SELECT
    m.year,
    m.gdp_growth,
    e.exports_bn_usd,
    -- נורמל ייצוא ל-% מתמ"ג (הנח תמ"ג ~600B USD)
    ROUND(e.exports_bn_usd / 600 * 100, 1) AS exports_pct_gdp,
    -- שינוי בייצוא שנה לשנה
    ROUND(e.exports_bn_usd -
        LAG(e.exports_bn_usd, 1) OVER (ORDER BY e.year), 1
    ) AS exports_yoy_change
FROM macro_annual AS m
JOIN exports AS e ON m.year = e.year
ORDER BY m.year;
```

*(שים לב: `LAG()` = Window Function – נלמד לעומק ב-Week 7)*

### ניתוח 4: פערים בין מחוזות

```sql
-- פער מחירי הדיור בין תל אביב לחיפה לאורך זמן
SELECT
    ta.year,
    ta.quarter,
    ta.avg_price AS ta_price,
    h.avg_price  AS haifa_price,
    ta.avg_price - h.avg_price        AS price_gap,
    ROUND(ta.avg_price * 1.0 / h.avg_price, 2) AS ta_vs_haifa_ratio
FROM housing_market AS ta
JOIN housing_market AS h
    ON ta.year = h.year
    AND ta.quarter = h.quarter
WHERE ta.district = 'תל אביב'
  AND h.district = 'חיפה'
ORDER BY ta.year, ta.quarter;
```

*(Self-JOIN: אותה טבלה פעמיים!)*

---

## חלק ו – CREATE TABLE AS SELECT

שמור תוצאת שאילתה כטבלה חדשה:

```sql
-- צור טבלת סיכום מחוזי
CREATE TABLE district_summary AS
SELECT
    district,
    AVG(avg_price)      AS avg_price_all_time,
    SUM(transactions)   AS total_transactions,
    COUNT(*)            AS num_periods,
    MAX(avg_price)      AS peak_price,
    MIN(avg_price)      AS trough_price
FROM housing_market
GROUP BY district;

-- בדוק
SELECT * FROM district_summary ORDER BY avg_price_all_time DESC;
```

---

## משימות השבוע

### משימה 1: GROUP BY + HAVING (25 נקודות)

כתוב שאילתות:

1. ממוצע מחיר דיור לפי **שנה**, ממוין מגבוה לנמוך
2. מחוזות עם יותר מ-8,000 עסקאות סה"כ (כל השנים)
3. שנים שבהן ממוצע מחירי הדיור היה מעל 2.8 מיליון
4. לכל מחוז: מחיר מקסימלי, מינימלי, ממוצע – וגם **מקדם וריאציה** (`MAX-MIN / AVG`)

### משימה 2: JOINs (35 נקודות)

1. **INNER JOIN:** מיזוג `macro_annual` + `exports` – כל שנה עם כל הנתונים
2. **Correlated:** לכל שנה, הצג את המחוז הכי יקר ואת המחוז הכי זול (השתמש ב-Subquery)
3. **Self-JOIN:** עבור כל זוג מחוזות (A,B), חשב את הפער הממוצע במחירים

### משימה 3: ניתוח כלכלי מקיף (40 נקודות)

כתוב שאילתה אחת (מורכבת!) שמחזירה:
- לכל שנה: ריבית, אינפלציה, ריבית ריאלית, ייצוא
- תוספת: סיווג תקופה (לפני/אחרי העלאת ריבית)
- תוספת: ממוצע מחיר דיור באותה שנה (JOIN עם housing_market)
- ממויין לפי שנה

**שאלת חקר:** האם ניתן לזהות את ההשפעה של העלאת הריבית על מחירי הדיור?
כתוב תשובה של 5-8 משפטים בקובץ הסיכום.

---

## הגשה

```
Members/YourName/Week_06/
├── week06_queries.sql         ← כל השאילתות
└── week06_housing_analysis.md ← ניתוח שוק הדיור
```

---

**השבוע הבא:** SQL מתקדם – Window Functions, CTEs, ושילוב Python+SQL → [שבוע 7](../Week_07_SQL_Advanced/README.md)
