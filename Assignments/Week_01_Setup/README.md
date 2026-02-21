# שבוע 1 – הכנת הסביבה: בניית מחשב של כלכלן נתונים

> **המשימה הראשונה שלך ב-EconLab PPE**
> בסוף השבוע הזה יהיה לך סביבת עבודה מקצועית שמוכנה לכל דבר שנעשה במסלול.
> אל תדלג על שום שלב – הבסיס הזה יחסוך לך שעות של כאבי ראש בהמשך.

---

## למה בכלל צריך את כל הכלים האלה?

לפני שמתקינים, כדאי להבין **מה כל כלי עושה** ולמה כלכלן צריך אותו:

| כלי | מה זה | למה כלכלן צריך |
|---|---|---|
| **Python** | שפת תכנות כללית | ניתוח נתונים, אוטומציה, API, מודלים |
| **R** | שפת סטטיסטיקה | אקונומטריקה, מודלים, גרפים אקדמיים |
| **Git** | מערכת ניהול גרסאות | לשמור קוד, לשתף, לא לאבד עבודה |
| **GitHub** | פלטפורמת שיתוף קוד | Portfolio מקצועי, שיתוף פעולה |
| **VS Code** | עורך קוד | כותבים ומריצים Python |
| **RStudio** | סביבת R | כותבים ומריצים R |
| **DBeaver** | ניהול SQL | מתחברים לבסיסי נתונים |
| **Jupyter** | Notebooks אינטראקטיביים | ניתוח + הסבר + גרפים ביחד |

---

## חלק א – התקנת כלים

### 1. Python 3.11+

Python היא שפת התכנות הנפוצה ביותר לניתוח נתונים בעולם.

