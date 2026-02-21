# מסלול הלמידה – EconLab PPE

## עקרון המסלול

המסלול בנוי כ**פירמידה של כלים**: כל שלב בונה על הקודם.
מתחילים מהתקנת סביבה, עוברים דרך Excel → SQL → Python → R → ויזואליזציה → BI Tools → DSGE.

**אין צורך בידע קודם בתכנות.** נתחיל מאפס מוחלט.

**עקרון הלימוד:** כל כלי מקבל **2-3 שבועות** – מרמה מתחילה מוחלטת ועד רמה מקצועית.
לא מדלגים, לא מזרזים. בסוף כל אחד יידע לעשות עבודת כלכלן אמיתית.

---

## מפת הדרכים הכוללת

```
שבוע  1      → הכנת סביבה (Git, Python, R, VS Code, DBeaver)
שבועות 2-4   → Excel (מאפס → בינוני → מתקדם + Dashboard)
שבועות 5-7   → SQL  (מאפס → בינוני → מתקדם + Python+SQL)
שבועות 8-10  → Python + Pandas (מאפס → בסיסי → מתקדם)
שבועות 11-12 → Python + APIs (בנק ישראל, הלמ"ס, OECD, World Bank)
שבועות 13-15 → R (יסודות → אקונומטריקה → Time Series)
שבועות 16-18 → ויזואליזציה מתקדמת (matplotlib → plotly → ggplot2)
שבועות 19-21 → Power BI / Tableau (Dashboards לקובעי מדיניות)
שבועות 22-24 → DSGE ומודלים מאקרו-כלכליים דינמיים
```

**סה"כ: ~24 שבועות** לרמת כלכלן נתונים מקצועי.

---

## מודול 1 – הכנת הסביבה

### שבוע 1 – Setup: בניית מחשב של כלכלן נתונים
**כלים:** Git, GitHub, Python, R, RStudio, VS Code, DBeaver, Jupyter

**מה לומדים:**
- למה כל כלי קיים ומה תפקידו
- התקנת כל הכלים + אימות
- Git: מחזור commit/push/pull
- GitHub: יצירת Portfolio מקצועי
- סביבה וירטואלית Python
- Jupyter Notebook ראשון עם גרף

📋 [משימה 1 – Setup](Assignments/Week_01_Setup/README.md)

---

## מודול 2 – Excel: מהיסוד לניתוח כלכלי מתקדם

### שבוע 2 – Excel מאפס: יסודות
**כלים:** Microsoft Excel / Google Sheets

**מה לומדים:**
- ממשק Excel: תאים, שורות, עמודות, גיליונות
- הזנת נתונים, עיצוב, רוחב עמודות
- פורמולות ראשונות: `=SUM()`, `=AVERAGE()`, `=COUNT()`, `=IF()`
- Absolute vs Relative References (`$A$1` מול `A1`)
- מיון, סינון, חיפוש (Ctrl+F)
- גרף קו ראשון: צמיחת תמ"ג ישראל

**נתונים:** נתוני מאקרו ישראל 2015-2024 מ-boi.org.il

📋 [משימה 2 – Excel Basics](Assignments/Week_02_Excel_Basics/README.md)

---

### שבוע 3 – Excel בינוני: ניתוח נתונים
**כלים:** Excel

**מה לומדים:**
- `VLOOKUP` ו-`INDEX/MATCH` – מיזוג נתונים
- `SUMIF`, `AVERAGEIF`, `COUNTIFS` – ניתוח לפי תנאים
- Conditional Formatting – Heat Maps, Data Bars
- Data Validation – מניעת שגיאות הזנה
- Pivot Tables – ניתוח רב-ממדי
- Slicers ו-Timelines – ממשק סינון ויזואלי
- גרפים מקצועיים: Combo, Scatter, Bar

**פרויקט:** ניתוח פערי שכר ומחיר דיור בין מחוזות ישראל

📋 [משימה 3 – Excel Intermediate](Assignments/Week_03_Excel_Intermediate/README.md)

---

### שבוע 4 – Excel מתקדם: Power Query, פיננסים, דשבורד
**כלים:** Excel (Power Query, Power Pivot)

**מה לומדים:**
- Power Query: ETL ב-Excel (ייבוא, ניקוי, Unpivot, מיזוג, ריענון אוטומטי)
- פונקציות פיננסיות: `NPV`, `IRR`, `PMT`, `FV` – הערכת פרויקטים ממשלתיים
- `XLOOKUP`, `SUMPRODUCT`, `INDIRECT` – פונקציות מתקדמות
- Sparklines ו-Waterfall Charts
- בניית Dashboard מאקרו-כלכלי מלא
- הגנה ושיתוף קובץ

