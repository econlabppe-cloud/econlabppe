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
| **Excel** | ניתוח ראשוני, Pivot Tables, פונקציות פיננסיות |
| **SQL** | שאילתות על בסיסי נתונים, מיזוג מקורות |
| **Python** | Pandas, ניתוח סדרות עתיות, גרפים, API |
| **R** | אקונומטריקה, רגרסיות, DiD, Time Series |
| **Power BI / Tableau** | דשבורדים ויזואליים לקובעי מדיניות |
| **DSGE** | הרצת מודלים מאקרו-כלכליים דינמיים |

---

## איך הלמידה עובדת?

המסלול מבוסס על **משימות שבועיות + קבוצת WhatsApp** פעילה.

כל שבוע: הסבר קצר → משימה מעשית → העלאה לתיקייה האישית ב-`Members/`

> ראה את [מסלול הלמידה המלא](Curriculum.md) ואת [תיקיית המשימות](Assignments/).

---

## מבנה המאגר

```
econlabppe/
├── README.md               ← אתה כאן
├── Curriculum.md           ← מסלול למידה מלא (שבוע אחר שבוע)
│
├── Assignments/            ← המשימות השבועיות
│   ├── Week_01_Setup/      ← התקנת כלים + חיבור לגיטהאב (משימה ראשונה!)
│   ├── Week_02_Excel/
│   ├── Week_03_SQL_Intro/
│   ├── Week_04_Python_Pandas/
│   ├── Week_05_APIs/
│   ├── Week_06_R_Basics/
│   ├── Week_07_Econometrics_R/
│   ├── Week_08_Visualization/
│   ├── Week_09_BI_Tools/
│   └── Week_10_DSGE/
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
