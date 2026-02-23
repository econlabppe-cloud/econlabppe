# הנחיות תרומה – EconLab PPE

## כללי זהב

1. **אל תעלה קבצי נתונים ל-Git.**
   קבצי `*.csv`, `*.xlsx`, `*.parquet` וכדומה מוחרגים ב-`.gitignore`.
   יש להעלות נתונים **אך ורק** לתיקיית Google Drive המשותפת.

2. **שמות קבצים ותיקיות – באנגלית בלבד (Snake Case).**
   דוגמה נכונה: `housing_price_index.py`, `Projects/Housing_Market/`.
   דוגמה שגויה: `ניתוח דיור.ipynb`.

3. **תוכן קבצי Markdown – בעברית.**
   הסברים, תיעוד ותיאורי פרויקטים נכתבים בעברית לנוחות הקריאה.

4. **סביבה וירטואלית – לא ב-Git.**
   יש להוסיף `.venv/`, `env/` ל-`.gitignore` ולא להעלות אותן.

5. **קבצי `.env` – לעולם לא ב-Git.**
   מפתחות API, סיסמאות וכתובות שרת שמורים אך ורק בקובץ `.env` מקומי.

---

## תהליך עבודה (Git Flow מומלץ)

```
main          ← ענף יציב בלבד
  └─ dev      ← אינטגרציה
       └─ feature/<your-name>/<topic>   ← עבודה שוטפת
```

1. צור ענף חדש מ-`dev`: `git checkout -b feature/YourName/topic`
2. עבוד, בצע Commit עם הודעות ברורות באנגלית.
3. פתח Pull Request ל-`dev` וציין מה עשית ולמה.
4. לאחר אישור – מיזוג (Merge).

---

## סגנון קוד

- Python: [PEP 8](https://pep8.org/) + Black formatter.
- SQL: מילים שמורות באותיות גדולות (`SELECT`, `FROM`, `WHERE`).
- Notebooks: אפס פלטים לפני Commit (`Kernel → Restart & Clear Output`).

---

*עדכון אחרון: נוצר על-ידי `setup_repo.py`*
