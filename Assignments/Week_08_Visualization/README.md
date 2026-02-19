# משימה 8 – ויזואליזציה: סיפור עם נתונים

> גרף טוב אחד שווה אלף מילים.
> קובעי מדיניות לא קוראים קוד – הם רואים גרפים.

---

## עקרונות ויזואליזציה כלכלית

1. **כותרת ברורה** – מה הגרף מראה ולמי
2. **תוויות צירים** – תמיד עם יחידות (%, ₪, מיליארד)
3. **מקור הנתונים** – תמיד בתחתית
4. **פשטות** – פחות זה יותר (הסר gridlines מיותרים, צבעים מיותרים)
5. **הדגשה** – צבע שונה לנקודה החשובה

---

## חלק א – Plotly: גרפים אינטראקטיביים (Python)

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.DataFrame({
    "year":         list(range(2010, 2025)),
    "gdp_growth":   [5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                     -1.9, 8.6, 6.5, 2.0, 1.1],
    "inflation":    [2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                     -0.6, 1.5, 5.1, 4.2, 3.5],
    "interest_rate":[1.5, 2.5, 2.25, 1.5, 0.25, 0.1, 0.1, 0.1, 0.1, 0.25,
                     0.1, 0.1, 3.25, 4.75, 4.5],
})

# ---- גרף 1: 3 מחווני מאקרו על ציר משותף ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["year"], y=df["gdp_growth"],
    name="צמיחת תמ\"ג", line=dict(color="steelblue", width=2)
))
fig.add_trace(go.Scatter(
    x=df["year"], y=df["inflation"],
    name="אינפלציה", line=dict(color="tomato", width=2)
))
fig.add_trace(go.Scatter(
    x=df["year"], y=df["interest_rate"],
    name="ריבית בנק ישראל", line=dict(color="green", width=2, dash="dash")
))

fig.add_vrect(x0=2020, x1=2021, fillcolor="orange",
              opacity=0.1, annotation_text="COVID-19")
fig.add_hline(y=0, line_dash="dot", line_color="gray")

fig.update_layout(
    title="מחווני מאקרו עיקריים – ישראל 2010–2024",
    xaxis_title="שנה",
    yaxis_title="אחוזים (%)",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", y=-0.2)
)

fig.write_html("macro_dashboard.html")
fig.show()
```

---

## חלק ב – Matplotlib: גרף לפרסום

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("דוח מאקרו-כלכלי – ישראל 2010–2024",
             fontsize=16, fontweight="bold", y=1.02)

# ---- Panel 1: GDP Growth ----
ax1 = axes[0, 0]
colors = ["steelblue" if g > 0 else "tomato" for g in df["gdp_growth"]]
ax1.bar(df["year"], df["gdp_growth"], color=colors, alpha=0.8)
ax1.axhline(0, color="black", linewidth=0.8)
ax1.set_title("צמיחת תמ\"ג (%)")
ax1.set_ylabel("%")

# ---- Panel 2: Inflation ----
ax2 = axes[0, 1]
ax2.plot(df["year"], df["inflation"], "o-", color="tomato", linewidth=2)
ax2.axhline(1, color="gray", linestyle="--", alpha=0.5, label="יעד 1%")
ax2.axhline(3, color="gray", linestyle="--", alpha=0.5, label="יעד 3%")
ax2.fill_between(df["year"], 1, 3, alpha=0.1, color="green", label="טווח יעד")
ax2.set_title("אינפלציה (%)")
ax2.legend(fontsize=8)

# ---- Panel 3: Interest Rate ----
ax3 = axes[1, 0]
ax3.step(df["year"], df["interest_rate"], where="post",
         color="green", linewidth=2)
ax3.fill_between(df["year"], df["interest_rate"],
                 step="post", alpha=0.2, color="green")
ax3.set_title("ריבית בנק ישראל (%)")

# ---- Panel 4: Unemployment ----
unemployment = [6.6, 5.6, 6.9, 6.3, 6.0, 5.3, 4.8, 4.3, 4.0, 3.8,
                4.3, 5.0, 3.7, 3.5, 4.2]
ax4 = axes[1, 1]
ax4.plot(df["year"], unemployment, "s-", color="purple", linewidth=2)
ax4.set_title("אבטלה (%)")

for ax in axes.flat:
    ax.grid(alpha=0.2)
    ax.set_xlabel("שנה")

plt.tight_layout()
fig.text(0.5, -0.02, "מקור: בנק ישראל, הלמ\"ס | עיבוד: EconLab PPE",
         ha="center", fontsize=9, color="gray")
plt.savefig("macro_report.png", dpi=200, bbox_inches="tight")
plt.show()
```

---

## חלק ג – ggplot2 (R): גרף לדוח אקדמי

```r
library(tidyverse)
library(patchwork)  # install.packages("patchwork")

df <- data.frame(
  year = 2010:2024,
  gdp_growth = c(5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                 -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation  = c(2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                 -0.6, 1.5, 5.1, 4.2, 3.5)
)

p1 <- ggplot(df, aes(year, gdp_growth, fill = gdp_growth > 0)) +
  geom_col(show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE"="steelblue", "FALSE"="tomato")) +
  labs(title = "צמיחת תמ\"ג", y = "%", x = NULL) +
  theme_minimal()

p2 <- ggplot(df, aes(year, inflation)) +
  geom_line(color = "tomato", size = 1) +
  geom_ribbon(aes(ymin = 1, ymax = 3), alpha = 0.1, fill = "green") +
  labs(title = "אינפלציה (יעד בנק ישראל: 1%-3%)", y = "%", x = NULL) +
  theme_minimal()

combined <- p1 / p2 +
  plot_annotation(
    title = "מחווני מאקרו – ישראל 2010–2024",
    caption = "מקור: בנק ישראל"
  )

ggsave("macro_ggplot.png", combined, width = 10, height = 8, dpi = 150)
```

---

## המשימה שלך

בחר **נושא כלכלי אחד** שמעניין אותך (דיור, תעסוקה, מסחר, אנרגיה...).
הורד נתונים (מ-BOI / World Bank / OECD) וצור **2 גרפים לפרסום**:

1. גרף אחד ב-Python (Plotly או Matplotlib)
2. גרף אחד ב-R (ggplot2)

כל גרף: כותרת, תוויות צירים, מקור נתונים, ניתן להבין בלי הסבר נוסף.

---

## הגשה

תיקייה: `Members/YourName/Week_08/`
- [ ] `visualization.py` / `visualization.ipynb`
- [ ] `visualization.R`
- [ ] `graph1.png` + `graph2.png`
- [ ] `macro_dashboard.html` (אינטראקטיבי!)

---

**השבוע הבא:** Power BI / Tableau → [משימה 9](../Week_09_BI_Tools/README.md)
