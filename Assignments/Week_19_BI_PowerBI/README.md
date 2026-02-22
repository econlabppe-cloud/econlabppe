# שבוע 19 – Power BI: דשבורדים כלכליים לביזנס

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=AGrl-H87pRU >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=TmhQCQr_DCA >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=LqN68A5o8XQ >}}

:::
## למה Power BI?

| Excel | Python/R | Power BI |
|---|---|---|
| טבלאות מוכרות | גמיש לחלוטין | דשבורד ויזואלי מהיר |
| גרפים בסיסיים | גרפים מתקדמים | **אינטראקטיבי + responsive** |
| קשה לשתף | דורש קוד | **שיתוף בלחיצה** |
| תצוגה סטטית | עבודה בקוד | **Drag-and-drop** |

**Power BI = הכלי שמנהלים רוצים לראות.**

---

## חלק א – התקנה ומבנה

### התקנה

1. **Power BI Desktop** (חינמי): [powerbi.microsoft.com](https://powerbi.microsoft.com/desktop)
   - Windows בלבד
   - Mac: השתמש בענן (Power BI Service) או ב-VM

2. **Power BI Service** (ענן, חינמי עם חשבון Microsoft):
   [app.powerbi.com](https://app.powerbi.com)

### מבנה ה-Interface

```
┌──────────────────────────────────────────────────┐
│  Ribbon: Home | Insert | Modeling | View | Help   │
├─────┬────────────────────────────┬────────────────┤
│     │                            │  Fields Panel  │
│ Nav │     Canvas (הדשבורד)       │  (עמודות)      │
│     │                            ├────────────────┤
│     │                            │  Visualizations│
│     │                            │  (סוגי גרף)   │
│     │                            ├────────────────┤
│     │                            │  Filters Panel │
└─────┴────────────────────────────┴────────────────┘
     [Report View | Data View | Model View]
```

### 3 Views חשובים

| View | שימוש |
|---|---|
| **Report** | בניית הדשבורד |
| **Data** | צפייה ועריכת הנתונים |
| **Model** | הגדרת קשרים בין טבלאות |

---

## חלק ב – ייבוא נתונים

### מ-Excel/CSV

```
Home → Get Data → Excel/CSV → בחר קובץ → בחר גיליון → Load
```

### נתוני בנק ישראל – ישירות ממקור

```
Home → Get Data → Web →
URL: https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/INT_RATE/
     ?startperiod=2020-01&endperiod=2024-12&format=csv
```

### Transform Data (Power Query)

לפני הטעינה, פתח **Power Query Editor**:

```
Home → Transform Data
```

פעולות חיוניות ב-Power Query:

| פעולה | איפה | שימוש |
|---|---|---|
| Rename Column | Right-click → Rename | שם ברור |
| Change Type | Data Type → Decimal | תיקון טיפוסים |
| Remove Rows | Home → Remove Rows | ניקוי header/footer |
| Fill Down | Transform → Fill → Down | מילוי ריק |
| Unpivot | Transform → Unpivot Columns | Wide → Long |
| Merge Queries | Home → Merge Queries | כמו JOIN |
| Group By | Transform → Group By | כמו GROUP BY |

### Best Practice: טבלת תאריכים (Date Table)

כל מודל Power BI מקצועי צריך **טבלת תאריכים**.

```m
// Power Query M Code: Date Table
let
    StartDate = #date(2018, 1, 1),
    EndDate   = Date.From(DateTime.LocalNow()),
    DateList  = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1,0,0,0)),
    DateTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    AddYear   = Table.AddColumn(DateTable, "Year",    each Date.Year([Date]),    Int32.Type),
    AddMonth  = Table.AddColumn(AddYear,   "Month",   each Date.Month([Date]),   Int32.Type),
    AddQuarter= Table.AddColumn(AddMonth,  "Quarter", each Date.QuarterOfYear([Date]), Int32.Type),
    AddMonthName = Table.AddColumn(AddQuarter, "MonthName", each Date.ToText([Date], "MMM"), type text)
in
    AddMonthName
```

---

## חלק ג – Data Model: קשרים בין טבלאות

### Star Schema (מומלץ)

```
                    ┌─────────────┐
                    │  Date Table │
                    │  (Dim)      │
                    └──────┬──────┘
                           │ 1:Many
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────┴──────┐   ┌───────┴──────┐   ┌───────┴──────┐
│  Macro Table │   │ Housing Table│   │ Exports Table│
│  (Fact)      │   │  (Fact)      │   │  (Fact)      │
└──────────────┘   └──────────────┘   └──────────────┘
```

### הגדרת קשרים

```
Model View → גרור שדה Date מ-Date Table → שחרר על שדה Date בFact Table
→ Many to One → Cardinality: Many to one → Cross-filter: Single
```

---

## חלק ד – DAX: שפת החישובים של Power BI

**DAX** (Data Analysis Expressions) = שפת הנוסחאות של Power BI.

### Measures vs. Calculated Columns

| Measures | Calculated Columns |
|---|---|
| חישוב דינמי (לפי filter) | חישוב סטטי בכל שורה |
| לא שומר בזיכרון | שומר בזיכרון |
| **מומלץ לרוב החישובים** | לקטגוריות ותוויות |

### Measures בסיסיים

```dax
// ---- BASIC MEASURES ----

// ממוצע צמיחה
Avg GDP Growth =
    AVERAGE(MacroData[gdp_growth])

// ממוצע מסונן
Avg Inflation Post2022 =
    CALCULATE(
        AVERAGE(MacroData[inflation]),
        MacroData[year] >= 2022
    )

// ספירה עם תנאי
Recession Years =
    COUNTROWS(
        FILTER(MacroData, MacroData[gdp_growth] < 0)
    )

// ---- TIME INTELLIGENCE ----

// שינוי Year-over-Year
GDP YoY Change =
    VAR CurrentValue = AVERAGE(MacroData[gdp_growth])
    VAR PrevYearValue =
        CALCULATE(
            AVERAGE(MacroData[gdp_growth]),
            DATEADD(DateTable[Date], -1, YEAR)
        )
    RETURN
        IF(
            ISBLANK(PrevYearValue),
            BLANK(),
            CurrentValue - PrevYearValue
        )

// שנה קודמת
GDP Previous Year =
    CALCULATE(
        AVERAGE(MacroData[gdp_growth]),
        PREVIOUSYEAR(DateTable[Date])
    )

// YTD (Year-to-Date)
Inflation YTD =
    TOTALYTD(AVERAGE(MacroData[inflation]), DateTable[Date])

// Moving Average 3 שנים
GDP MA3 =
    AVERAGEX(
        DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -3, YEAR),
        CALCULATE(AVERAGE(MacroData[gdp_growth]))
    )

// ---- CONDITIONAL ----

// ריבית ריאלית
Real Interest Rate =
    AVERAGE(MacroData[interest]) - AVERAGE(MacroData[inflation])

// סיווג
Economic Status =
    VAR gdp = AVERAGE(MacroData[gdp_growth])
    RETURN
        SWITCH(
            TRUE(),
            gdp < 0,    "מיתון",
            gdp < 2,    "צמיחה איטית",
            gdp < 4,    "צמיחה נורמלית",
            "צמיחה גבוהה"
        )

// ---- RANKING ----

GDP Growth Rank =
    RANKX(
        ALL(MacroData[year]),
        [Avg GDP Growth],
        ,
        DESC
    )
```

### Calculated Columns

```dax
// בטבלת MacroData
Real Rate = MacroData[interest] - MacroData[inflation]

Era =
    IF(MacroData[year] <= 2021, "ריבית נמוכה", "ריבית גבוהה")

Status =
    SWITCH(
        TRUE(),
        MacroData[gdp_growth] < 0, "מיתון",
        MacroData[gdp_growth] < 2, "צמיחה איטית",
        "צמיחה"
    )
```

---

## חלק ה – ויזואליזציות: בניית הדשבורד

### ויזואליזציות מרכזיות לדשבורד כלכלי

#### 1. KPI Cards (מדדים מרכזיים)

```
Insert → Card
→ Fields: [Avg GDP Growth]
→ Format:
   - Display units: None
   - Decimal places: 1
   - Conditional formatting: Color scale (אדום-ירוק)
```

#### 2. Line Chart – סדרה עתית

```
Insert → Line Chart
→ X-axis: DateTable[Year]
→ Y-axis: [Avg GDP Growth], [Avg Inflation]
→ Legend: Measure Names
→ Format:
   - Reference line: Y = 0
   - Series: מדגיש את ישראל
```

#### 3. Bar/Column Chart

```
Insert → Clustered Bar Chart
→ Y-axis: MacroData[year]
→ X-axis: [Avg GDP Growth]
→ Format → Data colors → Conditional formatting
   - Rules: If value < 0 → Red, else Blue
```

#### 4. Scatter Chart

```
Insert → Scatter Chart
→ X-axis: [Avg Inflation]
→ Y-axis: [Avg GDP Growth]
→ Size: [Avg Unemployment]
→ Details: MacroData[year]
→ Play Axis: DateTable[Year]  ← Animation!
```

#### 5. Treemap – השוואת גדלים

```
Insert → Treemap
→ Category: MacroData[Status]
→ Values: COUNTROWS(MacroData)
→ Colors: Per Category
```

#### 6. Matrix (Pivot Table)

```
Insert → Matrix
→ Rows: MacroData[era]
→ Columns: DateTable[Year]
→ Values: [Avg GDP Growth], [Avg Inflation]
→ Conditional Formatting: Color Scale
```

### Slicers (פילטרים אינטראקטיביים)

```
Insert → Slicer
→ Field: DateTable[Year]
→ Style: Dropdown / Slider
→ הוסף slicer שני: MacroData[era]
```

---

## חלק ו – עיצוב הדשבורד

### Layout מקצועי

```
┌──────────────────────────────────────────────────┐
│  כותרת: "דשבורד מאקרו-כלכלי – ישראל"            │
├──────┬──────┬──────┬──────┬──────────────────────┤
│ KPI  │ KPI  │ KPI  │ KPI  │  Slicer: שנה        │
│ GDP  │ CPI  │ INT  │ UNE  │  Slicer: עידן        │
├──────────────────────────┬───────────────────────┤
│                          │                       │
│   Line Chart: 3 סדרות   │  Bar: צמיחה לפי שנה  │
│   (GDP, CPI, Interest)  │  (ירוק/אדום)          │
│                          │                       │
├──────────────────────────┼───────────────────────┤
│                          │                       │
│  Scatter: CPI vs GDP    │  Matrix: Era × Year   │
│  (size = unemployment)  │                        │
│                          │                       │
└──────────────────────────┴───────────────────────┘
```

### טיפים לעיצוב

```
1. Theme: View → Themes → בחר או ייבא JSON theme
2. Font: Segoe UI (standard Microsoft)
3. Background: Format → Canvas background → Light gray (#F5F5F5)
4. Card borders: Format → Border → כל card
5. Alignment: Format → Align → Distribute evenly
6. Tooltips: Format → Tooltip → הוסף שדות נוספים
```

### Custom Theme JSON

```json
{
  "name": "EconLab Theme",
  "dataColors": ["#1565C0", "#F57C00", "#2E7D32", "#C62828", "#6A1B9A", "#00838F"],
  "background": "#FFFFFF",
  "foreground": "#212121",
  "tableAccent": "#1565C0",
  "visualStyles": {
    "*": {
      "*": {
        "fontFamily": [{"value": "Segoe UI"}],
        "fontSize": [{"value": 11}]
      }
    }
  }
}
```

שמור כ-`.json` → View → Themes → Browse for themes.

---

## חלק ז – פרסום ושיתוף

### Power BI Service

```
Home → Publish → בחר Workspace
→ אחרי הפרסום: app.powerbi.com
```

### שיתוף דוח

```
Power BI Service → Report → Share → הזן Email
```

### ייצוא ל-PDF/PowerPoint

```
File → Export to PDF
File → Export to PowerPoint
```

### אפשרויות חינמיות

- **Publish to Web**: לינק ציבורי (זהירות – כולם רואים!)
- **Embed in Website**: embed code ל-iframe
- **Export PNG**: לצילום מסך של כל Visual

---

## משימות השבוע

### משימה 1: בניית מודל נתונים (25 נקודות)

```
1. ייבא 3 טבלאות לפחות:
   - MacroData (GDP, CPI, Interest, Unemployment)
   - HousingData (Price Index, Transactions by Quarter)
   - ExportsData (Exports, Imports by Category)

2. צור Date Table ב-Power Query (M Code)

3. הגדר קשרים ב-Model View (Star Schema)

4. צור Calculated Column: Era, Status, Real Rate

5. צור 5 Measures: Avg, YoY Change, Recession Count, Rank, MA3
```

### משימה 2: דשבורד מאקרו (40 נקודות)

בנה דשבורד עם:
- 4 KPI Cards (GDP, CPI, Interest, Unemployment)
- Line Chart: 3 סדרות עתיות + Reference Line
- Bar Chart: צמיחה לפי שנה עם Conditional Formatting
- Scatter: CPI vs GDP + Animation
- 2 Slicers: Year + Era
- Matrix: Era × מדד

### משימה 3: דשבורד שוק הדיור (35 נקודות)

שאלת מחקר: **"כיצד ריבית גבוהה השפיעה על שוק הדיור?"**

```
בנה דשבורד עם:
- KPI: מחיר ממוצע, נפח עסקאות, שינוי YoY
- Line: מחיר דיור + ריבית (Dual Y-Axis)
- Bar: עסקאות לפי מחוז
- Map: מחיר ממוצע לפי עיר (Filled Map)
- Slicer: מחוז, שנה, רמת מחיר
```

---

## הגשה

```
Members/YourName/Week_19/
├── macro_dashboard.pbix        ← Power BI file
├── housing_dashboard.pbix
├── dashboard_screenshot.png
├── dax_measures.md             ← תיעוד כל ה-DAX Measures
└── findings.md
```

---

**השבוע הבא:** Tableau – גרפיקה מקצועית ודשבורדים לפרסום → [שבוע 20](../Week_20_BI_Tableau/README.md)
