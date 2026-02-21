# EconLab PPE – מכלכלה תיאורטית לכלכלה מעשית

> **המטרה:** לקחת סטודנטים לכלכלה שיודעים מודל סולו וסטטיסטיקה על הנייר —
> ולהפוך אותם לכלכלנים שמריצים קוד, מנתחים נתונים אמיתיים, ומדברים את השפה של שוק העבודה.

---

## למי זה מיועד?

סטודנטים לתואר ראשון בכלכלה (PPE / כלכלה / כלכלה וחשבונאות) שיוצאים עם:
- ✅ הבנה תיאורטית: מאקרו, מיקרו, אקונומטריקה
- ❌ חסרים: כלים מעשיים לעבוד עם נתונים ולקבל החלטות מבוססות-נתונים

**אחרי המסלול הזה תצאו עם:**

| כלי | מה תעשו איתו |
|---|---|
| **Excel** | ניתוח ראשוני, Pivot Tables, Power Query, NPV/IRR, Dashboard |
| **SQL** | שאילתות, JOINs, Window Functions, Python+SQL |
| **Python** | Pandas, Time Series, matplotlib, APIs |
| **R** | אקונומטריקה, DiD, ARIMA, VAR, ggplot2 |
| **Power BI / Tableau** | דשבורדים ויזואליים לקובעי מדיניות |
| **DSGE** | RBC, New Keynesian, Bayesian Estimation, IRFs |

---

## איך הלמידה עובדת?

המסלול מבוסס על **משימות שבועיות + קבוצת WhatsApp** פעילה.

**עקרון מרכזי:** כל כלי מקבל **2-3 שבועות** – מרמה מאפס מוחלט ועד רמה מקצועית.
לא מדלגים, לא מזרזים. כל שבוע: הסבר מלא → משימה מעשית → העלאה לתיקייה האישית ב-`Members/`

**~24 שבועות** לסיים את כל המסלול ולצאת עם Portfolio מקצועי.

> ראה את [מסלול הלמידה המלא](Curriculum.md) ואת [תיקיית המשימות](Assignments/).

---

## מבנה המאגר

```
econlabppe/
├── README.md               ← אתה כאן
├── Curriculum.md           ← מסלול למידה מלא (24 שבועות)
│
├── Assignments/            ← המשימות השבועיות (2-3 שבועות לכל כלי)
│   ├── Week_01_Setup/            ← מודול 1: הכנת סביבה
│   ├── Week_02_Excel_Basics/     ← מודול 2: Excel מאפס
│   ├── Week_03_Excel_Intermediate/ ← Excel בינוני
│   ├── Week_04_Excel_Advanced/   ← Excel מתקדם + Dashboard
│   ├── Week_05_SQL_Basics/       ← מודול 3: SQL מאפס
│   ├── Week_06_SQL_Intermediate/ ← SQL בינוני (JOINs, GROUP BY)
│   ├── Week_07_SQL_Advanced/     ← SQL מתקדם + Python+SQL
│   ├── Week_08_Python_Basics/    ← מודול 4: Python מאפס
│   ├── Week_09_Pandas_Basics/    ← Pandas בסיסי
│   ├── Week_10_Pandas_Advanced/  ← Pandas מתקדם + Time Series
│   ├── Week_11_APIs_Israel/      ← מודול 5: APIs ישראליים
│   ├── Week_12_APIs_International/ ← APIs בין-לאומיים
│   ├── Week_13_R_Basics/         ← מודול 6: R יסודות
│   ├── Week_14_R_Econometrics/   ← R אקונומטריקה
│   ├── Week_15_R_Time_Series/    ← R Time Series
│   ├── Week_16_Matplotlib/       ← מודול 7: ויזואליזציה
│   ├── Week_17_Plotly/           ← Plotly אינטראקטיבי
│   ├── Week_18_ggplot2_RMarkdown/ ← ggplot2 + R Markdown
│   ├── Week_19_PowerBI_Basics/   ← מודול 8: Power BI
│   ├── Week_20_PowerBI_Advanced/ ← Power BI מתקדם
│   ├── Week_21_Tableau/          ← Tableau Public
│   ├── Week_22_DSGE_Intro/       ← מודול 9: DSGE מבוא
│   ├── Week_23_DSGE_Estimation/  ← DSGE אמידה
│   └── Week_24_DSGE_Capstone/    ← פרויקט מסכם
│
├── Members/                ← תיקי העבודות האישיים של חברי המעבדה
│   ├── _template/          ← התחל מכאן! העתק לתיקייה בשמך
│   └── YourName/
│
├── Cookbook/               ← מדריכים וקטעי קוד מוכנים לשימוש
│   ├── boi_api.md          ← API בנק ישראל
│   ├── cbs_api.md          ← API הלמ"ס
│   ├── worldbank_api.md    ← API הבנק העולמי
│   ├── oecd_api.md         ← API ה-OECD
│   ├── pandas_guide.md     ← Pandas לכלכלנים
│   ├── sql_basics.md       ← SQL מהיסוד
│   └── r_econometrics.md   ← R לאקונומטריקה
│
├── Notebooks/              ← ניתוחים ודוחות לפי שלבי עבודה
│   ├── 00_Setup/
│   ├── 10_Data_Fetch/
│   ├── 20_Cleaning/
│   ├── 30_Analysis/
│   └── 40_Reports/
│
├── Projects/               ← פרויקטי מחקר ארוכי-טווח
│   ├── Housing_Market/
│   ├── Inflation_Tracker/
│   └── Labor_Market/
│
└── Data/                   ← מטה-דאטה בלבד (הנתונים ב-Google Drive)
```

