# Members – תיקי עבודות אישיים

## מה זה תיק עבודות (Portfolio)?

התיקייה `Members/YourName/` היא **תיק העבודות שלך**.
בסוף המסלול תוכל להציג אותה בראיון עבודה, לשלוח כ-GitHub link, ולהגיד:
> "הנה 10 שבועות של ניתוח כלכלי – קוד Python, R, SQL, דשבורד ומודל DSGE."

**זה מה שמבדיל אותך מכל שאר בוגרי הכלכלה.**

---

## חברי המעבדה

| שם | תיקייה | שבוע נוכחי |
|---|---|---|
| יהודה סעדיה | `Members/yehuda_saadya/` | מייסד |
| *(הצטרף!)* | `Members/YourName/` | - |

---

## איך מתחילים?

### שלב 1: העתק את ה-template
```bash
# שכפל את המאגר (אם עוד לא)
git clone https://github.com/YourOrg/econlabppe.git
cd econlabppe

# העתק את ה-template לתיקייה שלך
cp -r Members/_template Members/FirstName_LastName
```

> שם התיקייה: **אנגלית בלבד**, `FirstName_LastName`
> למשל: `Members/Noa_Cohen`, `Members/David_Levi`

### שלב 2: ערוך את קבצי הפרופיל
- `Members/YourName/README.md` – ה-"כרטיס ביקור" שלך
- `Members/YourName/intro.py` – סקריפט פייתון של היכרות ראשונה

### שלב 3: Push ל-GitHub
```bash
git add Members/YourName/
git commit -m "feat: add YourName to EconLab PPE"
git push
```

---

## מבנה מומלץ לתיקייה אישית

```
Members/YourName/
├── README.md           ← מי אתה ומה עשית (עדכן כל שבוע!)
├── intro.py            ← סקריפט היכרות (משימה 1)
│
├── Week_01_Setup/      ← תיעוד ההתקנה
├── Week_02_Excel/      ← ממצאי ניתוח + summary.md
├── Week_03_SQL/        ← queries.sql + sql_analysis.py
├── Week_04_Pandas/     ← macro_analysis.ipynb
├── Week_05_APIs/       ← api_data_fetch.ipynb
├── Week_06_R/          ← r_basics.R + גרפים
├── Week_07_Econ/       ← econometrics.R + results.md
├── Week_08_Viz/        ← גרפים + HTML אינטראקטיבי
├── Week_09_BI/         ← PDF של דשבורד / קישור Tableau
└── Week_10_DSGE/       ← dsge_analysis.R + irf_*.png
```

---

## כללים

1. **שם תיקייה:** אנגלית, `FirstName_LastName` (Snake_Case)
2. **אל תעלה נתונים:** CSV/Excel → Google Drive בלבד
3. **תנקה Notebooks לפני Push:** `Kernel → Restart & Clear Output`
4. **קובץ `.env`:** לעולם לא ב-Git (מפתחות API)
5. **עדכן את README.md שלך** לאחר כל משימה שמסיים

---

## עצות לתיק עבודות מוצלח

- כתוב **תגלית אחת** בכל `summary.md` ("גיליתי ש...")
- הוסף **גרף אחד** שאתה גאה בו לכל שבוע
- כתוב את ה-README שלך כאילו מישהו זר יקרא אותו
- התמקד ב**כלכלה**, לא רק בקוד

---
