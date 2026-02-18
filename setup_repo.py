"""
setup_repo.py
-------------
EconLab PPE – Repository Initializer
מאתחל את מבנה התיקיות והקבצים של המאגר.
הרץ מתוך שורש המאגר: python setup_repo.py
"""

import os

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def write_file(path: str, content: str) -> None:
    """יוצר קובץ עם תוכן בקידוד UTF-8 (יוצר תיקיות ביניים במידת הצורך)."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  [+] {path}")


def make_dir(path: str) -> None:
    """יוצר תיקייה (כולל הורים) אם לא קיימת."""
    os.makedirs(path, exist_ok=True)
    print(f"  [d] {path}/")


# ---------------------------------------------------------------------------
# Root files
# ---------------------------------------------------------------------------

ROOT_README = """\
# EconLab PPE – מעבדת כלכלה: תיאוריה לפרקטיקה

## משימת המעבדה

**EconLab PPE** היא מעבדת מחקר של סטודנטים לכלכלה שמטרתה לגשר בין הכלכלה האקדמית
(תיאוריה, מדלנות) לבין כלי מדעי הנתונים המעשיים (Python, SQL, מודלים מאקרו-כלכליים).

> מאמינים שכלכלן טוב בשנת 2025 חייב לדעת לא רק *מה* קורה בכלכלה, אלא גם *כיצד* לכמת,
> לנקות ולמדל נתונים בעצמו.

---

## מבנה המאגר

| תיקייה | תפקיד |
|---|---|
| `Cookbook/` | קטעי קוד ומדריכים מהירים (API, Pandas, SQL) |
| `Notebooks/` | שלבי העבודה – ממשיכת נתונים ועד דוחות |
| `Projects/` | פרויקטי מחקר ארוכי-טווח |
| `Members/` | מרחבי עבודה אישיים של חברי המעבדה |
| `Data/` | מטה-דאטה בלבד – הנתונים עצמם ב-Google Drive |

---

## נתוני גלם – Google Drive

הנתונים הגולמיים (קבצי CSV / Excel) **אינם** מועלים ל-Git.
ניתן למצוא אותם בתיקיית Google Drive המשותפת:

