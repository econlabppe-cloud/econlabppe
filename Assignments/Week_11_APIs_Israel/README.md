# שבוע 11 – APIs ישראליים: גישה לנתוני בנק ישראל והלמ"ס בזמן אמת

> **רמה:** בינוני – מניח שסיימת שבועות 8-10 (Python + Pandas)
> **מטרת השבוע:** להוריד נתונים כלכליים ישראליים אוטומטית ישירות לקוד שלך

---

## מה זה API ולמה זה משנה?

**בלי API:**
1. כנס לאתר בנק ישראל
2. חפש את הנתון הנכון
3. הורד Excel
4. פתח Excel
5. העתק ל-Python
6. חזור על הכל כל חודש

**עם API:**
```python
import requests
df = fetch_boi_data("RER_USD_ILS")  # שורה אחת!
```

נתונים מתעדכנים **אוטומטית** בכל פעם שמריצים.

---

## חלק א – יסודות: מה זה HTTP request?

```python
import requests

# GET request בסיסי
response = requests.get("https://example.com/api/data")

print(response.status_code)  # 200 = הצלחה, 404 = לא נמצא, 403 = אין הרשאה
print(response.headers)      # מידע על התגובה
print(response.text)         # התגובה כטקסט

# JSON (הפורמט הנפוץ)
data = response.json()       # המרה ל-Python dict/list
```

### Status codes חשובים

| קוד | משמעות |
|---|---|
| 200 | הצלחה |
| 400 | שגיאה בבקשה (Bad Request) |
| 401 | לא מורשה (דרוש API key) |
| 403 | אסור (Forbidden) |
| 404 | לא נמצא |
| 429 | יותר מדי בקשות (Rate Limit) |
| 500 | שגיאה בשרת |

---

## חלק ב – בנק ישראל (BOI): SDMX API

### מה זה SDMX?

SDMX (Statistical Data and Metadata eXchange) = פרוטוקול בין-לאומי לנתונים סטטיסטיים. הבנק העולמי, ה-OECD, ובנק ישראל משתמשים בו.

**אין צורך ב-API Key!** נתוני בנק ישראל פתוחים לכולם.

### Endpoint בסיסי

```
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/SERIES_NAME/?startperiod=YYYY-MM&endperiod=YYYY-MM&format=sdmx-json
```

### סדרות נתונים עיקריות

| קוד | תיאור | תדירות |
|---|---|---|
| `RER_USD_ILS` | שער חליפין דולר-שקל | יומי |
| `RER_EUR_ILS` | שער חליפין אירו-שקל | יומי |
| `CPI_1Y` | אינפלציה שנה עשרה | חודשי |
| `INT_RATE` | ריבית בנק ישראל | יומי |
| `M1` | היצע כסף M1 | חודשי |
| `M2` | היצע כסף M2 | חודשי |
| `CA_BALANCE` | מאזן שוטף | רבעוני |
| `EXPORTS_GOODS` | ייצוא סחורות | חודשי |
| `IMPORTS_GOODS` | ייבוא סחורות | חודשי |
| `HOUSING_STARTS` | התחלות בנייה | חודשי |
| `HOUSE_PRICE_INDEX` | מדד מחירי דיור | חודשי |

### פונקציה מלאה לשליפת נתוני BOI

