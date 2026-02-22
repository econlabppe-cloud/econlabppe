# משימה 4 – Python + Pandas: ניתוח נתונים כלכליים
### 🎥 סרטון הדרכה מרכזי
צפו בסרטון הבא שמכסה את ליבת החומר הטכני של שבוע זה:
{{< video https://www.youtube.com/watch?v=MeUPugsWmZA >}}


> Pandas הוא ה-"Excel של Python" – רק הרבה יותר חזק ומהיר.
> אחרי המשימה הזו תוכל לנתח כל CSV/Excel תוך דקות.

---

## הכנה

```bash
# ודא שהסביבה הוירטואלית פעילה
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows

# התקן חבילות
pip install pandas numpy matplotlib openpyxl jupyter
```

פתח Jupyter Notebook:
```bash
jupyter notebook
```
צור Notebook חדש ב-`Members/YourName/Week_04/`

---

## חלק א – טעינת נתונים

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# אפשרות 1: קרא CSV (מהורדה ידנית)
df = pd.read_csv("israel_cpi.csv", encoding="utf-8")

# אפשרות 2: צור נתונים ישירות (לתרגול)
data = {
    "year": range(2010, 2025),
    "gdp_growth": [5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                   -1.9, 8.6, 6.5, 2.0, 1.1],
    "inflation":  [2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                   -0.6, 1.5, 5.1, 4.2, 3.5],
    "unemployment": [6.6, 5.6, 6.9, 6.3, 6.0, 5.3, 4.8, 4.3, 4.0, 3.8,
                     4.3, 5.0, 3.7, 3.5, 4.2],
}
df = pd.DataFrame(data)

print(df.head())
print(df.dtypes)
print(df.describe())
```

---

## חלק ב – ניקוי ועיבוד

### סינון
```python
# שנים עם אינפלציה חיובית
positive_inflation = df[df["inflation"] > 0]
print(f"מספר שנים עם אינפלציה חיובית: {len(positive_inflation)}")

# עידן הריבית הגבוהה
high_rate_years = df[df["year"] >= 2022]
```

### עמודות חדשות
```python
# מחוון Phillips: קשר בין אינפלציה לאבטלה
df["phillips_gap"] = df["inflation"] - df["unemployment"]

# קבוצת עשור
df["decade"] = df["year"].apply(lambda y: "2010s" if y < 2020 else "2020s")
```

### סטטיסטיקה לפי קבוצה
```python
# ממוצעים לפי עשור
summary = df.groupby("decade").agg(
    avg_growth=("gdp_growth", "mean"),
    avg_inflation=("inflation", "mean"),
    avg_unemployment=("unemployment", "mean")
).round(2)

print(summary)
```

---

## חלק ג – גרפים ראשוניים

### גרף 1: צמיחת תמ"ג לאורך זמן
```python
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["year"], df["gdp_growth"], marker="o", color="steelblue", linewidth=2)
ax.axhline(0, color="red", linestyle="--", alpha=0.5, label="אפס")
ax.axvspan(2020, 2020.9, alpha=0.2, color="orange", label="COVID-19")
ax.set_title("צמיחת תמ\"ג ישראל 2010–2024", fontsize=14)
ax.set_xlabel("שנה")
ax.set_ylabel("% שינוי שנתי")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("gdp_growth.png", dpi=150)
plt.show()
```

### גרף 2: עקומת Phillips
```python
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(df["unemployment"], df["inflation"],
                     c=df["year"], cmap="viridis", s=80)
plt.colorbar(scatter, label="שנה")

# תוויות לשנים מעניינות
for _, row in df[df["year"].isin([2020, 2022, 2024])].iterrows():
    ax.annotate(str(int(row["year"])),
                (row["unemployment"], row["inflation"]),
                textcoords="offset points", xytext=(5, 5))

ax.set_xlabel("אבטלה %")
ax.set_ylabel("אינפלציה %")
ax.set_title("עקומת Phillips – ישראל 2010–2024")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("phillips_curve.png", dpi=150)
plt.show()
```

---

## חלק ד – שאלות לניתוח

ענה בתא Markdown בתוך ה-Notebook:

1. **מה קרה בשנת 2021?** (צמיחה + אינפלציה) – הסבר כלכלי
2. **האם עקומת Phillips תקפה לישראל?** מה הנתונים מראים?
3. **מה ההבדל הגדול ביותר** בין עשור 2010–2019 ל-2020–2024?

---

## הגשה

תיקייה: `Members/YourName/Week_04/`

**מה להגיש:**
- [ ] `macro_analysis.ipynb` – Jupyter Notebook המלא
  - קוד + גרפים + תשובות בעברית
- [ ] `gdp_growth.png` + `phillips_curve.png`

> ⚠️ לפני Push: `Kernel → Restart & Clear Output` (ניקוי output מה-Notebook)

---

**השבוע הבא:** APIs – גישה לנתונים ישירות מהמקור → [משימה 5](../Week_05_APIs/README.md)
