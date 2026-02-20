# שבוע 8 – Python מאפס: שפת התכנות של כלכלנים

> **רמה:** מוחלט מאפס – אין צורך בידע קודם בתכנות
> **מטרת השבוע:** ללמוד Python עד הרמה שנוכל להתחיל לעבוד עם נתונים כלכליים בשבוע הבא

---

## למה Python?

| שאלה | תשובה |
|---|---|
| **למה לא Excel?** | Excel נקרס על מיליוני שורות. Python מטפל בכל כמות. |
| **למה לא R?** | Python שפה כללית (web, automation, ML). R מיוחדת לסטטיסטיקה. נלמד גם וגם. |
| **למה דווקא Python?** | הכי נפוצה בעולם, הכי קל ללמוד, הכי טוב לניתוח נתונים. |
| **כמה זמן לוקח?** | שבועיים לבסיס. חודשים לשליטה. שנים לאמנות. מתחילים. |

---

## חלק א – היכרות ראשונה: Python כמחשבון חכם

פתח VS Code → פתח Terminal → כתוב:

```bash
python
```

נפתח **Python Interactive Shell** (REPL). נסה:

```python
>>> 2 + 2
4
>>> 1000 * 1.05 ** 10   # מה ₪1000 שווה אחרי 10 שנים ב-5%?
1628.8946267774418
>>> 100 - 72.3           # שיעור צמיחה
27.7
>>> exit()
```

כתוב `exit()` לצאת.

---

## חלק ב – קובץ Python ראשון

פתח VS Code → File → New File → שמור כ-`week08_basics.py`

### 1. הדפסה: print()

```python
# # בתחילת שורה = הערה (Python מתעלם)
# כל קוד בשורה אחרת

print("שלום, Python!")
print("צמיחת תמ''ג ישראל 2021:", 8.6, "%")
```

הרץ: לחץ ▶ (Run) ב-VS Code, או בטרמינל:
```bash
python week08_basics.py
```

### 2. משתנים (Variables)

משתנה = קופסה עם שם שמחזיקה ערך.

```python
# הגדרת משתנים
gdp_growth_2023 = 2.0
inflation_2023 = 4.2
unemployment_2023 = 3.5
country = "ישראל"
is_recession = False

# הדפסה
print(f"מדינה: {country}")
print(f"צמיחה: {gdp_growth_2023}%")
print(f"אינפלציה: {inflation_2023}%")
```

**f-string** (שורה שמתחילה ב-`f"`) = מאפשר להכניס משתנים לתוך טקסט.

### 3. טיפוסי נתונים (Data Types)

```python
# int – מספר שלם
year = 2023
num_years = 10

# float – מספר עשרוני
rate = 4.75
gdp_billions = 2100.5

# str – מחרוזת טקסט
name = "שרה כהן"
description = "כלכלנית בבנק ישראל"

# bool – True / False
is_growing = True
is_recession = False

# בדוק את הטיפוס
print(type(year))         # <class 'int'>
print(type(rate))         # <class 'float'>
print(type(name))         # <class 'str'>
print(type(is_growing))   # <class 'bool'>
```

### 4. פעולות חשבון

```python
a = 10
b = 3

print(a + b)    # חיבור: 13
print(a - b)    # חיסור: 7
print(a * b)    # כפל: 30
print(a / b)    # חילוק: 3.333...
print(a // b)   # חילוק שלם: 3
print(a % b)    # שארית: 1
print(a ** b)   # חזקה: 1000

# שימוש מתקדם
interest_rate = 0.045
principal = 100000
years = 20
future_value = principal * (1 + interest_rate) ** years
print(f"ערך עתידי: ₪{future_value:,.0f}")
# ₪{...:,.0f} = פורמט עם פסיקים ולא ספרות עשרוניות
```

---

## חלק ג – מחרוזות: עבודה עם טקסט

```python
# יצירת מחרוזת
s = "ניתוח מאקרו-כלכלי ישראל"

# פעולות בסיסיות
print(len(s))           # אורך: 24
print(s.upper())        # אותיות גדולות
print(s.lower())        # אותיות קטנות
print(s.replace("ישראל", "2024"))  # החלפה

# גישה לאותיות
print(s[0])             # אות ראשונה: נ
print(s[-1])            # אות אחרונה: ל
print(s[0:5])           # 5 אותיות ראשונות: ניתוח

# בדיקה
print("מאקרו" in s)     # True

# פיצול
parts = "2019,3.8,0.8,3.8".split(",")
print(parts)  # ['2019', '3.8', '0.8', '3.8']

# חיבור (join)
row = ",".join(["2020", "-1.9", "-0.6", "4.3"])
print(row)   # 2020,-1.9,-0.6,4.3

# f-strings מתקדמים
gdp = 2100.5
print(f"תמ''ג: {gdp:,.1f} מיליארד ₪")    # פסיקים + ספרה עשרונית
rate = 0.0425
print(f"ריבית: {rate:.2%}")               # פורמט אחוז
```

