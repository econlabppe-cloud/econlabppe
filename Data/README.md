# Data – מדיניות נתונים

## עיקרון מנחה

**GitHub = קוד | Google Drive = נתונים גדולים**

---

## גבולות GitHub – מה מותר ומה אסור?

| גודל קובץ | GitHub | Google Drive |
|---|---|---|
| < 1 MB | ✅ אפשרי (JSON, YAML, מטה-דאטה) | אפשרי |
| 1–50 MB | ⚠️ אפשרי אך לא מומלץ לנתונים | עדיף |
| 50–100 MB | ⚠️ אזהרה אוטומטית | כן |
| > 100 MB | ❌ חסום (דחיית push) | כן |
| > 1 GB (repo כולו) | ❌ GitHub מגביל | Google Drive |

**כלל אצבע:** אם הנתונים גדולים מ-5MB – שלח לDrive.

---

## מה מותר לשים כאן (ב-Git)?

```
Data/
├── README.md                  ← המסמך הזה
├── sources.md                 ← תיאור מקורות נתונים
├── data_dictionary.yaml       ← מילון נתונים (מבנה, יחידות, הגדרות)
├── schema/
│   └── macro_annual.sql       ← הגדרת סכמת SQL (ללא נתונים)
└── samples/
    └── macro_sample_5rows.csv ← דגימה קטנה (< 1MB) לתיעוד בלבד
```

## מה **אסור**?

- `*.csv` גדולים (> 5MB)
- `*.xlsx`, `*.xls`
- `*.parquet`, `*.feather`, `*.h5`
- קבצי מודל (`*.pkl`, `*.joblib`)

---

## מבנה תיקיית Google Drive

```
Google Drive/
└── EconLab_Data/
    ├── Raw/                    ← נתונים גולמיים כפי שהורדו
    │   ├── BOI/                ← נתוני בנק ישראל
    │   │   ├── interest_rate_2010_2024.csv
    │   │   └── exchange_rates_daily.csv
    │   ├── CBS/                ← נתוני הלמ"ס
    │   │   ├── population_by_district.xlsx
    │   │   └── wages_2015_2024.xlsx
    │   ├── WorldBank/          ← נתוני הבנק העולמי
    │   └── External/           ← מאמרים, דוחות PDF
    │
    ├── Processed/              ← נתונים לאחר ניקוי ועיבוד
    │   └── israel_macro_clean.parquet
    │
    └── Final/                  ← נתונים מוכנים לניתוח
        └── macro_annual_2000_2024.parquet
```

> 📁 [תיקיית Google Drive המשותפת – יש להחליף קישור](https://drive.google.com/placeholder)

---

## מקורות נתונים ומדריכים

| מקור | מה יש | דרך גישה | מדריך |
|---|---|---|---|
| בנק ישראל | ריבית, שע"ח, אינפלציה, מ"ת | API פתוח (SDMX) | [Cookbook/boi_api.md](../Cookbook/boi_api.md) |
| הלמ"ס | אוכלוסייה, שכר, תעסוקה | Excel + API חלקי | [Cookbook/cbs_api.md](../Cookbook/cbs_api.md) |
| הבנק העולמי | תמ"ג, חוב, סחר, 200 מדינות | wbgapi | [Cookbook/worldbank_api.md](../Cookbook/worldbank_api.md) |
| OECD | השוואה בין-מדינתית | SDMX-JSON | [Cookbook/oecd_api.md](../Cookbook/oecd_api.md) |
| רשות המסים | הכנסות המדינה, עובדים | Excel (data.gov.il) | - |
| FRED | מאקרו אמריקאי (Fed) | API + pandas-datareader | - |
| IMF WEO | תחזיות עולמיות | Excel / API | - |

---

## קוד לגישה ל-Google Drive מ-Python

```python
# pip install google-auth google-auth-oauthlib google-api-python-client

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io, pandas as pd

# שים credentials.json ב-.gitignore!
creds = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)
service = build("drive", "v3", credentials=creds)

def download_drive_csv(file_id: str) -> pd.DataFrame:
    """הורד CSV מ-Google Drive לתוך DataFrame."""
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    return pd.read_csv(buffer, encoding="utf-8-sig")
```

> ⚠️ `credentials.json` – לעולם לא ב-Git! הוסף ל-`.gitignore`.

---

## מוסכמות שמות קבצים בDrive

```
{source}_{topic}_{freq}_{start}_{end}.{ext}

דוגמאות:
boi_interest_rate_monthly_2010_2024.csv
cbs_wages_annual_2015_2024.xlsx
wb_gdp_growth_annual_2000_2024.parquet
```

---

*שינוי מדיניות זו דורש אישור מנהל המעבדה.*
