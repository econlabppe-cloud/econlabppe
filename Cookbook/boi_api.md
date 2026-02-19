# Cookbook: API בנק ישראל (BOI)

> ה-API של בנק ישראל הוא **פתוח לחלוטין** – אין צורך ב-API Key.
> מכסה: ריבית, שע"ח, אינפלציה, מאזן תשלומים, שוק ההון ועוד.

---

## בסיס ה-API

```
https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/{SERIES_CODE}/?startperiod={YYYY}&format=csv
```

---

## קודי סדרות נפוצות

| קוד | תיאור | תדירות |
|---|---|---|
| `RER_USD_ILS` | שע"ח דולר/שקל (ממוצע) | יומי |
| `RER_EUR_ILS` | שע"ח יורו/שקל | יומי |
| `CPI_1Y` | מדד מחירים לצרכן (שנתי %) | חודשי |
| `INT_RATE` | ריבית בנק ישראל | חודשי |
| `M1` | כסף במחזור (M1) | חודשי |
| `CA_BALANCE` | מאזן שוטף | רבעוני |

> לרשימה מלאה: [boi.org.il → נתונים סטטיסטיים → API](https://www.boi.org.il/roles/statistics/seriesapi/)

---

## קוד Python מלא

```python
"""
boi_api.py – שאילתות מ-API בנק ישראל
======================================
pip install requests pandas matplotlib
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO


BOI_BASE = (
    "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/"
    "BOI.STATISTICS/{series_code}/?startperiod={start}&format=csv"
)


def fetch_boi_series(series_code: str, start_year: int = 2015) -> pd.DataFrame:
    """
    שאל סדרה עתית מ-API בנק ישראל.

    Args:
        series_code: קוד הסדרה (לדוגמה 'RER_USD_ILS')
        start_year:  שנת התחלה

    Returns:
        DataFrame עם עמודות: period, value
    """
    url = BOI_BASE.format(series_code=series_code, start=start_year)

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"שגיאה בגישה ל-API: {e}") from e

    df = pd.read_csv(StringIO(resp.text))

    # נקה עמודות
    df.columns = df.columns.str.strip().str.lower()

    # מצא עמודות רלוונטיות (שם יכול להשתנות לפי סדרה)
    period_col = next((c for c in df.columns if "period" in c or "time" in c), None)
    value_col  = next((c for c in df.columns if "value" in c or "obs" in c), None)

    if not period_col or not value_col:
        raise ValueError(f"לא נמצאו עמודות מתאימות. עמודות: {list(df.columns)}")

    result = df[[period_col, value_col]].copy()
    result.columns = ["period", "value"]
    result["value"] = pd.to_numeric(result["value"], errors="coerce")
    result = result.dropna()
    return result


# ==========================================
# דוגמה 1: שע"ח דולר/שקל
# ==========================================
if __name__ == "__main__":
    print("מושך שע\"ח דולר/שקל...")
    df_fx = fetch_boi_series("RER_USD_ILS", start_year=2015)
    print(df_fx.tail(5))

    # ==========================================
    # דוגמה 2: ריבית בנק ישראל
    # ==========================================
    print("\nמושך ריבית בנק ישראל...")
    df_rate = fetch_boi_series("INT_RATE", start_year=2015)
    print(df_rate.tail(5))

    # ==========================================
    # גרף: שע"ח וריבית
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(df_fx["period"], df_fx["value"], color="steelblue", linewidth=1.5)
    ax1.set_title("שע\"ח דולר/שקל")
    ax1.set_ylabel("₪ לדולר")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(alpha=0.3)

    ax2.step(df_rate["period"], df_rate["value"],
             where="post", color="tomato", linewidth=2)
    ax2.fill_between(df_rate["period"], df_rate["value"],
                     step="post", alpha=0.2, color="tomato")
    ax2.set_title("ריבית בנק ישראל (%)")
    ax2.set_ylabel("%")
    ax2.tick_params(axis="x", rotation=45)
    ax2.grid(alpha=0.3)

    fig.text(0.5, 0.01, "מקור: בנק ישראל – API פתוח",
             ha="center", fontsize=9, color="gray")
    plt.tight_layout()
    plt.savefig("boi_data.png", dpi=150)
    plt.show()
    print("גרף נשמר כ-boi_data.png")
```

---

## דוגמה מהירה: שאל ריבית אחרונה

```python
import requests, json

url = ("https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/"
       "BOI.STATISTICS/INT_RATE/?startperiod=2024&format=csv")
import pandas as pd
from io import StringIO
df = pd.read_csv(StringIO(requests.get(url).text))
print("ריבית אחרונה:", df.iloc[-1].to_dict())
```

---

## שימושי נוסף: ה-API עם JSON

```python
# לקבלת metadata ורשימת סדרות:
url = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/dataflow/BOI.STATISTICS/all?format=json"
resp = requests.get(url, timeout=30)
# ה-response מכיל את כל הסדרות הזמינות
```

---

## שגיאות נפוצות

| שגיאה | פתרון |
|---|---|
| `HTTPError: 404` | קוד הסדרה שגוי – בדוק ברשימה |
| `ConnectionError` | בדוק חיבור לאינטרנט |
| `KeyError` בעמודות | ה-API שינה פורמט – הדפס `df.columns` |

---

*עודכן: 2025 | מקור: [boi.org.il](https://www.boi.org.il)*