**פרויקט מסכם:** דשבורד "השפעת העלאות הריבית על המשק הישראלי 2022-2024"

📋 [משימה 4 – Excel Advanced](Assignments/Week_04_Excel_Advanced/README.md)

---

## מודול 3 – SQL: שפת הנתונים של העולם

### שבוע 5 – SQL מאפס: יסודות
**כלים:** DBeaver, SQLite

**מה לומדים:**
- מה זה בסיס נתונים ולמה עדיף על Excel לנתונים גדולים
- `CREATE TABLE`, `INSERT INTO`
- `SELECT` + עמודות ספציפיות
- `WHERE` עם תנאים: `=`, `>`, `<`, `BETWEEN`, `LIKE`, `IN`, `AND`, `OR`
- `ORDER BY`, `LIMIT`
- פונקציות אגרגציה: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- עמודות מחושבות ו-`CASE WHEN`
- `UPDATE`, `DELETE`

**בסיס נתונים:** `israel_economy.db` עם נתוני מאקרו 2015-2024

📋 [משימה 5 – SQL Basics](Assignments/Week_05_SQL_Basics/README.md)

---

### שבוע 6 – SQL בינוני: GROUP BY, JOINs, Subqueries
**כלים:** DBeaver, SQLite

**מה לומדים:**
- `GROUP BY` – ניתוח לפי קטגוריות
- `HAVING` – סינון אחרי אגרגציה
- `INNER JOIN`, `LEFT JOIN` – מיזוג טבלאות
- Self-JOIN – אותה טבלה פעמיים
- Subqueries: ב-WHERE, ב-FROM, Correlated
- NULL handling: `IS NULL`, `COALESCE`
- `CREATE TABLE AS SELECT`

**בסיס נתונים מורחב:** טבלאות `exports` ו-`housing_market`

**שאלת מחקר:** כיצד הריבית הגבוהה השפיעה על שוק הדיור הישראלי?

📋 [משימה 6 – SQL Intermediate](Assignments/Week_06_SQL_Intermediate/README.md)

---

### שבוע 7 – SQL מתקדם: Window Functions, CTEs, Python+SQL
**כלים:** DBeaver, SQLite, Python

**מה לומדים:**
- CTEs (`WITH`) – שאילתות מורכבות בשלבים קריאים
- Window Functions:
  - `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` – דירוג
  - `LAG()`, `LEAD()` – השוואה לתקופות קודמות/עתידיות
  - Running Total, Moving Average (ממוצע נע)
  - `PERCENT_RANK()` – אחוזונים
- String Functions: `SUBSTR`, `TRIM`, `REPLACE`, `||`
- Date Functions: `strftime()`
- Python + SQLite: `pd.read_sql_query()`
- גרפים מלאים: SQL → Pandas → Matplotlib

**פרויקט מסכם SQL:** ניתוח מחקרי מלא – שוק הדיור הישראלי + מדיניות ריבית

📋 [משימה 7 – SQL Advanced](Assignments/Week_07_SQL_Advanced/README.md)

---

## מודול 4 – Python + Pandas: ניתוח נתונים מלא

### שבוע 8 – Python מאפס
**כלים:** Python, VS Code

**מה לומדים:**
- משתנים, טיפוסי נתונים: `int`, `float`, `str`, `bool`
- רשימות, מילונים, קבוצות, tuple
- לולאות `for`, `while`
- תנאים: `if`, `elif`, `else`
- פונקציות: `def`, `return`
- קריאה/כתיבה לקבצים, List Comprehensions

📋 [משימה 8 – Python Basics](Assignments/Week_08_Python_Basics/README.md)

---

### שבוע 9 – Pandas בסיסי
**כלים:** Python, pandas, Jupyter

**מה לומדים:**
- `read_csv()`, `read_excel()`
- DataFrame: בחירה, סינון, מיון
- `groupby()`, `apply()`, `value_counts()`
- ניקוי נתונים: `dropna()`, `fillna()`, `duplicated()`

📋 [משימה 9 – Pandas Basics](Assignments/Week_09_Pandas_Basics/README.md)

---

### שבוע 10 – Pandas מתקדם: Time Series
**כלים:** Python, pandas, matplotlib, numpy

**מה לומדים:**
- `pd.to_datetime()`, Resampling (`resample`)
- `rolling()` – ממוצע נע
- `merge()`, `concat()`, `pivot_table()`, `melt()`
- matplotlib שליטה מלאה + ייצוא לפרסום

