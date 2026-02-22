# שבוע 20 – Tableau: ויזואליזציה מקצועית ו-Storytelling

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=aHaOIvR00So >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=7EQCUKhhOJw >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=2A9794u-554 >}}

:::
## Power BI vs. Tableau

| Power BI | Tableau |
|---|---|
| ממוקד ב-Microsoft ecosystem | עצמאי לחלוטין |
| DAX – שפה חזקה | Calculations – פשוטות יותר |
| שיתוף בחינם עם Microsoft | Tableau Public חינמי (פומבי) |
| **מומלץ לארגונים** | **מומלץ לפרסום ועיתונאות** |
| Drag-and-drop טוב | **Drag-and-drop מעולה** |

---

## חלק א – התקנה

### Tableau Public (חינמי!)

הורד: [public.tableau.com](https://public.tableau.com/app/discover)

- **ניצול:** שמירת עבודה בענן הציבורי של Tableau
- **מגבלה:** כל הנתונים גלויים לציבור (בשלב זה – מספיק)
- **לדשבורדים פרטיים:** Tableau Desktop (בתשלום) / חינם לסטודנטים

### מבנה Tableau

```
┌─────────────────────────────────────────────────────────┐
│  Data Source (חיבור נתונים)                             │
├───────────┬─────────────────────────────────────────────┤
│  Sheets   │         Worksheet Canvas                    │
│  (גיליונות│  ┌──────────┬────────────────────────────┐  │
│  ודשבורד) │  │ Columns  │      Chart Area             │  │
│           │  ├──────────┤  (גרר שדות לפה)             │  │
│  Data     │  │  Rows    │                              │  │
│  Pane     │  ├──────────┴────────────────────────────┤  │
│  (שדות)   │  │ Marks Card: Color, Size, Label, Detail │  │
└───────────┴──┴───────────────────────────────────────┴──┘
                [Dimensions | Measures]
```

---

## חלק ב – חיבור נתונים

### ייבוא נתונים

```
Connect pane → Text File (.csv) / Microsoft Excel
→ בחר קובץ → Drag Table to Canvas → Preview
```

### Join בין טבלאות

```
Data Source → גרור טבלה שנייה לאותה Canvas
→ Join Type בחר: Inner / Left / Right / Full Outer
→ Join Clause: בחר שדות מקבילים (Year = Year)
```

### Union: הוספת שורות

```
Data Source → שם טבלה → Union
→ גרור קבצים נוספים לאותה Union
```

### Tableau Prep (לניקוי)

```
מומלץ לניקוי מקדים:
Tableau Prep Builder → Connect → Transform → Output
```

---

## חלק ג – ויזואליזציות ב-Tableau

### הגיון הבנייה

```
1. גרור Dimension → Rows/Columns (יוצר צירים)
2. גרור Measure → Rows/Columns (יוצר ציר מדד)
3. שנה סוג גרף: Show Me (פינה ימין עליון)
4. הוסף צבע: גרור Dimension/Measure → Marks → Color
5. הוסף גודל: גרור Measure → Marks → Size
6. הוסף label: גרור Measure → Marks → Label
```

### Line Chart – סדרה עתית

```
Rows:    [GDP Growth (Avg)]
Columns: [Year]
Marks:   Line
Color:   [מדד] (אם כמה סדרות)

Add Reference Line:
→ Right-click Y-axis → Add Reference Line
→ Value: Average
→ Label: Custom "ממוצע: <Value>"
```

### Bar Chart עם Conditional Color

```
Rows:    [Year]
Columns: [GDP Growth (Avg)]
Marks:   Bar

Color based on value:
→ Marks → Color → Edit Colors → Stepped Color
   OR
→ גרור [GDP Growth] → Color
→ Edit Colors: Green-White-Red diverging, Center: 0
```

### Scatter Plot

```
Rows:    [GDP Growth (Avg)]
Columns: [Inflation (Avg)]
Marks:   Circle
Size:    [Unemployment (Avg)]
Color:   [Year] (continuous → color gradient)
Label:   [Year]
Detail:  [Year]

Trend Line:
→ Analytics pane → Drag Trend Line → Linear
```

### Map: Choropleth

```
Double-click שדה גיאוגרפי (country, city)
→ Tableau מזהה אוטומטית ויוצר מפה!
Marks:   Filled Map
Color:   [GDP per Capita]
Tooltip: [Country, Year, GDP]
```

### Histogram

```
Rows:    [GDP Growth (CNT)]
Columns: [GDP Growth (bin)]
→ Right-click [GDP Growth] → Create → Bins → Bin size: 1
Marks:   Bar
```

---

## חלק ד – Calculated Fields

```
Right-click שדה → Create Calculated Field...
```

### חישובים בסיסיים

```tableau
// ריבית ריאלית
[Interest Rate] - [Inflation]

// שינוי YoY
([GDP Growth] - LOOKUP(ZN([GDP Growth]), -1)) / ABS(LOOKUP(ZN([GDP Growth]), -1))

// סיווג
IF [GDP Growth] < 0 THEN "מיתון"
ELSEIF [GDP Growth] < 2 THEN "צמיחה איטית"
ELSEIF [GDP Growth] < 4 THEN "צמיחה נורמלית"
ELSE "צמיחה גבוהה"
END

// Level of Detail (LOD) expression
// ממוצע שנה ללא קשר לסינון הנוכחי
{ FIXED [Year] : AVG([GDP Growth]) }

// Rank
RANK(SUM([GDP Growth]))
```

### Table Calculations (חישובים יחסיים)

```
Right-click Measure → Add Table Calculation:
- Running Total → SUM
- Percent Difference → Year over Year
- Moving Average → 3 periods back
- Rank → Competition
```

---

## חלק ה – Filters ו-Parameters

### Filters (קבועים)

```
גרור Dimension/Measure → Filters shelf
→ בחר ערכים / טווח
→ Apply to Worksheets → All using this Data Source
```

### Quick Filters (לדשבורד)

```
Right-click Filter → Show Filter
→ מופיע כ-control בגיליון
→ ניתן להוסיף לדשבורד
```

### Parameters (דינמיים)

```
Data pane → Create Parameter
→ Name: "Select Year"
→ Data type: Integer
→ Range: Min 2018, Max 2024, Step 1

שימוש בגרף:
→ Create Calculated Field:
   IF [Year] = [Select Year] THEN "נבחר" ELSE "אחר" END
→ גרור ל-Color

→ Right-click Parameter → Show Parameter Control
   (כדי שיופיע בדשבורד)
```

---

## חלק ו – Dashboard: בניית הדשבורד

### יצירת Dashboard

```
Sheet Tab Bar → New Dashboard (או Ctrl+Shift+D)
```

### Layout

```
Dashboard pane (שמאל):
- Objects: Horizontal / Vertical / Text / Image / Web Page / Blank

גרור Sheets לתוך הדשבורד
→ Float: ריחוף חופשי
→ Tiled: בלוק קבוע (מומלץ)
```

### Layout מקצועי לדשבורד כלכלי

```
┌────────────────────────────────────────────────────┐
│  Image: לוגו + Title Text                          │
├──────────────────────────────────────────────────  │
│  Parameter: Year  │  Filter: Era  │  Filter: Status│
├────────────────────────────────────────────────────┤
│  Sheet 1: Line (GDP + CPI)  │  Sheet 2: Bar (GDP)  │
├────────────────────────────────────────────────────┤
│  Sheet 3: Scatter (CPI×GDP) │  Sheet 4: Map/Table  │
├────────────────────────────────────────────────────┤
│  Caption: "מקור: בנק ישראל | EconLab PPE"         │
└────────────────────────────────────────────────────┘
```

### Actions: אינטראקטיביות בין גרפים

```
Dashboard → Actions → Add Action
→ Filter Action:
   Source Sheets: [Bar Chart]
   Run on: Select
   Target Sheets: [Scatter Chart]
   Target Filters: [Year]
   → כשלוחצים על שנה בbar, ה-scatter מסתנן לאותה שנה!

→ Highlight Action:
   Source: כולם
   Target: כולם
   Fields: [Year]
   → hover על שנה אחת → מדגיש אותה בכל הגרפים
```

---

## חלק ז – Story: הצגה נרטיבית

**Story** ב-Tableau = פרזנטציה עם כמה "נקודות עלילה" שמספרות סיפור.

```
Sheet Tab Bar → New Story (Ctrl+Shift+S)
```

### מבנה Story כלכלי

```
Caption 1: "ישראל 2018: כלכלה צומחת"
→ Dashboard: נתוני 2018-2019

Caption 2: "2020: זעזוע הקורונה"
→ Dashboard: highlight 2020 + annotation

Caption 3: "2021-2022: התאוששות חזקה"
→ Dashboard: 2021-2022 עם trend

Caption 4: "2022-2024: אתגר הריבית"
→ Dashboard: ריבית vs. צמיחה

Caption 5: "השוואה בין-לאומית"
→ Dashboard: Map + scatter vs. OECD

Caption 6: "מסקנות ותחזית"
→ Dashboard: forecast + bullet points
```

### עיצוב Story

```
Format → Story → Story Title: גופן, צבע, גודל
Story Navigator: Arrow Bar / Dots / Numbers
Background: White
```

---

## חלק ח – פרסום ב-Tableau Public

### שמירה ופרסום

```
File → Save to Tableau Public → התחבר עם חשבון
→ בוחר שם → Publish
→ קבל לינק: https://public.tableau.com/views/YourWorkbook/...
```

### Embed בדוח HTML/GitHub

```html
<!-- קוד embed שמקבלים מ-Tableau Public -->
<div class='tableauPlaceholder' id='viz1234567890'>
  <noscript>
    <a href='#'><img alt='Dashboard' src='https://...' /></a>
  </noscript>
  <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' />
    <param name='name' value='YourWorkbook/Dashboard1' />
    <param name='tabs' value='no' />
    <param name='toolbar' value='yes' />
  </object>
</div>
<script src='https://public.tableau.com/javascripts/api/viz_v1.js'></script>
```

---

## חלק ט – השוואת Tableau ל-Python/R

### אותו ניתוח – שתי גישות

```r
# R ggplot2 (קוד)
ggplot(macro, aes(x = inflation, y = gdp_growth, color = era)) +
  geom_point(aes(size = unemployment)) +
  geom_smooth(method = "lm") +
  facet_wrap(~era) +
  theme_minimal()
```

```
# Tableau (ללא קוד)
Columns: Inflation (Avg)
Rows: GDP Growth (Avg)
Color: Era
Size: Unemployment (Avg)
Add Trend Line: Linear
Add Pages shelf: Era (ל-facet)
```

**מתי ל-Tableau:**
- מצגת להנהלה
- פרסום לציבור
- שותף לא-טכני צריך לחקור

**מתי ל-Python/R:**
- ניתוח סטטיסטי מעמיק
- automation
- נתונים גדולים מאוד

---

## משימות השבוע

### משימה 1: 5 Worksheets (25 נקודות)

```
1. Line Chart: GDP Growth + CPI + Interest (3 measures, dual axis)
2. Bar Chart: GDP Growth by Year – Conditional Color (ירוק/אדום)
3. Scatter: CPI vs GDP, size=unemployment, color=year, trend line
4. Choropleth Map: GDP per capita – 20+ מדינות
5. Bubble Chart: GDP × CPI × Unemployment (3 measures!)
```

### משימה 2: Dashboard + Actions (40 נקודות)

```
בנה דשבורד: "ישראל בעולם – מאקרו 2018-2024"
- 4 Sheets
- 2 Filters (Year, Era)
- 1 Parameter (Select Country)
- Filter Action: לחיצה על שנה → filter כל הגרפים
- Highlight Action: hover → highlight בכל הגרפים
- Tooltip מותאם אישית לכל גרף
```

### משימה 3: Story כלכלי (35 נקודות)

```
בנה Story: "5 שנים של ריבית – השפעה על הכלכלה הישראלית"

5 Story Points:
1. רקע: הכלכלה לפני 2022
2. ההחלטה: העלאת ריבית חדה
3. ההשפעה על צמיחה ואבטלה
4. ההשפעה על שוק הדיור
5. מסקנות: האם ניהול חכם?

→ פרסם ב-Tableau Public
→ שלח לינק
```

---

## הגשה

```
Members/YourName/Week_20/
├── tableau_link.md             ← לינק ל-Tableau Public
├── dashboard_screenshot.png
├── story_screenshot.png
└── story_summary.md            ← 5 ממצאים עיקריים
```

---

**המודול הבא:** DSGE – מודלים מאקרו-כלכליים דינמיים → [שבוע 21](../Week_21_DSGE_Intro/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_20_BI_Tableau/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

