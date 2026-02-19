# Cookbook: API ה-OECD

> ה-OECD מספק נתונים לכל 38 המדינות החברות + מדינות שותפות.
> ישראל חברה ב-OECD מ-2010 – מה שמאפשר השוואות ישירות.

---

## שתי דרכי גישה

### 1. `pandasdmx` – ספרייה ייעודית (מומלץ)
```bash
pip install pandasdmx requests pandas
```

### 2. `requests` ישיר – API JSON
```bash
pip install requests pandas
```

---

## דוגמת קוד: pandasdmx

```python
"""
oecd_api_sdmx.py – נתוני OECD דרך pandasdmx
pip install pandasdmx requests pandas matplotlib
"""

import pandasdmx as sdmx
import pandas as pd
import matplotlib.pyplot as plt

# ---- התחבר ל-OECD ----
oecd = sdmx.Request("OECD")

# ---- רשימת datasets זמינים ----
# dataflows = oecd.dataflow()
# print(dataflows.dataflow)  # הסר הערה לצפייה ברשימה

# ==========================================
# דוגמה 1: אינפלציה ב-OECD (MEI dataset)
# ==========================================

resp = oecd.data(
    "MEI",
    key={"SUBJECT": "CPALTT01",  # CPI Total
         "COUNTRY": "ISR+USA+DEU+GBR+JPN",
         "FREQUENCY": "A"},      # Annual
    params={"startTime": "2010", "endTime": "2024"}
)
df_cpi = resp.to_pandas()

# השטח את ה-MultiIndex
if isinstance(df_cpi.index, pd.MultiIndex):
    df_cpi = df_cpi.reset_index()

print("נתוני CPI מ-OECD:")
print(df_cpi.head(10))


# ==========================================
# דוגמה 2: אבטלה
# ==========================================

resp_unemp = oecd.data(
    "MEI",
    key={"SUBJECT": "LRUNTTTT",
         "COUNTRY": "ISR+USA+DEU",
         "FREQUENCY": "A"},
    params={"startTime": "2010", "endTime": "2024"}
)
df_unemp = resp_unemp.to_pandas()
print("\nנתוני אבטלה מ-OECD:")
print(df_unemp.head())
```

---

## דרך חלופית: requests ישיר (אם pandasdmx לא עובד)

```python
"""
oecd_api_requests.py – OECD דרך requests ישיר
pip install requests pandas
"""

import requests
import pandas as pd
from io import StringIO


def fetch_oecd_csv(dataset: str, country: str, subject: str,
                   start: str = "2010", end: str = "2024") -> pd.DataFrame:
    """
    שאל נתונים מ-OECD Stats בפורמט CSV.

    Args:
        dataset: שם ה-dataset (לדוגמה 'MEI')
        country: קודי מדינות מופרדים ב-+ (לדוגמה 'ISR+USA')
        subject: קוד האינדיקטור (לדוגמה 'CPALTT01')
        start:   שנת התחלה
        end:     שנת סיום
    """
    url = (
        f"https://stats.oecd.org/SDMX-JSON/data/{dataset}/"
        f"{country}.{subject}.A/all?"
        f"startTime={start}&endTime={end}&contentType=csv"
    )
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))


# ==========================================
# שימוש
# ==========================================
if __name__ == "__main__":
    # אינפלציה
    df = fetch_oecd_csv(
        dataset="MEI",
        country="ISR+USA+DEU+GBR",
        subject="CPALTT01",
        start="2010",
        end="2024"
    )
    print("אינפלציה OECD:")
    print(df.head(10))
    print("עמודות:", list(df.columns))

    # אם יש עמודת COUNTRY ו-Value:
    if "COUNTRY" in df.columns and "Value" in df.columns:
        df_pivot = df.pivot_table(
            index="TIME", columns="COUNTRY", values="Value"
        )
        print("\nסיכום:")
        print(df_pivot.tail(5))
```

---

## אינדיקטורים נפוצים ב-MEI

| קוד SUBJECT | תיאור |
|---|---|
| `CPALTT01` | אינפלציה – CPI כולל |
| `LRUNTTTT` | אבטלה (% מכוח העבודה) |
| `NAEXKP01` | צמיחת GDP (% שנתי) |
| `IRLTLT01` | ריבית ארוכת טווח (אג"ח 10 שנים) |
| `IRSTCB01` | ריבית קצרת טווח |
| `XTIMVA01` | ייצוא סחורות |
| `XTEXVA01` | יבוא סחורות |

---

## גרף: ישראל vs ממוצע OECD

```python
# לאחר שטענת df_pivot:
fig, ax = plt.subplots(figsize=(12, 5))
for country in df_pivot.columns:
    alpha = 1.0 if country == "ISR" else 0.4
    lw = 2.5 if country == "ISR" else 1
    ax.plot(df_pivot.index, df_pivot[country],
            label=country, alpha=alpha, linewidth=lw)
ax.set_title("אינפלציה – ישראל vs. OECD")
ax.set_xlabel("שנה")
ax.set_ylabel("% שינוי שנתי")
ax.legend(ncol=4, fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("oecd_inflation.png", dpi=150)
```

---

## OECD Data Explorer (ממשק ויזואלי)

לפני שכותבים קוד: כדאי לבדוק את הנתונים ב:
**[data-explorer.oecd.org](https://data-explorer.oecd.org)**
שם אפשר לסנן, לצפות ולייצא CSV ידנית.

---

*עודכן: 2025 | מקור: [stats.oecd.org](https://stats.oecd.org)*
