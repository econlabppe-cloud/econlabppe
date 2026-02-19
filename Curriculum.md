# מסלול הלמידה – EconLab PPE

## עקרון המסלול

המסלול בנוי כ**פירמידה של כלים**: כל שלב בונה על הקודם.
מתחילים מ-Excel (ידידותי ומוכר) ומגיעים עד הרצת מודלי DSGE.

**אין צורך בידע קודם בתכנות.** נתחיל מאפס.

---

## מפת הדרכים

```
Excel  →  SQL  →  Python (Pandas)  →  Python (APIs)  →  R  →  Viz  →  BI Tools  →  DSGE
  1         2          3-4               5              6-7    8          9           10
```

---

## שבועות 1-10: פירוט

### שבוע 1 – הכנת הסביבה (Setup)
**כלים:** Git, GitHub, Python, R, RStudio, VS Code, DBeaver
**מה לומדים:**
- מה זה Git ולמה כלכלנים צריכים אותו
- יצירת תיקייה אישית ב-`Members/`
- התקנת כל הכלים הנדרשים

📋 [משימה 1](Assignments/Week_01_Setup/README.md)

---

### שבוע 2 – Excel: מהיסוד לניתוח כלכלי
**כלים:** Microsoft Excel / Google Sheets
**מה לומדים:**
- ניקוי נתונים: סינון, מיון, הסרת כפילויות
- Pivot Tables לסיכום נתוני GDP, תעסוקה, אינפלציה
- פונקציות כלכליות: NPV, IRR, VLOOKUP, INDEX-MATCH
- גרפים ראשוניים: תרשים עמודות, קווי, פיזורי

📋 [משימה 2](Assignments/Week_02_Excel/README.md)

---

### שבוע 3 – SQL: שאילתות על נתוני כלכלה
**כלים:** DBeaver, SQLite
**מה לומדים:**
- מה זה בסיס נתונים ולמה זה שונה מגיליון אקסל
- `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`
- `JOIN` בין טבלאות (לדוגמה: אוכלוסייה + תמ"ג לפי מחוז)
- שאילתות מצטברות: `SUM`, `AVG`, `COUNT`

📋 [משימה 3](Assignments/Week_03_SQL_Intro/README.md)

---

### שבוע 4 – Python + Pandas: ניתוח נתונים
**כלים:** Python, Jupyter Notebook, pandas
**מה לומדים:**
- הסביבה הוירטואלית ו-Jupyter Notebook
- קריאת CSV/Excel עם `pd.read_csv()`
- סינון, מיון, groupby
- ניתוח סדרה עתית: CPI, ריבית, שער חליפין

📋 [משימה 4](Assignments/Week_04_Python_Pandas/README.md)

---

### שבוע 5 – Python + APIs: גישה לנתונים כלכליים
**כלים:** Python, requests, wbgapi, pandas
**מה לומדים:**
- מה זה API ואיך מדברים איתו
- **בנק ישראל** – ריבית, שע"ח, מדד המחירים (SDMX)
- **הלמ"ס** – נתוני אוכלוסייה, תעסוקה
- **הבנק העולמי** – תמ"ג, חוב, סחר בין-לאומי
- **OECD** – השוואה בין-מדינתית
- ניהול מפתחות API בצורה בטוחה (`.env`)

📋 [משימה 5](Assignments/Week_05_APIs/README.md)

---

### שבוע 6 – R: יסודות
**כלים:** R, RStudio
**מה לומדים:**
- מה ההבדל בין Python ל-R ומתי כל אחד מתאים
- וקטורים, data frames, ה-tidyverse
- `dplyr` לעיבוד נתונים (כמו pandas)
- `ggplot2` לגרפים (יפה מ-matplotlib)
- קריאת נתוני Excel/CSV ב-R

📋 [משימה 6](Assignments/Week_06_R_Basics/README.md)

---

### שבוע 7 – R: אקונומטריקה מעשית
**כלים:** R, RStudio
**מה לומדים:**
- רגרסיה לינארית: `lm()` + פרשנות תוצאות
- Difference-in-Differences (DiD) – הערכת מדיניות
- ARIMA לחיזוי סדרות עתיות
- אחריות על תוצאות: בדיקת הנחות, בעיית ריבוי-בדיקות

📋 [משימה 7](Assignments/Week_07_Econometrics_R/README.md)

---

### שבוע 8 – ויזואליזציה: סיפור עם נתונים
**כלים:** Python (matplotlib, plotly), R (ggplot2)
**מה לומדים:**
- עקרונות ויזואליזציה: מה עובד ומה לא
- גרפים אינטראקטיביים עם Plotly
- אנימציות (אינפלציה לאורך זמן)
- הכנת גרף לפרסום/פרזנטציה

📋 [משימה 8](Assignments/Week_08_Visualization/README.md)

---

### שבוע 9 – Power BI / Tableau: דשבורדים
**כלים:** Power BI Desktop (Windows) / Tableau Public
**מה לומדים:**
- ייבוא נתונים מ-Excel ו-CSV
- בניית דשבורד מאקרו-כלכלי חי
- חיבור ל-API (Power BI + Python script)
- שיתוף דוחות עם קובעי מדיניות

📋 [משימה 9](Assignments/Week_09_BI_Tools/README.md)

---

### שבוע 10 – DSGE: מודלים מאקרו-כלכליים דינמיים
**כלים:** R (gEcon / bvartools), Python (pydsge)
**מה לומדים:**
- מה זה DSGE ולמה הוא מרכזי בבנקים מרכזיים
- RBC כמודל בסיסי – ניתוח עסקות המחזור הכלכלי
- כיול מודל על נתוני ישראל
- Impulse Response Functions: מה קורה לכלכלה אחרי הלם?

📋 [משימה 10](Assignments/Week_10_DSGE/README.md)

---

## מקורות נתונים מרכזיים

| מקור | כיסוי | API? | מדריך |
|---|---|---|---|
| בנק ישראל | ריבית, שע"ח, אינפלציה, מאזן תשלומים | ✅ SDMX | [Cookbook](Cookbook/boi_api.md) |
| הלמ"ס | אוכלוסייה, תעסוקה, שכר, מחירי דיור | ⚠️ חלקי | [Cookbook](Cookbook/cbs_api.md) |
| רשות המסים | הכנסות המדינה, נתוני עובדים | ⚠️ Excel | - |
| הבנק העולמי | תמ"ג, סחר, חוב, 200+ מדינות | ✅ wbgapi | [Cookbook](Cookbook/worldbank_api.md) |
| OECD | השוואה ל-38 מדינות OECD | ✅ SDMX | [Cookbook](Cookbook/oecd_api.md) |
| IMF WEO | תחזיות עולמיות | ✅ | - |
| FRED (ארה"ב) | סדרות מאקרו אמריקאיות | ✅ | - |

---

## תיק העבודות שלך

בסוף המסלול, התיקייה `Members/YourName/` תהיה **Portfolio** אמיתי:
- קוד Python ו-R שכתבת
- Notebooks עם ניתוחים על נתונים ישראליים
- דשבורד Power BI / Tableau
- מודל DSGE מוריץ על נתוני ישראל

**זה מה שמראים בראיון עבודה.**

---

*עודכן לאחרונה: 2025*