📋 [משימה 10 – Pandas Advanced](Assignments/Week_10_Pandas_Advanced/README.md)

---

## מודול 5 – Python + APIs

### שבוע 11 – APIs ישראליים
**כלים:** Python, requests

**מה לומדים:**
- REST API, HTTP requests, JSON
- **בנק ישראל (BOI):** ריבית, שע"ח, CPI
- **הלמ"ס (CBS):** תעסוקה, שכר
- ניהול מפתחות: `.env`

📋 [משימה 11 – APIs Israel](Assignments/Week_11_APIs_Israel/README.md)

---

### שבוע 12 – APIs בין-לאומיים
**כלים:** Python, wbgapi, fredapi

**מה לומדים:**
- **הבנק העולמי:** `wbgapi`
- **OECD:** SDMX API
- **FRED:** `fredapi`
- Pipeline נתונים אוטומטי + Cache

📋 [משימה 12 – APIs International](Assignments/Week_12_APIs_International/README.md)

---

## מודול 6 – R: אקונומטריקה ומודלים סטטיסטיים

### שבוע 13 – R יסודות
📋 [משימה 13 – R Basics](Assignments/Week_13_R_Basics/README.md)

### שבוע 14 – R: אקונומטריקה מעשית
📋 [משימה 14 – R Econometrics](Assignments/Week_14_R_Econometrics/README.md)

### שבוע 15 – R: Time Series וחיזוי
📋 [משימה 15 – R Time Series](Assignments/Week_15_R_Time_Series/README.md)

---

## מודול 7 – ויזואליזציה מתקדמת

### שבוע 16 – matplotlib + seaborn
📋 [משימה 16 – matplotlib Advanced](Assignments/Week_16_Matplotlib/README.md)

### שבוע 17 – Plotly: גרפים אינטראקטיביים
📋 [משימה 17 – Plotly Interactive](Assignments/Week_17_Plotly/README.md)

### שבוע 18 – ggplot2 ו-R Markdown
📋 [משימה 18 – ggplot2 & RMarkdown](Assignments/Week_18_ggplot2_RMarkdown/README.md)

---

## מודול 8 – Power BI / Tableau

### שבוע 19 – Power BI יסודות
📋 [משימה 19 – Power BI Basics](Assignments/Week_19_PowerBI_Basics/README.md)

### שבוע 20 – Power BI מתקדם
📋 [משימה 20 – Power BI Advanced](Assignments/Week_20_PowerBI_Advanced/README.md)

### שבוע 21 – Tableau Public
📋 [משימה 21 – Tableau](Assignments/Week_21_Tableau/README.md)

---

## מודול 9 – DSGE: מודלים מאקרו-כלכליים דינמיים

### שבוע 22 – מבוא ל-DSGE
📋 [משימה 22 – DSGE Intro](Assignments/Week_22_DSGE_Intro/README.md)

### שבוע 23 – DSGE: אמידה וסימולציה
📋 [משימה 23 – DSGE Estimation](Assignments/Week_23_DSGE_Estimation/README.md)

### שבוע 24 – DSGE: NK ופרויקט מסכם
📋 [משימה 24 – DSGE Capstone](Assignments/Week_24_DSGE_Capstone/README.md)

---

## מקורות נתונים מרכזיים

| מקור | כיסוי | API? | מדריך |
|---|---|---|---|
| בנק ישראל | ריבית, שע"ח, אינפלציה | ✅ SDMX | [Cookbook](Cookbook/boi_api.md) |
| הלמ"ס | אוכלוסייה, תעסוקה, שכר | ⚠️ חלקי | [Cookbook](Cookbook/cbs_api.md) |
| הבנק העולמי | תמ"ג, סחר, חוב, 200+ מדינות | ✅ wbgapi | [Cookbook](Cookbook/worldbank_api.md) |
| OECD | השוואה ל-38 מדינות | ✅ SDMX | [Cookbook](Cookbook/oecd_api.md) |
| FRED | סדרות מאקרו אמריקאיות | ✅ fredapi | - |
| IMF WEO | תחזיות עולמיות | ✅ | - |

---

## תיק העבודות שלך

בסוף המסלול, התיקייה `Members/YourName/` תהיה **Portfolio** אמיתי שמכיל:
- קוד Python ו-R שכתבת
- Notebooks עם ניתוחים על נתונים ישראליים ובין-לאומיים
- דשבורד Power BI / Tableau
- מחקר עצמאי מלא עם מודל DSGE

**זה מה שמראים בראיון עבודה.**

---

*עודכן: 2025 | EconLab PPE*
