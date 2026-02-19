# Cookbook: הלמ"ס (CBS) – הלשכה המרכזית לסטטיסטיקה

> הלמ"ס (Central Bureau of Statistics) הוא מקור הנתונים הרשמי של ישראל.
> **חשוב:** ללמ"ס אין API כוללני – נתונים רבים זמינים רק כ-Excel להורדה.

---

## שלוש דרכי גישה

| שיטה | מתי להשתמש | קושי |
|---|---|---|
| הורדת Excel ישירות | נתונים סטטיים | קל |
| CBS API (חלקי) | מאגרי נתונים מסוימים | בינוני |
| Web scraping מוגבל | כשאין אפשרות אחרת | מתקדם |

---

## דרך 1: הורדת Excel + Pandas

```python
"""
cbs_excel.py – קריאת קבצי Excel מהלמ"ס
pip install pandas openpyxl requests
"""

import pandas as pd
import requests
from pathlib import Path


def download_cbs_file(url: str, filename: str) -> Path:
    """הורד קובץ מהלמ\"ס ושמור מקומית."""
    resp = requests.get(url, timeout=60,
                        headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    path = Path(filename)
    path.write_bytes(resp.content)
    print(f"הורד: {path} ({len(resp.content) / 1024:.0f} KB)")
    return path


def read_cbs_excel(filepath: str, sheet_name: int = 0,
                   skip_rows: int = 4) -> pd.DataFrame:
    """
    קרא Excel מהלמ\"ס.

    הלמ\"ס בד\"כ מוסיף 4-6 שורות כותרת לפני הנתונים.
    ייתכן שתצטרך לשנות skip_rows לפי הקובץ.
    """
    df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        skiprows=skip_rows,
        engine="openpyxl"
    )
    # נקה עמודות ריקות
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    return df


# ==========================================
# דוגמה: נתוני אוכלוסייה
# ==========================================

# הורד מהלמ"ס (בדוק קישור עדכני באתר cbs.gov.il)
# url = "https://www.cbs.gov.il/he/publications/doclib/2024/population/pop2024.xlsx"
# path = download_cbs_file(url, "cbs_population.xlsx")

# לתרגול: צור DataFrame ידנית
population_data = {
    "year": range(2015, 2025),
    "total_population_thousands": [8380, 8547, 8714, 8883, 9054, 9136, 9217,
                                    9449, 9570, 9700],
    "jewish_pct": [74.9, 74.8, 74.7, 74.6, 74.5, 73.9, 73.9, 73.9, 73.9, 74.0],
}
df_pop = pd.DataFrame(population_data)
print(df_pop)

# אחוז גידול שנתי
df_pop["growth_rate"] = df_pop["total_population_thousands"].pct_change() * 100
print("\nאחוז גידול שנתי:")
print(df_pop[["year", "growth_rate"]].dropna())
```

---

## דרך 2: CBS API (databank)

```python
"""
cbs_api.py – גישה לנתונים דרך CBS databank API
"""

import requests
import pandas as pd

CBS_API_BASE = "https://api.cbs.gov.il/index/api/1.0"


def get_cbs_subjects(lang: str = "he") -> list:
    """קבל רשימת נושאים זמינים מה-CBS."""
    url = f"{CBS_API_BASE}/subject?lang={lang}&limit=50"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_cbs_series(keyword: str, lang: str = "he") -> list:
    """חפש סדרות לפי מילת מפתח."""
    url = f"{CBS_API_BASE}/series/search?keyword={keyword}&lang={lang}&limit=20"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ==========================================
# שימוש
# ==========================================
if __name__ == "__main__":
    # חפש סדרות על אבטלה
    results = search_cbs_series("אבטלה")
    for r in results[:5]:
        print(r.get("id"), "-", r.get("name", {}).get("he", ""))
```

---

## דרך 3: נתוני תעסוקה ושכר (מקורות מומלצים)

### מה להוריד ידנית מהאתר:
| נושא | נתיב באתר | פורמט |
|---|---|---|
| אוכלוסייה | Statistical Abstract → Population | Excel |
| תעסוקה ואבטלה | Statistical Abstract → Labour Force | Excel |
| שכר ממוצע | Statistical Abstract → Wages | Excel |
| מחירי דיור | דוח מחירי דיור רבעוני | Excel |
| יוקר מחיה (CPI) | מחשבון יוקר מחיה | Excel / JSON |

> אתר: [cbs.gov.il/he/publications](https://www.cbs.gov.il/he/publications)

---

## טיפ: CPI ישראל דרך בנק ישראל

לעיתים קרובות **קל יותר** לשאול את נתוני המחירים דרך API בנק ישראל:
```python
# מ-boi_api.md
df_cpi = fetch_boi_series("CPI_1Y", start_year=2010)
```

---

## עיבוד קובץ Excel טיפוסי מהלמ"ס

```python
import pandas as pd

# קרא קובץ Excel (שנשמר ב-Google Drive – לא ב-Git!)
df = pd.read_excel("cbs_wages.xlsx", skiprows=5, engine="openpyxl")

# הלמ"ס משתמש בעברית בכותרות – נרמל:
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace('"', "")
    .str.replace("'", "")
)

# הסר שורות ריקות
df = df.dropna(subset=[df.columns[0]])

# המר מספרים (לפעמים הם strings עם פסיקים)
for col in df.select_dtypes(include="object").columns:
    df[col] = pd.to_numeric(df[col].str.replace(",", ""), errors="ignore")

print(df.head())
print(df.dtypes)
```

---

## כלי עזר: databank.cbs.gov.il

ממשק ויזואלי לבניית שאילתות:
**[databank.cbs.gov.il](https://databank.cbs.gov.il)**
אפשר לסנן, לבנות טבלה ולייצא CSV/Excel.

---

*עודכן: 2025 | מקור: [cbs.gov.il](https://www.cbs.gov.il)*
