# משימה 9 – Power BI / Tableau: דשבורדים לקובעי מדיניות

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=ZyhVh-qRZPA >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=txMibs211Yk >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=W9XjIGF9HZQ >}}

:::
## בחר כלי

| Power BI | Tableau Public |
|---|---|
| Windows בלבד | Windows + Mac |
| חינם (Desktop) | חינם (Public) |
| מוטמע ב-Microsoft 365 | קהילתי, פתוח |
| נפוץ בממשלה/בנקים | נפוץ ב-NGO/מחקר |

הורד **אחד מהם**:
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
- [Tableau Public](https://public.tableau.com/en-us/s/download)

---

## חלק א – ייבוא נתונים

### Power BI:
1. `Get Data → Text/CSV`
2. ייבא את `israel_macro.csv` (שמור מ-Python: `df.to_csv("israel_macro.csv", index=False)`)
3. `Transform Data` – ודא שסוגי הנתונים נכונים (שנה = Integer, אחוזים = Decimal)

### Tableau:
1. `Connect → To a File → Text File`
2. בחר את ה-CSV
3. בדוק ב-Data Source tab שהעמודות נכונות

---

## חלק ב – בנה דשבורד מאקרו-כלכלי

### Power BI – שלב אחר שלב:

**כרטיס 1: KPI Cards**
- KPI: ממוצע צמיחת תמ"ג (Measure: `AVERAGE(macro[gdp_growth])`)
- KPI: אינפלציה אחרונה
- KPI: ריבית נוכחית

**ויז 1: גרף קו – צמיחת תמ"ג לאורך זמן**
- X-axis: `year`, Y-axis: `gdp_growth`
- הוסף Reference Line ב-0

**ויז 2: Clustered Bar – ישראל vs ממוצע OECD**
(ייבא נתוני OECD מ-CSV נפרד)

**Slicer: סנן לפי טווח שנים**
- `Insert → Slicer → year`

**ויז 3: Scatter Plot – Phillips Curve**
- X: `unemployment`, Y: `inflation`
- Play Axis: `year` (אנימציה!)

---

## חלק ג – חיבור Python ל-Power BI (מתקדם)

Power BI יכול להריץ קוד Python ישירות!

```python
# בתוך Power BI: Transform Data → Run Python Script
# הקוד הבא ייצא DataFrame לתוך Power BI:

import pandas as pd
import wbgapi as wb

df = wb.data.DataFrame(
    "NY.GDP.MKTP.KD.ZG",
    economy=["ISR", "USA", "DEU"],
    time=range(2010, 2025)
).reset_index()
df.columns = ["year"] + [c for c in df.columns[1:]]
# Power BI יקרא את dataset (df) אוטומטית
```

---

## המשימה שלך

בנה דשבורד שמראה **3-5 מחווני מאקרו של ישראל** לשנים 2010–2024.

**דרישות מינימום:**
- [ ] לפחות 3 ויזואליזציות שונות
- [ ] Slicer/Filter אחד לפחות
- [ ] כותרת ברורה + מקור נתונים
- [ ] ניתן להבין בלי הסבר

---

## הגשה

תיקייה: `Members/YourName/Week_09/`

**Power BI:**
- שמור כ-`macro_dashboard.pbix` **ואל תעלה ל-Git** (קובץ בינארי)
- **במקום זה:** עשה `Export → PDF` ועלה `macro_dashboard.pdf`
- וגם: Export לתמונה של כל עמוד ועלה PNG

**Tableau:**
- Publish ל-Tableau Public
- צרף קישור ב-`dashboard_link.md`

---

**השבוע הבא:** DSGE – המאתגר שבכולם → [משימה 10](../Week_10_DSGE/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_09_BI_Tools/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