---

## חלק ד – רשימות (Lists): הכלי החשוב ביותר

```python
# יצירת רשימה
years = [2018, 2019, 2020, 2021, 2022, 2023]
gdp_growth = [4.2, 3.8, -1.9, 8.6, 6.5, 2.0]
inflation = [0.8, 0.8, -0.6, 1.5, 5.1, 4.2]

# גישה לאיברים
print(years[0])    # 2018 (מתחיל מ-0!)
print(years[-1])   # 2023 (האחרון)
print(years[1:4])  # [2019, 2020, 2021] (מ-1 עד 3, לא כולל 4)

# מידע על הרשימה
print(len(years))         # 6
print(max(gdp_growth))    # 8.6
print(min(gdp_growth))    # -1.9
print(sum(gdp_growth))    # סכום כולל

# הוסף איבר
years.append(2024)
gdp_growth.append(1.1)

# מחק איבר
years.remove(2018)       # מחיקה לפי ערך
del gdp_growth[0]        # מחיקה לפי אינדקס

# בדיקת שייכות
print(2022 in years)     # True

# מיון
sorted_growth = sorted(gdp_growth, reverse=True)  # מגדול לקטן
print(sorted_growth)
```

### פעולות על רשימות

```python
# חיבור שתי רשימות
data_2022 = [6.5, 5.1, 3.7, 3.25]
data_2023 = [2.0, 4.2, 3.5, 4.75]
combined = data_2022 + data_2023
print(combined)

# חישוב ממוצע בסיסי
def average(lst):
    return sum(lst) / len(lst)

print(f"ממוצע צמיחה: {average(gdp_growth):.2f}%")
print(f"ממוצע אינפלציה: {average(inflation):.2f}%")
```

---

## חלק ה – מילונים (Dictionaries): נתונים מובנים

מילון = קבוצת **מפתח: ערך**. בדיוק כמו מילון אמיתי (מילה: הגדרה).

```python
# יצירת מילון
israel_2023 = {
    "year": 2023,
    "gdp_growth": 2.0,
    "inflation": 4.2,
    "unemployment": 3.5,
    "interest_rate": 4.75
}

# גישה לערכים
print(israel_2023["gdp_growth"])   # 2.0
print(israel_2023.get("inflation", 0))  # 4.2 (עם ברירת מחדל 0)

# שינוי ערך
israel_2023["unemployment"] = 3.6

# הוספת מפתח חדש
israel_2023["exports_bn"] = 75.4

# בדיקה
print("gdp_growth" in israel_2023)    # True

# איטרציה
for key, value in israel_2023.items():
    print(f"{key}: {value}")

# כל המפתחות
print(list(israel_2023.keys()))

# כל הערכים
print(list(israel_2023.values()))
```

### רשימה של מילונים – מבנה כלכלי טיפוסי

```python
# כך מייצגים טבלת נתונים
macro_data = [
    {"year": 2020, "gdp": -1.9, "inflation": -0.6},
    {"year": 2021, "gdp": 8.6,  "inflation": 1.5},
    {"year": 2022, "gdp": 6.5,  "inflation": 5.1},
    {"year": 2023, "gdp": 2.0,  "inflation": 4.2},
]

# גישה לשורה ספציפית
print(macro_data[2]["inflation"])  # 5.1

# ניתוח
avg_gdp = sum(row["gdp"] for row in macro_data) / len(macro_data)
print(f"ממוצע צמיחה: {avg_gdp:.2f}%")
```

---

## חלק ו – לולאות (Loops): חוזרים על פעולות

### for loop – איטרציה על רשימה

```python
years = [2019, 2020, 2021, 2022, 2023]
gdp_growth = [3.8, -1.9, 8.6, 6.5, 2.0]

# לולאה פשוטה
for year in years:
    print(f"שנה: {year}")

# לולאה עם אינדקס (enumerate)
for i, year in enumerate(years):
    growth = gdp_growth[i]
    status = "צמיחה" if growth > 0 else "מיתון"
    print(f"{year}: {growth}% – {status}")

# zip – שתי רשימות ביחד
for year, growth in zip(years, gdp_growth):
    print(f"{year}: {growth}%")
```

### range() – מספרים ברצף

```python
# range(start, stop, step)
for i in range(2015, 2025):
    print(i)            # 2015, 2016, ..., 2024

for i in range(0, 100, 10):
    print(i)            # 0, 10, 20, ..., 90
```

### while loop – חוזר כל עוד תנאי מתקיים