```python
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_boi_series(series_id, start_date=None, end_date=None):
    """
    שולפת סדרת נתונים מ-API בנק ישראל.

    Args:
        series_id: קוד הסדרה (לדוגמה: 'RER_USD_ILS')
        start_date: תאריך התחלה בפורמט 'YYYY-MM' (ברירת מחדל: 3 שנים אחורה)
        end_date: תאריך סיום (ברירת מחדל: היום)

    Returns:
        pd.DataFrame עם עמודות: date, value
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m")

    url = (
        f"https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/{series_id}/"
        f"?startperiod={start_date}&endperiod={end_date}&format=sdmx-json"
    )

    print(f"  שולפת: {series_id} ({start_date} → {end_date})...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # זורק exception אם status >= 400
    except requests.exceptions.Timeout:
        print("  ✗ timeout – השרת לא ענה")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  ✗ שגיאת HTTP: {e}")
        return None

    data = response.json()

    # פרסור SDMX-JSON
    try:
        series_data = data["data"]["dataSets"][0]["series"]
        observations = list(series_data.values())[0]["observations"]

        time_periods = data["data"]["structure"]["dimensions"]["observation"][0]["values"]
        periods = [t["name"] for t in time_periods]

        records = []
        for idx, (_, vals) in enumerate(observations.items()):
            records.append({
                "date": periods[int(idx)],
                "value": vals[0]
            })

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
        df.columns = ["date", series_id]

        print(f"  ✓ {len(df)} נקודות נתונים")
        return df

    except (KeyError, IndexError) as e:
        print(f"  ✗ שגיאה בפרסור: {e}")
        return None
```

### שימוש בפונקציה

```python
# שליפת ריבית
interest_df = fetch_boi_series("INT_RATE", "2020-01", "2024-12")
print(interest_df.head())

# שליפת שע"ח
exchange_df = fetch_boi_series("RER_USD_ILS", "2022-01")

# שליפת אינפלציה
cpi_df = fetch_boi_series("CPI_1Y", "2015-01")

# שליפת מספר סדרות
time.sleep(1)  # חשוב! אל תפגע בשרת עם בקשות רבות
housing_df = fetch_boi_series("HOUSE_PRICE_INDEX", "2018-01")

# מיזוג סדרות
macro_df = interest_df.merge(exchange_df, on="date", how="inner")
macro_df = macro_df.merge(cpi_df, on="date", how="left")
print(macro_df.tail())
```

### ויזואליזציה: ריבית + שע"ח

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# ריבית
ax1.step(interest_df["date"], interest_df["INT_RATE"],
         color="royalblue", linewidth=2, label="ריבית (%)")
ax1.set_ylabel("ריבית (%)")
ax1.set_title("מדיניות בנק ישראל – ריבית ושע\"ח")
ax1.grid(True, alpha=0.3)
ax1.legend()

# שע"ח
ax2.plot(exchange_df["date"], exchange_df["RER_USD_ILS"],
         color="darkorange", linewidth=1.5, label="₪/$")
ax2.set_ylabel("שקל לדולר")
ax2.set_xlabel("תאריך")
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig("boi_monetary_policy.png", dpi=150)
plt.show()
```

---

## חלק ג – ניהול מפתחות API ב-.env

### למה לא להכניס keys קשה-קודד בקוד?

```python
# ❌ רע מאוד! אל תעשה את זה!
api_key = "sk-1234abcd5678efgh"  # כשתעלה ל-GitHub, כולם יראו!
```

### הפתרון: קובץ `.env`

```bash
# 1. התקן python-dotenv
pip install python-dotenv

# 2. צור קובץ .env (בתיקיית הפרויקט)
# ⚠️ קובץ זה לעולם לא מועלה ל-GitHub!
```

```bash
# .env  (אל תוסיף לגיטהאב!)
CBS_API_KEY=your_cbs_key_here
FRED_API_KEY=your_fred_key_here
OECD_APP_NAME=EconLab_App
```

```python
# 3. השתמש בקוד
from dotenv import load_dotenv
import os

load_dotenv()  # טוען את .env לסביבה

cbs_key = os.getenv("CBS_API_KEY")
fred_key = os.getenv("FRED_API_KEY")

print(cbs_key)  # None אם לא הוגדר, הערך אם הוגדר
```

### ה-.gitignore חייב לכלול

```
# .gitignore
.env
*.env
.env.*
```

---

## חלק ד – הלמ"ס (CBS): נתוני אוכלוסייה ותעסוקה

### API הלמ"ס

הלמ"ס מספק נתונים בכמה פורמטים. המומלץ ביותר הוא JSON דרך הממשק הגרפי.

```python
import requests
import pandas as pd