**Windows:**
1. כנס ל-[python.org/downloads](https://www.python.org/downloads/)
2. לחץ על "Download Python 3.11.x" (הגרסה הכתומה הגדולה)
3. **חשוב מאוד:** לפני שלוחצים Install, סמן ✅ **"Add Python to PATH"**
4. לחץ "Install Now"

**Mac:**
```bash
# התקן Homebrew קודם אם אין לך:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# התקן Python:
brew install python@3.11
```

**בדיקה:** פתח Terminal / CMD וכתוב:
```bash
python --version
# אמור לראות: Python 3.11.x

python -c "print('Python עובד!')"
# אמור לראות: Python עובד!
```

> **שגיאה נפוצה:** אם רואים `'python' is not recognized` ב-Windows – לא סימנת "Add to PATH". הסר את ההתקנה וחזור על התהליך.

---

### 2. R + RStudio

R נבנתה בשנות ה-90 ע"י סטטיסטיקאים, ועד היום היא הסטנדרט לאקונומטריקה.

**שלב א – R עצמה (מנוע):**
1. כנס ל-[cran.r-project.org](https://cran.r-project.org/)
2. בחר לפי מערכת ההפעלה שלך (Windows / Mac / Linux)
3. לחץ "install R for the first time"
4. הורד והתקן

**שלב ב – RStudio (ממשק):**
1. כנס ל-[posit.co/download/rstudio-desktop](https://posit.co/download/rstudio-desktop/)
2. הורד "RStudio Desktop – Free"
3. התקן

**בדיקה:** פתח RStudio ובחלונית Console (למטה) כתוב:
```r
print("R עובד!")
# אמור לראות: [1] "R עובד!"

2 + 2
# אמור לראות: [1] 4
```

---

### 3. Git

Git מאפשר לך לשמור כל גרסה של הקוד שלך ולשתף עם אחרים.

**Windows:** הורד מ-[git-scm.com](https://git-scm.com/) → הפעל את ה-installer עם הגדרות ברירת מחדל.

**Mac:** כבר מותקן! בדוק:
```bash
git --version
```

**הגדרה ראשונית** (חובה לכולם):
```bash
# הגדר את השם שלך (כפי שיופיע ב-commits)
git config --global user.name "Firstname Lastname"

# הגדר את האימייל שלך (אותו אימייל כמו ב-GitHub)
git config --global user.email "your@email.com"

# בדוק שנשמר:
git config --list
```

---

### 4. VS Code – עורך קוד לפייתון

**התקנה:**
1. הורד מ-[code.visualstudio.com](https://code.visualstudio.com/)
2. התקן

**Extensions חובה:**
פתח VS Code → לחץ על אייקון ה-Extensions (Ctrl+Shift+X):

- **Python** (מאת Microsoft) – הכרחי
- **Jupyter** (מאת Microsoft) – לעבוד עם notebooks
- **GitLens** – לראות היסטוריית שינויים

**בדיקה:** לחץ Ctrl+Shift+P → כתוב "Select Interpreter" → בחר את ה-Python שהתקנת.

---

### 5. DBeaver – ניהול בסיסי נתונים

**התקנה:**
1. כנס ל-[dbeaver.io](https://dbeaver.io/)
2. הורד **Community Edition** (חינמי)
3. התקן

DBeaver מאפשר לחבר ל-SQLite, PostgreSQL, MySQL, ועוד – ממשק אחד לכל כלי SQL.

---

## חלק ב – חיבור לגיטהאב

### מה זה GitHub ולמה חשוב?

GitHub הוא "ענן לקוד". במקום שקובץ Excel יושב על שולחן העבודה שלך:
- הקוד שלך מאוחסן בענן ✅
- אתה יכול לעבוד מכל מחשב ✅
- גורם גיוס יכול לראות את הפרויקטים שלך ✅
- לא מאבדים עבודה אם המחשב קורס ✅

### שלב 1 – פתח חשבון GitHub
- כנס ל-[github.com](https://github.com)
- לחץ "Sign Up"
- **שם משתמש:** השתמש בשם אמיתי מקצועי (FirstnameLastname)
- **אימייל:** אמיתי שאתה משתמש בו

### שלב 2 – Clone את המאגר שלנו

```bash
# שכפל את המאגר למחשב שלך
git clone https://github.com/YourOrg/econlabppe.git

# כנס לתיקייה
cd econlabppe

# ראה מה יש שם
ls
```

**מה קרה?** יצרת עותק מקומי של כל הקוד מהענן. מעכשיו אתה יכול לעבוד, ואחר כך "לדחוף" את השינויים חזרה.

### שלב 3 – הבנת מחזור ה-Git

```bash
# 1. ראה מה שינית
git status

# 2. הוסף קבצים ל"תיבת ההכנה"
git add filename.py

# 3. שמור snapshot עם הסבר
git commit -m "הוספתי ניתוח ראשון"

# 4. שלח לענן (GitHub)
git push
```

### שלב 4 – צור תיקייה אישית

```bash
# העתק את ה-template לתיקייה בשמך
cp -r Members/_template Members/FirstName_LastName

# ראה מה קיבלת
ls Members/FirstName_LastName/
```

---

## חלק ג – Python: הרץ את סקריפט ההיכרות

### מה זה סביבה וירטואלית ולמה צריך?

דמיין שלכל פרויקט יש "חדר" משלו עם החבילות שלו. אם פרויקט א' צריך pandas 1.5 ופרויקט ב' צריך pandas 2.0 – הם לא "מריבים". זה מה שסביבה וירטואלית עושה.

```bash
# צור סביבה וירטואלית
cd econlabppe
python -m venv .venv

# הפעל אותה:
source .venv/bin/activate    # Mac / Linux
.venv\Scripts\activate       # Windows

# תראה שב-Terminal מופיע (.venv) לפני שורת הפקודה
# (.venv) $
```

### התקנת חבילות

```bash
# חבילות הבסיס שנשתמש בהן כל המסלול
pip install pandas numpy matplotlib requests jupyter openpyxl

# בדוק שהותקן:
pip list
```

**מה כל חבילה עושה:**
- `pandas` – עבודה עם טבלאות נתונים
- `numpy` – חישובים מתמטיים
- `matplotlib` – גרפים
- `requests` – גישה ל-APIs
- `jupyter` – Notebooks
- `openpyxl` – קריאת/כתיבת Excel

### ערוך את קובץ ה-intro שלך

פתח `Members/YourName/intro.py` ב-VS Code ומלא:

```python
# intro.py – ברוך הבא ל-EconLab!

name = "שמך המלא"
degree = "כלכלה ממשל, שנה ב"
why_econlab = "רוצה ללמוד לעבוד עם נתונים כלכליים אמיתיים"
interest = "שוק הדיור בישראל"

print("=" * 40)
print(f"שם: {name}")
print(f"תואר: {degree}")
print(f"למה EconLab: {why_econlab}")
print(f"תחום עניין: {interest}")
print("=" * 40)
print("הסביבה עובדת! מוכן להתחיל.")
```

### הרץ את הסקריפט

```bash
python Members/YourName/intro.py
```

צפה שתראה את הפלט שלך מודפס.

---

## חלק ד – Jupyter Notebook ראשון

Jupyter Notebooks הם כמו מסמכי Word שאפשר להריץ בתוכם קוד. נשתמש בהם כל המסלול.

```bash
# הפעל Jupyter
jupyter notebook
```

נפתח דפדפן. לחץ **New → Python 3**.

**נסה את זה בתא הראשון:**
```python
# תא 1 – חישוב פשוט
gdp_2023 = 2100  # מיליארד ₪ (בערך)
gdp_2022 = 1980  # מיליארד ₪
growth_rate = (gdp_2023 - gdp_2022) / gdp_2022 * 100
print(f"צמיחת תמ''ג 2023: {growth_rate:.1f}%")
```

לחץ Shift+Enter להריץ. תראה את הפלט מתחת לתא.

**תא 2:**
```python
import matplotlib.pyplot as plt

years = [2019, 2020, 2021, 2022, 2023]
gdp_growth = [3.8, -1.9, 8.6, 6.5, 2.0]

plt.figure(figsize=(10, 5))
plt.plot(years, gdp_growth, marker='o', linewidth=2, color='royalblue')
plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
plt.title("צמיחת תמ''ג ישראל 2019-2023", fontsize=14)
plt.xlabel("שנה")
plt.ylabel("צמיחה (%)")
plt.grid(True, alpha=0.3)
plt.show()
```

תראה גרף! שמור את ה-Notebook כ-`Members/YourName/Week_01/first_notebook.ipynb`.

---

## חלק ה – הגשה

```bash
# הוסף את הקבצים שלך
git add Members/YourName/

# Commit עם הסבר ברור
git commit -m "feat: Week 1 setup complete - YourName"

# Push לענן
git push
```

**לכנס ל-GitHub ולוודא שהתיקייה שלך מופיעה!**

---

## בדיקה עצמית – כל הבאים חייבים לעבוד

- [ ] `python --version` מחזיר 3.11+
- [ ] `git --version` עובד
- [ ] `git config --list` מציג את השם והאימייל שלך
- [ ] RStudio נפתח, מריץ `2+2` ומחזיר 4
- [ ] VS Code עם Python + Jupyter Extensions
- [ ] DBeaver מותקן ונפתח
- [ ] `(.venv)` מופיע ב-Terminal
- [ ] `intro.py` רץ ומדפיס את הפרטים שלך
- [ ] Jupyter Notebook ראשון עם גרף
- [ ] הכל מועלה ל-GitHub

---

## מושגי יסוד לסיכום

| מושג | הגדרה |
|---|---|
| **Repository** | תיקייה של קוד שמנוהלת ע"י Git |
| **Commit** | snapshot של הקוד עם הסבר |
| **Push** | שליחת הקוד מהמחשב לענן |
| **Clone** | הורדת Repository מהענן למחשב |
| **Virtual Environment** | סביבה מבודדת עם חבילות ספציפיות |

---

## עזרה

נתקלת בבעיה? פרסם בקבוצת WhatsApp עם:
1. מה ניסית לעשות
2. צילום מסך של השגיאה
3. מה כבר ניסית

---

**השבוע הבא:** Excel מאפס – הכלי שכל כלכלן מתחיל בו → [שבוע 2](../Week_02_Excel_Basics/README.md)