```python
# סימולציית ריבית דריבית
balance = 100000  # ₪100,000
rate = 0.05       # 5% בשנה
years = 0

while balance < 200000:
    balance *= 1 + rate
    years += 1
    print(f"שנה {years}: ₪{balance:,.0f}")

print(f"\nנדרשו {years} שנים להכפיל את הכסף")
```

### List Comprehension – לולאה בשורה אחת

```python
# ממיר שיעורי צמיחה לקטגוריות
gdp_rates = [3.8, -1.9, 8.6, 6.5, 2.0, 1.1]

categories = ["צמיחה" if g > 0 else "מיתון" for g in gdp_rates]
print(categories)
# ['צמיחה', 'מיתון', 'צמיחה', 'צמיחה', 'צמיחה', 'צמיחה']

# ריבית ריאלית לכל שנה
inflation = [0.8, -0.6, 1.5, 5.1, 4.2, 3.5]
interest  = [0.25, 0.1, 0.1, 3.25, 4.75, 4.5]
real_rates = [r - i for r, i in zip(interest, inflation)]
print(real_rates)
```

---

## חלק ז – תנאים (Conditionals)

```python
gdp_growth = 2.0
inflation = 4.2

# if בסיסי
if gdp_growth > 0:
    print("כלכלה צומחת")

# if-else
if gdp_growth > 3:
    print("צמיחה גבוהה")
else:
    print("צמיחה מתונה")

# if-elif-else
if gdp_growth < 0:
    status = "מיתון"
elif gdp_growth < 2:
    status = "צמיחה איטית"
elif gdp_growth < 4:
    status = "צמיחה נורמלית"
else:
    status = "צמיחה גבוהה"

print(f"מצב כלכלי: {status}")

# תנאים מרובים
if gdp_growth > 0 and inflation > 3:
    print("סטגפלציה: צמיחה נמוכה + אינפלציה גבוהה – בעיה!")

if gdp_growth < 0 or inflation > 8:
    print("מצב חירום כלכלי!")

# Ternary (תנאי בשורה אחת)
label = "חיובי" if gdp_growth > 0 else "שלילי"
```

---

## חלק ח – פונקציות (Functions)

פונקציה = קוד שניתן שם, שאפשר לקרוא שוב ושוב.

```python
# פונקציה בסיסית
def calculate_real_rate(nominal_rate, inflation):
    """
    מחשבת ריבית ריאלית לפי נוסחת פישר הפשוטה.

    Args:
        nominal_rate: ריבית נומינלית (%)
        inflation: שיעור אינפלציה (%)

    Returns:
        ריבית ריאלית (%)
    """
    return nominal_rate - inflation

# קריאה לפונקציה
real_2022 = calculate_real_rate(3.25, 5.1)
real_2023 = calculate_real_rate(4.75, 4.2)
print(f"ריבית ריאלית 2022: {real_2022:.2f}%")
print(f"ריבית ריאלית 2023: {real_2023:.2f}%")
```

### פרמטרים עם ברירת מחדל

```python
def compound_interest(principal, rate, years, compound=12):
    """
    מחשבת ערך עתידי עם ריבית דריבית.
    compound = כמה פעמים בשנה (ברירת מחדל: חודשי = 12)
    """
    return principal * (1 + rate / compound) ** (compound * years)

print(f"ריבית שנתית: ₪{compound_interest(100000, 0.05, 10, 1):,.0f}")
print(f"ריבית חודשית: ₪{compound_interest(100000, 0.05, 10):,.0f}")
print(f"ריבית יומית: ₪{compound_interest(100000, 0.05, 10, 365):,.0f}")
```

### פונקציה שמחזירה מספר ערכים

```python
def analyze_series(data_list):
    """מנתחת סדרת נתונים ומחזירה סטטיסטיקה בסיסית."""
    n = len(data_list)
    mean = sum(data_list) / n
    sorted_data = sorted(data_list)
    max_val = sorted_data[-1]
    min_val = sorted_data[0]
    data_range = max_val - min_val

    return mean, max_val, min_val, data_range

gdp_series = [4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1]
mean, high, low, span = analyze_series(gdp_series)
print(f"ממוצע: {mean:.2f}%")
print(f"שיא: {high}%  שפל: {low}%  טווח: {span:.1f}%")
```

---

## חלק ט – קריאה וכתיבה לקבצים

```python
# כתיבה לקובץ
data = [
    "year,gdp_growth,inflation",
    "2020,-1.9,-0.6",
    "2021,8.6,1.5",
    "2022,6.5,5.1",
    "2023,2.0,4.2",
]

with open("macro_data.csv", "w", encoding="utf-8") as f:
    for line in data:
        f.write(line + "\n")

print("קובץ נכתב!")

# קריאה מקובץ
with open("macro_data.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"מספר שורות: {len(lines)}")

# עיבוד הנתונים
header = lines[0].strip().split(",")  # ['year', 'gdp_growth', 'inflation']
rows = []
for line in lines[1:]:
    values = line.strip().split(",")
    row = {
        "year": int(values[0]),
        "gdp_growth": float(values[1]),
        "inflation": float(values[2])
    }
    rows.append(row)

for row in rows:
    print(row)
```