---

## איפה שומרים נתונים?

**GitHub (כאן):** קוד, notebooks, סקריפטים, קבצי מטה-דאטה קטנים
**Google Drive:** קבצי CSV/Excel גדולים, מאמרים, מצגות

> 📁 [תיקיית Google Drive המשותפת – יש להחליף קישור](https://drive.google.com/placeholder)

### גבולות GitHub לקבצים:
- קבצים עד ~50MB – מותר (עם אזהרה)
- קבצים מעל 100MB – חסום אוטומטית
- **מסקנה:** קבצי נתונים קטנים (< 5MB) – אפשר לשים ב-`Data/`. קבצים גדולים – Google Drive בלבד.

---

## התחלה מהירה

### שלב 1 – שכפל את המאגר
```bash
git clone https://github.com/YourOrg/econlabppe.git
cd econlabppe
```

### שלב 2 – צור תיקייה אישית
```bash
cp -r Members/_template Members/YourFirstName_YourLastName
```
ערוך את `Members/YourName/README.md` ואת `Members/YourName/intro.py` עם הפרטים שלך.

### שלב 3 – צור סביבה וירטואלית בפייתון
```bash
python -m venv .venv
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### שלב 4 – עקוב אחרי משימה 1
ראה: [`Assignments/Week_01_Setup/README.md`](Assignments/Week_01_Setup/README.md)

---

## כלים להתקין (פעם ראשונה)

| כלי | קישור הורדה | הערות |
|---|---|---|
| Python 3.11+ | [python.org](https://www.python.org/downloads/) | סמן "Add to PATH" |
| R | [cran.r-project.org](https://cran.r-project.org/) | |
| RStudio | [posit.co/rstudio](https://posit.co/download/rstudio-desktop/) | IDE ל-R |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com/) | IDE ל-Python |
| Git | [git-scm.com](https://git-scm.com/) | |
| DBeaver | [dbeaver.io](https://dbeaver.io/) | לניהול SQL |
| Power BI Desktop | [powerbi.microsoft.com](https://powerbi.microsoft.com/desktop/) | Windows בלבד |

---

## כללי תרומה

ראה: [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

*"כלכלן שלא יודע לעבוד עם נתונים הוא כמו רופא שלא יודע לקרוא בדיקות."*