> 📁 **[קישור לתיקיית Google Drive – יש להחליף קישור זה](https://drive.google.com/placeholder)**

---

## תחילת עבודה

```bash
# שכפל את המאגר
git clone <repo-url>
cd econlabppe

# צור סביבה וירטואלית והתקן תלויות
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt  # (כשיוצר)
```

---

## כללי תרומה

ראה את הקובץ [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

*נוצר אוטומטית על-ידי `setup_repo.py`*
"""

CONTRIBUTING = """\
# הנחיות תרומה – EconLab PPE

## כללי זהב

1. **אל תעלה קבצי נתונים ל-Git.**
   קבצי `*.csv`, `*.xlsx`, `*.parquet` וכדומה מוחרגים ב-`.gitignore`.
   יש להעלות נתונים **אך ורק** לתיקיית Google Drive המשותפת.

2. **שמות קבצים ותיקיות – באנגלית בלבד (Snake Case).**
   דוגמה נכונה: `housing_price_index.py`, `Projects/Housing_Market/`.
   דוגמה שגויה: `ניתוח דיור.ipynb`.

3. **תוכן קבצי Markdown – בעברית.**
   הסברים, תיעוד ותיאורי פרויקטים נכתבים בעברית לנוחות הקריאה.

4. **סביבה וירטואלית – לא ב-Git.**
   יש להוסיף `.venv/`, `env/` ל-`.gitignore` ולא להעלות אותן.

5. **קבצי `.env` – לעולם לא ב-Git.**
   מפתחות API, סיסמאות וכתובות שרת שמורים אך ורק בקובץ `.env` מקומי.

---

## תהליך עבודה (Git Flow מומלץ)

```
main          ← ענף יציב בלבד
  └─ dev      ← אינטגרציה
       └─ feature/<your-name>/<topic>   ← עבודה שוטפת
```

1. צור ענף חדש מ-`dev`: `git checkout -b feature/YourName/topic`
2. עבוד, בצע Commit עם הודעות ברורות באנגלית.
3. פתח Pull Request ל-`dev` וציין מה עשית ולמה.
4. לאחר אישור – מיזוג (Merge).

---

## סגנון קוד

- Python: [PEP 8](https://pep8.org/) + Black formatter.
- SQL: מילים שמורות באותיות גדולות (`SELECT`, `FROM`, `WHERE`).
- Notebooks: אפס פלטים לפני Commit (`Kernel → Restart & Clear Output`).

---

*עדכון אחרון: נוצר על-ידי `setup_repo.py`*
"""

GITIGNORE = """\
# =============================================================
# EconLab PPE – .gitignore
# =============================================================

# --- סביבות Python ---
.venv/
env/
venv/
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
build/
dist/
*.egg-info/
.eggs/

# --- Jupyter ---
.ipynb_checkpoints/

# --- נתונים (אל תעלה ל-Git!) ---
*.csv
*.xlsx
*.xls
*.parquet
*.feather
*.hdf
*.h5
*.pickle
*.pkl
data/raw/

# --- סביבות וסודות ---
.env
.env.*
*.env
secrets.yaml

# --- מערכת הפעלה ---
.DS_Store
Thumbs.db
desktop.ini

# --- IDE ---
.idea/
.vscode/
*.suo
*.user
*.swp
*~

# --- תיעוד מיוצר ---
docs/_build/
site/
"""

# ---------------------------------------------------------------------------
# Cookbook
# ---------------------------------------------------------------------------

COOKBOOK_FILES = {
    "Cookbook/boi_api.md": """\
# מדריך: API בנק ישראל (BOI)

## מה כאן?
מדריך זה יכיל קטעי קוד מוכנים לשימוש לשאילתות מ-API הפתוח של בנק ישראל.

## נושאים מתוכננים

- אחזור סדרות עתיות: ריבית, שע"ח, מדד המחירים לצרכן
- פרמטרים נפוצים (`series_code`, `start_period`, `end_period`)
- עיבוד תגובת JSON לתוך DataFrame של Pandas
- שמירת נתונים ל-Google Drive (ולא ל-Git!)

## דוגמה (skeleton)

```python
import requests
import pandas as pd

BASE_URL = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/"

def fetch_series(series_code: str, start: str, end: str) -> pd.DataFrame:
    \"\"\"אחזר סדרה עתית מ-API בנק ישראל.\"\"\"
    # TODO: implement
    raise NotImplementedError
```

---
*יש להשלים את הפונקציה ולהוסיף דוגמאות נוספות.*
""",
    "Cookbook/cbs_api.md": """\
# מדריך: API הלשכה המרכזית לסטטיסטיקה (CBS)

## מה כאן?
מדריך זה יכיל קטעי קוד לגישה לנתוני הלמ"ס (הלשכה המרכזית לסטטיסטיקה).

## נושאים מתוכננים

- גישה לנתוני אוכלוסייה, תעסוקה ושכר מ-databank.cbs.gov.il
- הורדת קבצי Excel מהאתר ופרסורם עם Pandas
- שימוש ב-`requests` + `BeautifulSoup` לגרידה מוגבלת (כאשר אין API ייעודי)
- מיפוי קודי NUTS לאזורים גיאוגרפיים

## כלים עיקריים

| כלי | שימוש |
|---|---|
| `requests` | הורדת קבצים ושאילתות HTTP |
| `pandas` | קריאה וניתוח טבלאות |
| `openpyxl` | קריאת קבצי Excel |

---
*יש להשלים דוגמאות קוד אמיתיות.*
""",
    "Cookbook/pandas_guide.md": """\
# מדריך Pandas – פעולות יומיומיות במעבדה

## מה כאן?
אוסף קטעי קוד ל-Pandas שחוזרים שוב ושוב בניתוחי נתונים כלכליים.

## נושאים מתוכננים

### טעינה וסינון
- קריאת CSV / Excel עם encoding נכון
- סינון לפי תאריך, אזור, ענף כלכלי
- שינוי שמות עמודות ל-snake_case

### עיבוד סדרות עתיות
- המרה ל-`DatetimeIndex`
- Resampling (חודשי / רבעוני / שנתי)
- Rolling Average, YoY Change

### מיזוג מקורות נתונים
- `pd.merge` לפי מפתח משותף
- `pd.concat` לאיחוד טבלאות מרובות

### ייצוא
- שמירה ל-Parquet (לא CSV!) לחיסכון במקום
- ייצוא לגוגל דרייב עם `google-auth`

---
*יש להוסיף קטעי קוד לכל נושא.*
""",
    "Cookbook/sql_basics.md": """\
# יסודות SQL – למשתמש Python

## מה כאן?
מדריך SQL בסיסי-מתקדם המותאם לכלכלנים העובדים עם בסיסי נתונים (SQLite, PostgreSQL).

## נושאים מתוכננים

### שאילתות בסיסיות
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- פילטור לפי טווח תאריכים
- `GROUP BY` + פונקציות אגרגציה (`SUM`, `AVG`, `COUNT`)

### שאילתות מתקדמות
- `JOIN` בין טבלאות (INNER, LEFT, FULL OUTER)
- Subqueries ו-CTEs (`WITH ... AS`)
- Window Functions: `ROW_NUMBER()`, `LAG()`, `LEAD()`

### Python + SQL
- שימוש ב-`sqlite3` לניהול DB מקומי
- `pandas.read_sql_query()` לטעינת תוצאות ישירות ל-DataFrame
- SQLAlchemy לחיבור ל-PostgreSQL

---
*יש להוסיף תרגילים ופתרונות לכל סעיף.*
""",
}

# ---------------------------------------------------------------------------
# Notebooks
# ---------------------------------------------------------------------------

NOTEBOOK_FOLDERS = {
    "Notebooks/00_Setup": """\
# שלב 00 – הגדרת סביבה

## מטרה
תיקייה זו מכילה מחברות הגדרה ראשונית לפני כל פרויקט.

## תכולה אופיינית

- `environment_check.ipynb` – בדיקת גרסאות Python וחבילות
- `google_drive_auth.ipynb` – הגדרת הרשאות לגישה ל-Google Drive
- `api_keys_test.ipynb` – אימות מפתחות API (BOI, CBS)

## הנחיות

1. אל תשמור מפתחות API בתוך ה-Notebook – השתמש ב-`.env`.
2. נקה פלטים לפני Commit.
""",
    "Notebooks/10_Data_Fetch": """\
# שלב 10 – אחזור נתונים

## מטרה
תיקייה זו מכילה מחברות לאחזור נתונים ממקורות חיצוניים.

## מקורות נתונים נפוצים

| מקור | API / URL |
|---|---|
| בנק ישראל | edge.boi.gov.il |
| הלמ"ס | databank.cbs.gov.il |
| World Bank | api.worldbank.org |
| FRED (Fed) | fred.stlouisfed.org |

## הנחיות

- שמור נתונים גולמיים ל-Google Drive (`Data/Raw/`), לא ל-Git.
- תעד את תאריך האחזור בשם הקובץ: `cpi_raw_2024-01.parquet`.
""",
    "Notebooks/20_Cleaning": """\
# שלב 20 – ניקוי ועיצוב נתונים

## מטרה
תיקייה זו מכילה מחברות לניקוי, תיקון ועיצוב (wrangling) של הנתונים הגולמיים.

## פעולות נפוצות

- הסרת כפילויות ושגיאות
- המרת טיפוסי נתונים (תאריכים, מספרים)
- טיפול בערכים חסרים (`NaN`)
- אחידות שמות עמודות (snake_case)
- מיזוג קבצים ממקורות שונים

## קונבנציה לשמות קבצים

`<topic>_clean_<version>.parquet` – דוגמה: `cpi_clean_v1.parquet`
""",
    "Notebooks/30_Analysis": """\
# שלב 30 – ניתוח נתונים

## מטרה
תיקייה זו מכילה מחברות לניתוח סטטיסטי ומודלים כלכליים.

## סוגי ניתוח נפוצים

- סטטיסטיקה תיאורית (ממוצע, סטיית תקן, מדיאנה)
- ניתוח מגמות וסדרות עתיות
- רגרסיה ליניארית ומודלים חזויים
- מתאמים בין משתנים כלכליים

## כלים

| כלי | שימוש |
|---|---|
| `statsmodels` | רגרסיה, ARIMA |
| `scikit-learn` | Machine Learning |
| `matplotlib` / `seaborn` | ויזואליזציה |
| `plotly` | גרפים אינטראקטיביים |
""",
    "Notebooks/40_Reports": """\
# שלב 40 – דוחות ופרסומים

## מטרה
תיקייה זו מכילה מחברות להפקת דוחות סופיים, גרפים לפרסום וסיכומים.

## פורמטים נפוצים

- `*.ipynb` עם ויזואליזציות מלאות
- ייצוא ל-PDF / HTML באמצעות `nbconvert`
- מצגות עם `RISE` או `reveal.js`

## הנחיות

- וודא שהמחברת ניתנת להרצה מחדש (`Restart & Run All`) ללא שגיאות.
- אל תקשה-קוד (hardcode) נתיבים מקומיים – השתמש ב-`pathlib.Path`.
- הוסף תא Markdown עם מסקנות ברורות בראש המחברת.
""",
}

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

PROJECT_FOLDERS = {
    "Projects/Housing_Market": """\
# פרויקט: שוק הדיור בישראל

## שאלת המחקר
כיצד ריבית בנק ישראל, היצע הדירות ורמות השכר משפיעים על מחירי הדיור
במרכז הארץ לעומת הפריפריה?

## מקורות נתונים

| מקור | נתון |
|---|---|
| בנק ישראל | ריבית, משכנתאות |
| הלמ"ס | מחירי דירות, התחלות בנייה |
| רשות המיסים | נתוני עסקאות |

## מצב הפרויקט

- [ ] אחזור נתונים היסטוריים (2010–היום)
- [ ] ניקוי ואיחוד מקורות
- [ ] מודל רגרסיה ראשוני
- [ ] ויזואליזציה אינטראקטיבית
- [ ] סיכום ומסקנות

## אחראי פרויקט

*יש לעדכן שם*
""",
    "Projects/Inflation_Tracker": """\
# פרויקט: עוקב אינפלציה

## שאלת המחקר
מהם הגורמים העיקריים לאינפלציה בישראל בשנים האחרונות?
האם ניתן לבנות מודל חיזוי לטווח קצר של מדד המחירים לצרכן (CPI)?

## מקורות נתונים

| מקור | נתון |
|---|---|
| הלמ"ס | CPI חודשי לפי קטגוריות |
| בנק ישראל | ציפיות אינפלציה, ריבית |
| FRED | מחירי אנרגיה עולמיים |

## מצב הפרויקט

- [ ] הגדרת סדרות עתיות רלוונטיות
- [ ] ניתוח הפירוק לרכיבים (אנרגיה, מזון, ליבה)
- [ ] מודל ARIMA / VAR
- [ ] לוח מחוונים (Dashboard) חי
- [ ] דוח אקדמי

## אחראי פרויקט

*יש לעדכן שם*
""",
    "Projects/Labor_Market": """\
# פרויקט: שוק העבודה

## שאלת המחקר
כיצד השתנה שוק העבודה הישראלי לאחר אירועי אוקטובר 2023?
מה הקשר בין שיעור האבטלה, השכר הממוצע ורמת ההשתתפות?

## מקורות נתונים

| מקור | נתון |
|---|---|
| הלמ"ס | שיעור אבטלה, שכר ממוצע |
| שירות התעסוקה | דורשי עבודה |
| בנק ישראל | סקר שכר |

## מצב הפרויקט

- [ ] מיפוי מקורות נתונים
- [ ] סדרות עתיות שנתיות / רבעוניות
- [ ] השוואה לשוק עבודה גלובלי (OECD)
- [ ] מודל ניבוי אבטלה
- [ ] מאמר / Poster

## אחראי פרויקט

*יש לעדכן שם*
""",
}

# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------

MEMBERS_README = """\
# Members – מרחבי עבודה אישיים

## מה התיקייה הזו?

כאן כל חבר מעבדה יוצר תיקייה אישית לניסויים, טיוטות ומחקרים.
התיקייה האישית היא מרחב חופשי – אין דרישות עיצוב מחמירות.

## כיצד ליצור תיקייה אישית?

```bash
mkdir Members/YourName
cd Members/YourName
# צור קובץ README אישי:
echo "# אזור עבודה של YourName" > README.md
git add .
git commit -m "feat: add YourName workspace"
```

## כללים

1. שם התיקייה – **באנגלית** (למשל `Members/Noa_Cohen`).
2. אל תעלה נתונים (CSV / Excel) גם כאן.
3. ניתן ליצור Notebooks, סקריפטים ותיעוד חופשי.

---
*חברי המעבדה הנוכחיים – יש לעדכן רשימה זו:*

| שם | תיקייה |
|---|---|
| (ריק) | `Members/YourName` |
"""

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

DATA_README = """\
# Data – מטה-דאטה בלבד

## חשוב מאוד

תיקייה זו **אינה** מכילה קבצי נתונים ממשיים.
כל הנתונים הגולמיים והמעובדים שמורים ב-**Google Drive** המשותף.

> 📁 **[קישור לתיקיית Google Drive – יש להחליף קישור זה](https://drive.google.com/placeholder)**

---

## מבנה תיקיית Google Drive (מוסכם)

```
Google Drive/
└── EconLab_Data/
    ├── Raw/              ← נתונים גולמיים כפי שהורדו
    │   ├── BOI/
    │   ├── CBS/
    │   └── External/
    ├── Processed/        ← נתונים לאחר ניקוי (Parquet)
    └── Final/            ← נתונים לניתוח סופי
```

---

## מה מותר לשים ב-Git בתיקייה זו?

- קבצי מטה-דאטה קטנים בפורמט `*.json` או `*.yaml` (schema, data dictionary)
- תיאורי מקורות נתונים בקבצי Markdown
- קובצי `*.sql` להגדרת סכמת בסיס נתונים

## מה **אסור**?

- `*.csv`, `*.xlsx`, `*.parquet` – **בשום פנים ואופן**
- קבצים מעל 1MB בכלל

---
*שינוי מוסכמות אלה דורש אישור מנהל המעבדה.*
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n========================================")
    print("  EconLab PPE – Repository Initializer")
    print("========================================\n")

    # --- Root files ---
    print("[1/6] Root files...")
    write_file("README.md", ROOT_README)
    write_file("CONTRIBUTING.md", CONTRIBUTING)
    write_file(".gitignore", GITIGNORE)

    # --- Cookbook ---
    print("\n[2/6] Cookbook/...")
    make_dir("Cookbook")
    for path, content in COOKBOOK_FILES.items():
        write_file(path, content)

    # --- Notebooks ---
    print("\n[3/6] Notebooks/...")
    for folder, readme_content in NOTEBOOK_FOLDERS.items():
        make_dir(folder)
        write_file(os.path.join(folder, "README.md"), readme_content)

    # --- Projects ---
    print("\n[4/6] Projects/...")
    for folder, readme_content in PROJECT_FOLDERS.items():
        make_dir(folder)
        write_file(os.path.join(folder, "README.md"), readme_content)

    # --- Members ---
    print("\n[5/6] Members/...")
    make_dir("Members")
    write_file("Members/README.md", MEMBERS_README)

    # --- Data ---
    print("\n[6/6] Data/...")
    make_dir("Data")
    write_file("Data/README.md", DATA_README)

    print("\n========================================")
    print("  הסיום! מבנה המאגר נוצר בהצלחה.")
    print("========================================\n")


if __name__ == "__main__":
    main()
