# משימה 5 – APIs: גישה ישירה לנתוני כלכלה

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

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
## הכנה

```bash
pip install requests pandas wbgapi python-dotenv
```

---

## חלק א – API בנק ישראל

בנק ישראל מפרסם את כל הנתונים שלו דרך API פתוח (ללא צורך ב-API Key).

```python
import requests
import pandas as pd

def fetch_boi_series(series_code: str, start_year: int = 2010) -> pd.DataFrame:
    """
    שאל סדרה עתית מ-API בנק ישראל.

    קודים שימושיים:
    - RER_USD_ILS  : שע"ח דולר/שקל
    - CPI_1Y       : מדד מחירים לצרכן (שנתי)
    - INT_RATE     : ריבית בנק ישראל
    """
    url = (
        "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/"
        f"BOI.STATISTICS/{series_code}/?"
        f"startperiod={start_year}&format=csv"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))
    df.columns = df.columns.str.lower()
    return df

# דוגמה: שע"ח דולר/שקל
df_fx = fetch_boi_series("RER_USD_ILS", start_year=2015)
print(df_fx.head(10))
```

ראה מדריך מלא: [`Cookbook/boi_api.md`](../../Cookbook/boi_api.md)

---

## חלק ב – API הבנק העולמי

```python
import wbgapi as wb

# מה אינדיקטורים זמינים?
# wb.series.search("GDP growth")

# תמ"ג ישראל בנפח קבוע (% שינוי שנתי)
df_gdp = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    economy="ISR",
    time=range(2000, 2025)
)
df_gdp.index.name = "year"
df_gdp.columns = ["gdp_growth_pct"]
print(df_gdp.tail(10))

# השוואה בין-מדינתית: ישראל, ארה"ב, גרמניה, טורקיה
countries = ["ISR", "USA", "DEU", "TUR"]
df_compare = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=countries,
    time=range(2010, 2025)
)
print(df_compare)
```

ראה מדריך מלא: [`Cookbook/worldbank_api.md`](../../Cookbook/worldbank_api.md)

---

## חלק ג – API ה-OECD

```python
import requests
import pandas as pd

def fetch_oecd(dataset: str, subject: str, country: str = "ISR",
               start: str = "2010", end: str = "2024") -> pd.DataFrame:
    """
    שאל נתונים מ-OECD Stats API (SDMX-JSON).

    דוגמאות:
    - dataset="MEI", subject="CPALTT01"  : CPI
    - dataset="MEI", subject="LRUNTTTT"  : אבטלה
    - dataset="SNA_TABLE1", subject="B1_GA" : GDP
    """
    url = (
        f"https://stats.oecd.org/SDMX-JSON/data/{dataset}/"
        f"{country}.{subject}.A/all?"
        f"startTime={start}&endTime={end}&contentType=csv"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))
    return df

# דוגמה: אינפלציה ישראל
df_cpi = fetch_oecd("MEI", "CPALTT01", country="ISR")
print(df_cpi.head())
```

ראה מדריך מלא: [`Cookbook/oecd_api.md`](../../Cookbook/oecd_api.md)

---

## חלק ד – ניהול מפתחות API (חשוב!)

חלק מה-APIs דורשים Token (מפתח גישה). **לעולם אל תשים אותו בקוד!**

### צור קובץ `.env` (לא מועלה ל-Git):
```
# .env
BOI_API_KEY=your_key_here
WORLD_BANK_KEY=your_key_here
```

### קרא אותו בפייתון:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BOI_API_KEY")
```

### ודא ש-`.env` ב-`.gitignore`:
```bash
# בדוק:
cat .gitignore | grep .env
# אמור לראות: .env
```

---

## המשימה שלך

צור Notebook `Members/YourName/Week_05/api_data_fetch.ipynb` עם:

### תרגיל 1 – נתוני בנק ישראל
- שאל את שע"ח הדולר/שקל לשנים 2015–2024
- הצג גרף קווי
- הוסף הערה: מתי הייתה נקודת השפל של השקל?

### תרגיל 2 – השוואה בין-מדינתית
- שאל מ-World Bank את **אחוז האבטלה** עבור: ישראל, ארה"ב, גרמניה, יוון
- לשנים 2010–2024
- הצג בגרף יחיד עם 4 קווים

### תרגיל 3 – שאלה כלכלית משלך
- בחר **אינדיקטור אחד** שמעניין אותך (ממי שתרצה)
- שאל את הנתונים בפייתון
- כתוב פסקה קצרה על מה שגילית

---

## הגשה

תיקייה: `Members/YourName/Week_05/`
- [ ] `api_data_fetch.ipynb`
- [ ] `.env.example` (קובץ דוגמה עם מפתחות ריקים – **ללא** ערכים אמיתיים!)

---

**השבוע הבא:** R – יסודות → [משימה 6](../Week_06_R_Basics/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_05_APIs/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