---

## חלק י – מודולים: שימוש בקוד מוכן

Python מגיע עם ספריות מובנות. נשתמש בכמה:

```python
import math
import statistics
import datetime

# math
print(math.sqrt(16))       # 4.0
print(math.log(100, 10))   # 2.0
print(math.pi)             # 3.14159...

# statistics
gdp_growth = [4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1]
print(statistics.mean(gdp_growth))    # ממוצע
print(statistics.median(gdp_growth))  # חציון
print(statistics.stdev(gdp_growth))   # סטיית תקן

# datetime
today = datetime.date.today()
print(f"היום: {today}")
print(f"שנה: {today.year}")

# datetime לניתוח כלכלי
report_date = datetime.date(2024, 1, 15)
print(f"דוח: {report_date.strftime('%d/%m/%Y')}")
```

---

## משימות השבוע

### משימה 1: פונקציות כלכליות (30 נקודות)

כתוב קובץ `economic_functions.py` עם 5 פונקציות:

```python
def gdp_growth_rate(gdp_current, gdp_previous):
    """מחשבת שיעור צמיחה בין שתי תקופות."""
    pass  # → החלף בקוד אמיתי

def real_interest_rate(nominal, inflation):
    """נוסחת פישר: ריבית ריאלית."""
    pass

def future_value(principal, annual_rate, years):
    """ערך עתידי עם ריבית דריבית שנתית."""
    pass

def classify_inflation(rate):
    """מסווגת את רמת האינפלציה."""
    # דפלציה (<0) / יציבות (0-2%) / מתונה (2-5%) / גבוהה (>5%)
    pass

def moving_average(data, window=3):
    """מחשבת ממוצע נע בחלון נתון."""
    pass
```

**בדוק:**
```python
print(gdp_growth_rate(2100, 1980))   # → 6.06%
print(real_interest_rate(4.75, 4.2)) # → 0.55%
print(future_value(100000, 0.05, 10)) # → ₪162,889
print(classify_inflation(5.1))        # → גבוהה
print(moving_average([3.8, -1.9, 8.6, 6.5, 2.0]))  # → [3.5, 4.4, 5.7]
```

### משימה 2: ניתוח סדרה עתית (40 נקודות)

כתוב `time_series_analysis.py` שעושה:

1. מגדיר רשימת נתונים: צמיחה + אינפלציה + ריבית לשנים 2015-2024
2. מחשב לכל שנה: ריבית ריאלית + סיווג מצב כלכלי
3. מוצא: שנת הצמיחה הגבוהה, שנת האינפלציה הגבוהה, שנות מיתון
4. מדפיס טבלה מסודרת:

```
שנה | צמיחה | אינפלציה | ריבית | ריבית ריאלית | מצב
-----|--------|---------|-------|-------------|-----
2015 |  2.5%  |  -0.6%  | 0.1%  |    0.7%    | צמיחה מתונה
...
```

### משימה 3: סימולציה כלכלית (30 נקודות)

כתוב `simulation.py`:

**חישוב השפעת הלם מדיניות ריבית:**
- נתון: כלכלה עם צמיחה בסיסית של 3%, אינפלציה של 2%
- בנק מרכזי מעלה ריבית ב-0.25% בכל רבעון (מ-0.1% עד 4.75%)
- הנח: כל 1% עלייה בריבית → ירידה של 0.4% בצמיחה
- הנח: כל 1% עלייה בריבית → ירידה של 0.3% באינפלציה אחרי שנה

הדמה 16 רבעונים (4 שנים) ועקוב אחרי:
- ריבית (קלט)
- אינפלציה (עם השפעה מתמשכת)
- צמיחה (עם השפעה מתמשכת)

הדפס תוצאות לכל רבעון.

---

## הגשה

```
Members/YourName/Week_08/
├── economic_functions.py
├── time_series_analysis.py
└── simulation.py
```

---

## קיצורי VS Code שחוסכים זמן

| קיצור | פעולה |
|---|---|
| **F5** | הרץ סקריפט |
| **Ctrl+/** | הפעל/כבה הערה |
| **Tab** | הזחה (indent) |
| **Shift+Tab** | ביטול הזחה |
| **Ctrl+D** | בחר עוד מופע של אותו טקסט |
| **Alt+↑/↓** | הזז שורה למעלה/למטה |
| **Ctrl+Shift+K** | מחק שורה |

---

**השבוע הבא:** Pandas – ניתוח נתונים עם כלי ה-"Excel של Python" → [שבוע 9](../Week_09_Pandas_Basics/README.md)
