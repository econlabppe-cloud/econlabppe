# שבוע 5 – SQL מאפס: שפת הנתונים של העולם


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=HXV3zeQKqGY](https://www.youtube.com/watch?v=HXV3zeQKqGY) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=zsjfGDiOcTo](https://www.youtube.com/watch?v=zsjfGDiOcTo) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=ztHopE5Wnpc](https://www.youtube.com/watch?v=ztHopE5Wnpc) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=HXV3zeQKqGY >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=7S_tz1z_5bA >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=p3qvj9hO_EQ >}}

:::
## למה SQL? ולמה דווקא עכשיו?

**Excel טוב ל:**
- ניתוח ראשוני
- גרפים מהירים
- פרזנטציות

**SQL טוב ל:**
- נתונים גדולים (מיליוני שורות – Excel נקרס)
- שאילתות מדויקות ("תן לי כל עסקאות מחוז תל אביב עם שכר > 15,000 שנפסקו אחרי 2020")
- מספר מקורות נתונים ביחד (JOIN)
- אוטומציה (אותה שאילתה על נתונים חדשים)

**מי משתמש ב-SQL?**
- **בנק ישראל:** שאילתות על בסיסי נתונים של מאזני בנקים
- **הלמ"ס:** סקרי שכר, תעסוקה, מחירי דיור
- **משרד האוצר:** נתוני מע"מ, מס הכנסה
- **כל FinTech:** ניתוח עסקאות, זיהוי הונאות

---

## חלק א – מה זה בסיס נתונים?

### Excel מול בסיס נתונים

| תכונה | Excel | בסיס נתונים (SQL) |
|---|---|---|
| **גודל מקסימלי** | ~1M שורות | מיליארדי שורות |
| **מספר משתמשים** | 1 בו-זמנית | אלפים בו-זמנית |
| **עקביות נתונים** | ידנית | אוטומטית (Foreign Keys) |
| **שאילתות מורכבות** | קשה | מהיר ועוצמתי |
| **גיבוי** | ידני | אוטומטי |

### מבנה בסיס נתונים

```
בסיס נתונים (Database): israel_economy
├── טבלה (Table): macro_annual
│   ├── עמודה: year (INTEGER)
│   ├── עמודה: gdp_growth (REAL)
│   ├── עמודה: inflation (REAL)
│   └── עמודה: unemployment (REAL)
│
├── טבלה (Table): population_district
│   ├── עמודה: year (INTEGER)
│   ├── עמודה: district (TEXT)
│   └── עמודה: population (INTEGER)
│
└── טבלה (Table): exports
    ├── עמודה: year (INTEGER)
    └── עמודה: exports_bn_usd (REAL)
```

### סוגי בסיסי נתונים

| סוג | דוגמאות | מתי משתמשים |
|---|---|---|
| **SQLite** | קובץ .db | פיתוח, לימוד, פרויקטים קטנים |
| **PostgreSQL** | Postgres | פרודקשן, ניתוח כלכלי |
| **MySQL** | MySQL | אתרי web |
| **SQL Server** | MSSQL | ארגונים גדולים, ממשלה |
| **BigQuery** | Google | Big Data, עשרות מיליארדי שורות |

**נשתמש ב-SQLite** – פשוט להתחיל, לא צריך שרת.

---

## חלק ב – הכנת הסביבה

### התקנת DBeaver (אם עוד לא התקנת)

1. כנס ל-[dbeaver.io](https://dbeaver.io/) → Community Edition
2. התקן

### יצירת בסיס נתונים SQLite

1. פתח DBeaver
2. File → New Database Connection
3. בחר **SQLite**
4. Database: לחץ "Create" → שמור בשם `israel_economy.db` בתיקייה שלך
5. לחץ Finish

תראה את בסיס הנתונים בעץ השמאלי.

### פתח SQL Editor

לחץ על בסיס הנתונים → SQL Editor → Open SQL Script

---

## חלק ג – יצירת הטבלאות הראשונות

### CREATE TABLE

```sql
-- יצירת טבלת נתוני מאקרו שנתיים
CREATE TABLE macro_annual (
    year          INTEGER PRIMARY KEY,  -- מפתח ראשי (ייחודי)
    gdp_growth    REAL,                 -- צמיחת תמ"ג %
    inflation     REAL,                 -- אינפלציה %
    unemployment  REAL,                 -- אבטלה %
    interest_rate REAL                  -- ריבית בנק ישראל %
);
```

**מה המשמעות:**
- `INTEGER` = מספר שלם
- `REAL` = מספר עם נקודה עשרונית
- `TEXT` = מחרוזת
- `PRIMARY KEY` = הערך הזה ייחודי, לא יכולים להיות שתי שורות עם אותו year

לחץ **Ctrl+Enter** להריץ.

### INSERT INTO – הכנסת נתונים

```sql
INSERT INTO macro_annual VALUES
(2015, 2.5, -0.6, 5.3, 0.1),
(2016, 4.0,  0.0, 4.8, 0.1),
(2017, 3.5,  0.2, 4.2, 0.1),
(2018, 4.2,  0.8, 4.0, 0.1),
(2019, 3.8,  0.8, 3.8, 0.25),
(2020, -1.9, -0.6, 4.3, 0.1),
(2021, 8.6,  1.5, 5.0, 0.1),
(2022, 6.5,  5.1, 3.7, 3.25),
(2023, 2.0,  4.2, 3.5, 4.75),
(2024, 1.1,  3.5, 4.2, 4.5);
```

### SELECT – קריאת נתונים (הכי חשוב!)

```sql
-- קרא הכל מהטבלה
SELECT * FROM macro_annual;
```

`*` = כל העמודות. תראה את כל הנתונים שהכנסת.

---

## חלק ד – SELECT: אמנות השאילתות

### 1. בחירת עמודות ספציפיות

```sql
-- רק שנה ואינפלציה
SELECT year, inflation
FROM macro_annual;
```

### 2. ORDER BY – מיון

```sql
-- ממוין לפי אינפלציה מגבוהה לנמוכה
SELECT year, inflation
FROM macro_annual
ORDER BY inflation DESC;

-- מנמוכה לגבוהה
SELECT year, gdp_growth
FROM macro_annual
ORDER BY gdp_growth ASC;
```

`DESC` = Descending (יורד), `ASC` = Ascending (עולה, ברירת מחדל)

### 3. LIMIT – הגבלת תוצאות

```sql
-- 3 השנים עם הצמיחה הגבוהה ביותר
SELECT year, gdp_growth
FROM macro_annual
ORDER BY gdp_growth DESC
LIMIT 3;
```

### 4. WHERE – סינון לפי תנאי

```sql
-- שנים עם צמיחה חיובית
SELECT year, gdp_growth
FROM macro_annual
WHERE gdp_growth > 0;

-- שנים עם אינפלציה גבוהה מ-2%
SELECT year, inflation
FROM macro_annual
WHERE inflation > 2;

-- שנת המיתון (צמיחה שלילית)
SELECT year, gdp_growth
FROM macro_annual
WHERE gdp_growth < 0;
```

### 5. תנאים מרובים: AND, OR, NOT

```sql
-- שנים עם אינפלציה גבוהה וצמיחה טובה (סטגפלציה – אינפלציה בלי צמיחה)
SELECT year, gdp_growth, inflation
FROM macro_annual
WHERE inflation > 3 AND gdp_growth < 2;

-- שנים עם ריבית גבוהה מאוד OR מיתון
SELECT year, interest_rate, gdp_growth
FROM macro_annual
WHERE interest_rate > 3 OR gdp_growth < 0;

-- שנים עם ריבית לא שווה ל-0.1%
SELECT year, interest_rate
FROM macro_annual
WHERE interest_rate != 0.1;
```

### 6. BETWEEN – טווח

```sql
-- שנים 2019-2023
SELECT *
FROM macro_annual
WHERE year BETWEEN 2019 AND 2023;

-- ריבית בין 1% ל-5%
SELECT year, interest_rate
FROM macro_annual
WHERE interest_rate BETWEEN 1 AND 5;
```

### 7. IN – רשימה

```sql
-- שנים ספציפיות
SELECT year, gdp_growth
FROM macro_annual
WHERE year IN (2020, 2022, 2024);
```

### 8. LIKE – חיפוש בטקסט

*(שימושי כשיש עמודות טקסט)*

```sql
-- (לדוגמה, בטבלה עם שמות מחוזות)
SELECT * FROM population_district
WHERE district LIKE 'ת%';  -- מחוזות שמתחילים ב-ת

SELECT * FROM population_district
WHERE district LIKE '%רושלים%';  -- מכיל "רושלים"
```

- `%` = כל מחרוזת
- `_` = תו בודד

---

## חלק ה – פונקציות אגרגציה

### COUNT, SUM, AVG, MIN, MAX

```sql
-- כמה שנים יש בנתונים?
SELECT COUNT(*) AS number_of_years
FROM macro_annual;

-- ממוצע אינפלציה
SELECT AVG(inflation) AS avg_inflation
FROM macro_annual;

-- ממוצע אינפלציה בעשור האחרון
SELECT AVG(inflation) AS avg_inflation_decade
FROM macro_annual
WHERE year >= 2015;

-- אינפלציה מקסימלית ומינימלית
SELECT
    MAX(inflation) AS max_inflation,
    MIN(inflation) AS min_inflation,
    MAX(inflation) - MIN(inflation) AS range_inflation
FROM macro_annual;

-- צמיחה כוללת מצטברת (סכום שנתי – לא מדויק, אבל מתרגלים SUM)
SELECT SUM(gdp_growth) AS total_growth
FROM macro_annual;
```

### AS – שמות ידידותיים לעמודות

```sql
SELECT
    AVG(inflation)   AS "ממוצע אינפלציה",
    AVG(gdp_growth)  AS "ממוצע צמיחה",
    AVG(unemployment) AS "ממוצע אבטלה",
    AVG(interest_rate) AS "ממוצע ריבית"
FROM macro_annual;
```

---

## חלק ו – עמודות מחושבות

```sql
-- יצור עמודה מחושבת: ריבית ריאלית = ריבית נומינלית - אינפלציה
SELECT
    year,
    interest_rate,
    inflation,
    (interest_rate - inflation) AS real_interest_rate
FROM macro_annual;

-- פרשנות: ריבית ריאלית חיובית = בנק מרכזי מדכא כלכלה
-- ריבית ריאלית שלילית = מדיניות מרחיבה
```

```sql
-- שנה + קטגוריה
SELECT
    year,
    gdp_growth,
    CASE
        WHEN gdp_growth > 4  THEN 'צמיחה גבוהה'
        WHEN gdp_growth > 0  THEN 'צמיחה מתונה'
        ELSE                      'מיתון'
    END AS growth_category
FROM macro_annual
ORDER BY year;
```

`CASE WHEN` = בדיוק כמו `IF` ב-Excel.

---

## חלק ז – יצירת טבלה שנייה + הכנה ל-JOIN

```sql
-- טבלת אוכלוסייה לפי מחוז
CREATE TABLE population_district (
    year        INTEGER,
    district    TEXT,
    population  INTEGER,
    PRIMARY KEY (year, district)  -- מפתח מורכב
);

INSERT INTO population_district VALUES
(2022, 'תל אביב', 1380000),
(2022, 'ירושלים', 1100000),
(2022, 'חיפה',    990000),
(2022, 'צפון',    1350000),
(2022, 'דרום',    1300000),
(2022, 'מרכז',    2100000),
(2023, 'תל אביב', 1400000),
(2023, 'ירושלים', 1120000),
(2023, 'חיפה',    998000),
(2023, 'צפון',    1360000),
(2023, 'דרום',    1320000),
(2023, 'מרכז',    2130000);
```

---

## חלק ח – UPDATE ו-DELETE

### UPDATE – עדכון נתונים

```sql
-- עדכן נתון שגוי
UPDATE macro_annual
SET inflation = 5.2
WHERE year = 2022;

-- עדכן כמה עמודות בבת אחת
UPDATE macro_annual
SET gdp_growth = 1.2, unemployment = 4.3
WHERE year = 2024;
```

### DELETE – מחיקת נתונים

```sql
-- מחק שורה ספציפית
DELETE FROM macro_annual
WHERE year = 2015;

-- **זהירות!** DELETE ללא WHERE ימחק את כל הטבלה!
-- DELETE FROM macro_annual;  ← אל תריץ!
```

---

## משימות השבוע

### משימה 1: יצירת בסיס נתונים (20 נקודות)

צור בסיס נתונים `israel_economy.db` עם שתי הטבלאות:
- `macro_annual` (עם כל הנתונים כולל 2015-2024)
- `population_district` (עם הנתונים שלמעלה)

### משימה 2: שאילתות SELECT בסיסיות (30 נקודות)

כתוב שאילתות SQL לכל הבאות:

1. כל השנים ממוינות לפי ריבית מגבוהה לנמוכה
2. 5 השנים עם הצמיחה הגבוהה ביותר
3. שנים שבהן **גם** האינפלציה **וגם** האבטלה היו מעל הממוצע *(תרגם קודם את "ממוצע" לערך ספציפי)*
4. שנים עם ריבית ריאלית שלילית (ריבית - אינפלציה < 0)
5. מספר השנים עם צמיחה מעל 3%

### משימה 3: פונקציות אגרגציה (30 נקודות)

כתוב שאילתה אחת שמחזירה:
- ממוצע כל מדד (צמיחה, אינפלציה, אבטלה, ריבית) לשנים 2015-2019
- ממוצע כל מדד לשנים 2020-2024
- (רמז: שתי שאילתות נפרדות או CASE WHEN)

### משימה 4: CASE WHEN (20 נקודות)

צור שאילתה שמחזירה:
- שנה
- צמיחת תמ"ג
- סיווג צמיחה: "מיתון" / "צמיחה איטית" / "צמיחה נורמלית" / "צמיחה גבוהה"
- סיווג אינפלציה: "דפלציה" / "יציבות מחירים" / "אינפלציה מתונה" / "אינפלציה גבוהה"

---

## הגשה

```
Members/YourName/Week_05/
├── week05_queries.sql     ← כל השאילתות ממוספרות
└── week05_summary.md      ← 3 תובנות כלכליות
```

**בקובץ SQL:**
```sql
-- ==============================================
-- Week 5 SQL Queries – [שמך]
-- ==============================================

-- משימה 1: יצירת טבלאות
-- [קוד CREATE TABLE + INSERT]

-- -------------------------------------------
-- משימה 2, שאילתה 1: שנים ממוינות לפי ריבית
-- -------------------------------------------
SELECT ...
```

---

## שאלות להבנה עצמית

1. מה ההבדל בין `WHERE` ל-`HAVING`? (נלמד ב-Week 6)
2. למה `PRIMARY KEY` חשוב?
3. מה קורה אם מריצים `INSERT` עם `year` שכבר קיים?
4. מה ההבדל בין `COUNT(*)` ל-`COUNT(column_name)`?
5. מה עושה `ORDER BY year DESC, inflation ASC`?

---

**השבוע הבא:** SQL בינוני – GROUP BY, JOINs, ושאילתות מורכבות → [שבוע 6](../Week_06_SQL_Intermediate/README.md)
