# משימה 1 – הכנת הסביבה

> **המשימה הראשונה שלך ב-EconLab PPE**
> אחרי שתסיים, יהיה לך מחשב מוכן לעבוד עם נתונים כמו מקצוענים.

---

## חלק א – התקנת כלים (חובה)

### 1. Python 3.11+
1. כנס ל-[python.org/downloads](https://www.python.org/downloads/)
2. הורד את הגרסה העדכנית
3. **חשוב ב-Windows:** סמן את ✅ "Add Python to PATH" לפני ההתקנה
4. אמת התקנה: פתח Terminal / CMD וכתוב:
   ```bash
   python --version
   ```
   אמור להיראות: `Python 3.11.x`

### 2. R + RStudio
1. **R עצמו:** [cran.r-project.org](https://cran.r-project.org/)
2. **RStudio (IDE):** [posit.co/download/rstudio-desktop](https://posit.co/download/rstudio-desktop/)
3. פתח RStudio ובדוק שהכל עולה

### 3. Git
1. הורד מ-[git-scm.com](https://git-scm.com/)
2. אמת התקנה:
   ```bash
   git --version
   ```

### 4. VS Code (IDE לפייתון)
1. הורד מ-[code.visualstudio.com](https://code.visualstudio.com/)
2. התקן את ה-Extension: **Python** (מאת Microsoft)
3. התקן את ה-Extension: **Jupyter**

### 5. DBeaver (לניהול SQL)
1. הורד **Community Edition** מ-[dbeaver.io](https://dbeaver.io/)
2. זה ה-IDE שלנו לכל עבודת SQL

---

## חלק ב – חיבור לגיטהאב

### 1. צור חשבון GitHub
- כנס ל-[github.com](https://github.com) ופתח חשבון אם אין לך
- שם משתמש מקצועי (FirstnameLastname)

### 2. Fork / Clone את המאגר
```bash
# שכפל את המאגר למחשב שלך
git clone https://github.com/YourOrg/econlabppe.git
cd econlabppe
```

### 3. הגדר את זהותך ב-Git
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 4. צור תיקייה אישית
```bash
# העתק את ה-template לתיקייה שלך
cp -r Members/_template Members/FirstName_LastName
```

---

## חלק ג – Python: הרץ את סקריפט ההיכרות

### 1. צור סביבה וירטואלית
```bash
cd econlabppe
python -m venv .venv

# הפעל:
source .venv/bin/activate    # Mac / Linux
.venv\Scripts\activate       # Windows
```

### 2. התקן את החבילות הבסיסיות
```bash
pip install pandas numpy matplotlib requests jupyter
```

### 3. ערוך את קובץ ה-intro שלך
פתח את `Members/YourName/intro.py` ומלא את הפרטים שלך:
- שמך
- התואר שלך
- למה הצטרפת ל-EconLab
- מה תחום הכלכלה שמעניין אותך

### 4. הרץ את הסקריפט
```bash
python Members/YourName/intro.py
```
ודא שרואים את הפלט שלך.

---

## חלק ד – הגשה

```bash
# הוסף את הקבצים שלך
git add Members/YourName/

# Commit
git commit -m "feat: Week 1 setup - YourName"

# Push
git push
```

---

## בדיקה עצמית – כל הבאים צריכים לעבוד

- [ ] `python --version` מחזיר 3.11+
- [ ] `git --version` עובד
- [ ] RStudio נפתח ורץ
- [ ] VS Code עם Python extension
- [ ] DBeaver מותקן
- [ ] תיקייה אישית ב-`Members/YourName/` קיימת ב-GitHub
- [ ] `intro.py` רץ ומדפיס את הפרטים שלך

---

## עזרה

נתקלת בבעיה? פרסם בקבוצת WhatsApp עם:
1. מה אתה מנסה לעשות
2. צילום מסך של השגיאה
3. מה כבר ניסית

---

**השבוע הבא:** Excel לניתוח כלכלי → [משימה 2](../Week_02_Excel/README.md)
