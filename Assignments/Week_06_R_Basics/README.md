# משימה 6 – R: יסודות

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=0OQJC_FEQ_A >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=9yeOJ0ZMUYw >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=CJzeKzKz_KU >}}

:::
## Python vs R – מתי כל אחד?

| Python | R |
|---|---|
| Web scraping, APIs | אקונומטריקה מתקדמת |
| Machine Learning | מודלים סטטיסטיים |
| אוטומציה, Pipeline | מחקר אקדמי |
| Big Data | ויזואליזציה מקצועית |
| אם בחרת אחד – Python | אם בחרת שניים – גם R |

---

## חלק א – RStudio: הסביבה

פתח RStudio. הסביבה מחולקת ל-4 חלקים:
- **Console** (שמאל תחתון): הרצת קוד מיידית
- **Script** (שמאל עליון): קבצי `.R`
- **Environment** (ימין עליון): משתנים פעילים
- **Plots/Files** (ימין תחתון): גרפים ותיקיות

---

## חלק ב – יסודות R

צור קובץ `r_basics.R` ב-`Members/YourName/Week_06/`

```r
# ============================================
# R BASICS – EconLab PPE Week 6
# ============================================

# --- 1. וקטורים ומשתנים ---
gdp_growth <- c(5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                -1.9, 8.6, 6.5, 2.0, 1.1)
years <- 2010:2024

cat("ממוצע צמיחה:", mean(gdp_growth), "\n")
cat("סטיית תקן:", sd(gdp_growth), "\n")
cat("מקסימום:", max(gdp_growth), "בשנת", years[which.max(gdp_growth)], "\n")
cat("מינימום:", min(gdp_growth), "בשנת", years[which.min(gdp_growth)], "\n")

# --- 2. Data Frame ---
df <- data.frame(
  year         = years,
  gdp_growth   = gdp_growth,
  inflation    = c(2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                   -0.6, 1.5, 5.1, 4.2, 3.5),
  unemployment = c(6.6, 5.6, 6.9, 6.3, 6.0, 5.3, 4.8, 4.3, 4.0, 3.8,
                   4.3, 5.0, 3.7, 3.5, 4.2)
)

str(df)
summary(df)
```

---

## חלק ג – tidyverse

```r
# התקן את ה-tidyverse (פעם אחת):
# install.packages("tidyverse")

library(tidyverse)

# --- dplyr: עיבוד נתונים ---
df_analysis <- df |>
  filter(year >= 2015) |>
  mutate(
    decade = if_else(year < 2020, "2015-2019", "2020-2024"),
    high_inflation = inflation > 2
  ) |>
  group_by(decade) |>
  summarise(
    avg_growth     = mean(gdp_growth),
    avg_inflation  = mean(inflation),
    avg_unemp      = mean(unemployment),
    .groups = "drop"
  )

print(df_analysis)
```

---

## חלק ד – ggplot2: גרפים מקצועיים

```r
library(ggplot2)

# --- גרף 1: צמיחת תמ"ג ---
ggplot(df, aes(x = year, y = gdp_growth)) +
  geom_col(aes(fill = gdp_growth > 0), show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "steelblue", "FALSE" = "tomato")) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray40") +
  annotate("rect", xmin = 2019.5, xmax = 2020.5,
           ymin = -Inf, ymax = Inf, alpha = 0.1, fill = "orange") +
  annotate("text", x = 2020, y = -3, label = "COVID-19", size = 3) +
  labs(
    title    = "צמיחת התמ\"ג של ישראל 2010–2024",
    subtitle = "שינוי שנתי באחוזים",
    x = "שנה", y = "% שינוי"
  ) +
  theme_minimal(base_size = 13)

ggsave("gdp_growth_r.png", width = 10, height = 5, dpi = 150)

# --- גרף 2: Scatter – אינפלציה vs אבטלה ---
ggplot(df, aes(x = unemployment, y = inflation, label = year)) +
  geom_point(aes(color = year), size = 3) +
  geom_text(nudge_x = 0.1, size = 3) +
  scale_color_viridis_c() +
  labs(
    title = "עקומת Phillips – ישראל 2010–2024",
    x = "אבטלה %", y = "אינפלציה %"
  ) +
  theme_minimal()

ggsave("phillips_r.png", width = 8, height = 6, dpi = 150)
```

---

## המשימה שלך

**תרגיל 1:** הרץ את הקוד למעלה ב-RStudio. שמור את הגרפים.

**תרגיל 2:** הוסף עמודה `real_gdp_growth = gdp_growth - inflation` (צמיחה ריאלית מקורבת).
- הצג גרף שמשווה `gdp_growth` vs `real_gdp_growth` לאורך זמן.

**תרגיל 3:** שאלה כלכלית:
- חשב מתאם (Pearson) בין אינפלציה לאבטלה עבור 2010–2019 ועבור 2020–2024 בנפרד.
- האם עקומת Phillips "שוברת" אחרי COVID?

```r
# רמז:
cor(df$inflation[df$year <= 2019], df$unemployment[df$year <= 2019])
cor(df$inflation[df$year > 2019], df$unemployment[df$year > 2019])
```

---

## הגשה

תיקייה: `Members/YourName/Week_06/`
- [ ] `r_basics.R`
- [ ] `gdp_growth_r.png`
- [ ] `phillips_r.png`
- [ ] `summary.md` – תשובות לתרגיל 2 ו-3

---

**השבוע הבא:** R – אקונומטריקה → [משימה 7](../Week_07_Econometrics_R/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_06_R_Basics/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