def fetch_cbs_series(table_id, format="json"):
    """
    שולפת טבלת נתונים מהלמ"ס.
    table_id: מספר הטבלה מאתר cbs.gov.il
    """
    base_url = "https://www.cbs.gov.il/he/pages/download.aspx"
    params = {
        "ver": "now",
        "Id": table_id,
    }

    # הלמ"ס לרוב מספק קבצי Excel
    url = f"https://www.cbs.gov.il/he/publications/LochutTlushim/{table_id}.xlsx"

    print(f"מוריד טבלה {table_id}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # שמור לקובץ זמני
        with open(f"cbs_{table_id}.xlsx", "wb") as f:
            f.write(response.content)
        df = pd.read_excel(f"cbs_{table_id}.xlsx", skiprows=5, header=0)
        return df
    except Exception as e:
        print(f"שגיאה: {e}")
        return None

# נתוני תעסוקה רבעוניים (שנה ודוגמה)
# לרוב צריך להוריד ידנית מהאתר ולעבד
```

### עיבוד נתוני הלמ"ס (שנורד ידנית)

```python
# אחרי הורדת קובץ מהלמ"ס:
df = pd.read_excel(
    "employment_quarterly.xlsx",
    sheet_name="עיקרי",
    header=3,              # כותרת בשורה 4
    skipfooter=5           # בלי שורות סיכום תחתיות
)

# ניקוי שמות עמודות (הלמ"ס משתמש בכותרות ארוכות)
df.columns = [str(c).strip() for c in df.columns]

# בחר עמודות רלוונטיות
df = df[["רבעון", "שיעור אבטלה", "שיעור תעסוקה", "שכר ממוצע"]]

# המרת רבעון לתאריך
def quarter_to_date(quarter_str):
    """'2022-I' → datetime(2022, 1, 1)"""
    year, q = quarter_str.split("-")
    month = {"I": 1, "II": 4, "III": 7, "IV": 10}[q]
    return pd.Timestamp(int(year), month, 1)

df["date"] = df["רבעון"].apply(quarter_to_date)
df = df.set_index("date").sort_index()

print(df.head())
```

---

## חלק ה – שילוב BOI + הלמ"ס: ניתוח מלא

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

print("=== Pipeline נתונים ישראלי ===\n")

# 1. שליפת ריבית מ-BOI
interest = fetch_boi_series("INT_RATE", "2019-01", "2024-12")
interest = interest.set_index("date").resample("Q").mean()  # רבעוני

# 2. שליפת שע"ח מ-BOI
time.sleep(0.5)
exchange = fetch_boi_series("RER_USD_ILS", "2019-01", "2024-12")
exchange = exchange.set_index("date").resample("Q").mean()

# 3. שליפת מדד דיור מ-BOI
time.sleep(0.5)
housing_idx = fetch_boi_series("HOUSE_PRICE_INDEX", "2019-01", "2024-12")
housing_idx = housing_idx.set_index("date").resample("Q").mean()

# 4. מיזוג כל הסדרות
combined = pd.concat([interest, exchange, housing_idx], axis=1)
combined.columns = ["interest_rate", "usd_ils", "house_price_idx"]
combined = combined.dropna()

print("\nנתונים משולבים:")
print(combined.tail(8))

# 5. ניתוח: קורלציה ריבית-דיור
corr = combined.corr()
print(f"\nקורלציה: ריבית ↔ מדד דיור = {corr.loc['interest_rate', 'house_price_idx']:.3f}")

# 6. ויזואליזציה
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle("ישראל: ריבית, שע\"ח, ומחירי דיור", fontsize=14, fontweight="bold")

axes[0].step(combined.index, combined["interest_rate"],
             color="royalblue", linewidth=2)
axes[0].set_ylabel("ריבית (%)")

axes[1].plot(combined.index, combined["usd_ils"],
             color="darkorange", linewidth=1.5)
axes[1].set_ylabel("₪/$")

axes[2].plot(combined.index, combined["house_price_idx"],
             color="darkgreen", linewidth=2)
axes[2].set_ylabel("מדד מחירי דיור")
axes[2].set_xlabel("רבעון")

for ax in axes:
    ax.grid(True, alpha=0.3)
    ax.axvspan(pd.Timestamp("2022-01"), pd.Timestamp("2023-10"),
               alpha=0.08, color="red", label="תקופת העלאת ריבית")

plt.tight_layout()
plt.savefig("israel_monetary_housing.png", dpi=150)
plt.show()

# 7. ייצוא
combined.to_csv("israel_economic_indicators.csv", encoding="utf-8-sig")
print("\n✓ Pipeline הסתיים! קבצים נשמרו.")
```

---

## חלק ו – Rate Limiting ו-Caching

### לא לפגוע בשרתים!

```python
import time
import json
import os

def fetch_with_cache(series_id, start_date, end_date, cache_dir="cache"):
    """
    שולפת עם cache מקומי – לא מפציצה את השרת.
    """
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/{series_id}_{start_date}_{end_date}.pkl"

    # אם קיים בcache – השתמש
    if os.path.exists(cache_file):
        print(f"  ↩ cache: {series_id}")
        return pd.read_pickle(cache_file)

    # אחרת – שלוף ושמור
    df = fetch_boi_series(series_id, start_date, end_date)
    if df is not None:
        df.to_pickle(cache_file)
    time.sleep(0.3)  # המתן בין בקשות
    return df

# שימוש
interest = fetch_with_cache("INT_RATE", "2020-01", "2024-12")
```

---

## משימות השבוע

### משימה 1: BOI Pipeline (40 נקודות)

כתוב `boi_pipeline.py` שעושה:
1. שולף **4 סדרות** מ-BOI (ריבית, שע"ח, CPI, מדד דיור)
2. ממיר לרבעוני עם `resample`
3. מחשב: ריבית ריאלית, שינוי % שנתי בשע"ח ובמדד דיור
4. מיזוג ל-DataFrame אחד
5. מציג: קורלציה מטריצה + 4 גרפים
6. שומר ל-CSV

### משימה 2: מאגר נתונים כלכלי ישראלי (60 נקודות)

בנה `israel_data_hub.py` שמכיל:

```python
class IsraelEconomyHub:
    """מאגר נתונים כלכלי ישראלי עם cache אוטומטי."""

    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_interest_rates(self, start="2019-01", end=None):
        """מחזיר ריבית בנק ישראל."""
        pass

    def get_exchange_rates(self, currency="USD", start="2019-01", end=None):
        """מחזיר שע"ח לפי מטבע: USD, EUR, GBP."""
        pass

    def get_inflation(self, start="2019-01", end=None):
        """מחזיר נתוני CPI."""
        pass

    def get_housing_index(self, start="2019-01", end=None):
        """מחזיר מדד מחירי דיור."""
        pass

    def get_macro_summary(self, start="2020-01", end=None):
        """מחזיר DataFrame משולב עם כל המדדים."""
        pass

    def plot_monetary_policy(self, save=True):
        """מציג גרף מדיניות מוניטרית: ריבית + CPI."""
        pass
```

**בדיקה:**
```python
hub = IsraelEconomyHub()
df = hub.get_macro_summary("2020-01", "2024-12")
print(df.describe())
hub.plot_monetary_policy()
```

---

## הגשה

```
Members/YourName/Week_11/
├── boi_pipeline.py
├── israel_data_hub.py
├── israel_monetary_housing.png
└── week11_findings.md
```

---

**השבוע הבא:** APIs בין-לאומיים – בנק עולמי, OECD, FRED → [שבוע 12](../Week_12_APIs_International/README.md)
