# משימה 2 – Excel לניתוח כלכלי


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=k1VUZEVuDJ8](https://www.youtube.com/watch?v=k1VUZEVuDJ8) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=g1kmDtCyVLg](https://www.youtube.com/watch?v=g1kmDtCyVLg) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=9IeD-wB8kWE](https://www.youtube.com/watch?v=9IeD-wB8kWE) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=k1VUZEVuDJ8 >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=0bNJHrosMJU >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=9IeD-wB8kWE >}}

:::
## חלק א – נתוני הבסיס

הורד את הקובץ הבא מתיקיית Google Drive:
> 📁 `EconLab_Data/Raw/` → `israel_macro_2010_2024.xlsx`

הקובץ מכיל נתוני ישראל לשנים 2010–2024:
- תמ"ג (צמיחה שנתית %)
- אינפלציה (CPI שנתי %)
- אבטלה (%)
- ריבית בנק ישראל (%)

**אין גישה לדרייב?** עבוד עם נתונים מ-[boi.org.il → סטטיסטיקה](https://boi.org.il) ויצא Excel ידני.

---

## חלק ב – משימות

### 1. ניקוי ועיצוב (10 נקודות)
- הוסף כותרות ברורות לכל עמודה
- עצב כ-Table (Insert → Table)
- הוסף פורמט מספרי עם ספרה אחרת אחרי הנקודה
- צור גיליון נפרד `cleaned_data`

### 2. חישובים בסיסיים (20 נקודות)
בגיליון `analysis` חשב:
- ממוצע צמיחה 2010–2024: `=AVERAGE(...)`
- שנת הצמיחה הגבוהה ביותר: `=MAX(...)` + `=INDEX/MATCH`
- מספר שנים עם אינפלציה > 3%: `=COUNTIF(...)`
- מתאם בין צמיחה לאינפלציה: `=CORREL(...)`

### 3. Pivot Table (30 נקודות)
צור Pivot Table שמציג:
- ממוצע אינפלציה לפי עשור (2010–2019 vs 2020–2024)
- שנים עם ריבית > ממוצע: True/False בעמודה חדשה
- השתמש ב-Slicer לסינון לפי טווח שנים

### 4. גרפים (40 נקודות)
**גרף 1 – סדרה עתית:**
- ציר X: שנה, ציר Y: צמיחת תמ"ג
- הוסף קו מגמה (Trendline)
- עצב כך שאפשר להציג בפרזנטציה

**גרף 2 – Scatter Plot:**
- ציר X: אינפלציה, ציר Y: ריבית בנק ישראל
- כל נקודה = שנה אחת
- הוסף תווית לנקודות שנת 2022-2024 (עידן הריבית הגבוהה)

---

## הגשה

שמור כ-`Members/YourName/Week_02/israel_macro_analysis.xlsx` והעלה ל-GitHub.

> ⚠️ **רגע!** הקובץ הוא Excel. ה-`.gitignore` חוסם `.xlsx`!
> פתרון: שמור **גם** כ-`analysis_summary.md` עם ממצאים בכתב:

```markdown
# ממצאי ניתוח מאקרו ישראל 2010-2024

## ממוצעים
- צמיחת תמ"ג ממוצעת: X%
- אינפלציה ממוצעת: X%

## תובנות עיקריות
1. ...
2. ...
```

---

## ללמוד עוד

- [ExcelJet – Excel Functions](https://exceljet.net/excel-functions)
- [רשות המסים – נתוני הכנסות (Excel)](https://taxes.gov.il)

---

**השבוע הבא:** SQL – שאילתות על בסיסי נתונים → [משימה 3](../Week_03_SQL_Intro/README.md)
