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
    """אחזר סדרה עתית מ-API בנק ישראל."""
    # TODO: implement
    raise NotImplementedError
```

---
*יש להשלים את הפונקציה ולהוסיף דוגמאות נוספות.*
