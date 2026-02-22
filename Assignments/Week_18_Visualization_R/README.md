# שבוע 18 – ggplot2 מתקדם ו-R Markdown: דוחות לפרסום

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=h29g21z0a68 >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=n8kYa9vuLI0 >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=qRvEpZX6jHk >}}

:::
## חלק א – ggplot2 מתקדם: Theme מקצועי

### Theme בסיסי לפרסום

```r
library(tidyverse)
library(scales)
library(ggtext)      # install.packages("ggtext")
library(patchwork)   # install.packages("patchwork")

# Theme מותאם אישית
theme_econlab <- function(base_size = 12) {
  theme_minimal(base_size = base_size) %+replace%
    theme(
      # כותרות
      plot.title       = element_text(size = base_size + 2, face = "bold",
                                      margin = margin(b = 8)),
      plot.subtitle    = element_text(size = base_size - 1, color = "gray50",
                                      margin = margin(b = 12)),
      plot.caption     = element_text(size = base_size - 3, color = "gray60",
                                      hjust = 0, margin = margin(t = 10)),

      # צירים
      axis.title       = element_text(size = base_size - 1, color = "gray30"),
      axis.text        = element_text(size = base_size - 2, color = "gray40"),
      axis.ticks       = element_blank(),
      axis.line.x      = element_line(color = "gray80", linewidth = 0.4),

      # רשת
      panel.grid.major.y = element_line(color = "gray92", linewidth = 0.4),
      panel.grid.major.x = element_blank(),
      panel.grid.minor   = element_blank(),

      # רקע
      plot.background  = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA),

      # אגדה
      legend.position     = "top",
      legend.direction    = "horizontal",
      legend.title        = element_blank(),
      legend.key.size     = unit(0.8, "lines"),
      legend.text         = element_text(size = base_size - 2),

      # margin כולל
      plot.margin = margin(15, 15, 10, 15)
    )
}
```

### גרף ברמת The Economist

```r
macro_df <- tibble(
  year         = 2018:2024,
  gdp_growth   = c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation    = c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5),
  interest     = c(0.1, 0.25, 0.1, 0.1, 3.25, 4.75, 4.5),
  unemployment = c(4.0, 3.8, 4.3, 5.0, 3.7, 3.5, 4.2),
)

# גרף עמודות מקצועי
p1 <- ggplot(macro_df, aes(x = year, y = gdp_growth)) +
  # שנת קורונה
  annotate("rect", xmin = 2019.5, xmax = 2020.5,
           ymin = -Inf, ymax = Inf, fill = "gray90", alpha = 0.8) +
  annotate("text", x = 2020, y = 9.5, label = "קורונה",
           size = 3, color = "gray50", angle = 90) +
  # תקופת ריבית גבוהה
  annotate("rect", xmin = 2021.5, xmax = 2024.5,
           ymin = -Inf, ymax = Inf, fill = "#FFF3E0", alpha = 0.6) +
  annotate("text", x = 2023, y = 9.5, label = "ריבית גבוהה",
           size = 3, color = "#E65100") +
  # עמודות
  geom_col(aes(fill = gdp_growth > 0), width = 0.7, show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#C62828")) +
  # קו אפס
  geom_hline(yintercept = 0, color = "gray40", linewidth = 0.6) +
  # ממוצע
  geom_hline(yintercept = mean(macro_df$gdp_growth),
             linetype = "dashed", color = "gray60", linewidth = 0.8) +
  annotate("text", x = 2018.3, y = mean(macro_df$gdp_growth) + 0.3,
           label = sprintf("ממוצע: %.1f%%", mean(macro_df$gdp_growth)),
           size = 3, color = "gray50") +
  # labels על עמודות
  geom_text(aes(label = sprintf("%.1f%%", gdp_growth),
                vjust = ifelse(gdp_growth > 0, -0.4, 1.3)),
            size = 3.2, fontface = "bold",
            color = ifelse(macro_df$gdp_growth > 0, "#1565C0", "#C62828")) +
  scale_x_continuous(breaks = 2018:2024) +
  scale_y_continuous(labels = function(x) paste0(x, "%"),
                     limits = c(-3.5, 11)) +
  labs(
    title    = "**צמיחת תמ\"ג ישראל**, 2018–2024",
    subtitle = "שינוי שנתי בתמ\"ג הריאלי, בקבוע מחיר 2015",
    x        = NULL,
    y        = "שינוי שנתי (%)",
    caption  = "מקור: בנק ישראל, הלשכה המרכזית לסטטיסטיקה | EconLab PPE"
  ) +
  theme_econlab()

# ggtext מאפשר bold/italic בכותרות
p1 <- p1 +
  theme(plot.title = element_markdown(size = 14))

print(p1)
ggsave("gdp_economist_style.png", p1, width = 10, height = 5.5, dpi = 300)
```

---

## חלק ב – patchwork: כמה גרפים בדף אחד

```r
library(patchwork)

# גרף 2: קו ריבית
p2 <- ggplot(macro_df, aes(x = year, y = interest)) +
  geom_step(linewidth = 2, color = "#1565C0") +
  geom_area(stat = "identity", alpha = 0.15, fill = "#1565C0") +
  scale_x_continuous(breaks = 2018:2024) +
  scale_y_continuous(labels = function(x) paste0(x, "%")) +
  labs(title = "ריבית בנק ישראל",
       x = NULL, y = "ריבית (%)") +
  theme_econlab()

# גרף 3: scatter
p3 <- ggplot(macro_df, aes(x = inflation, y = gdp_growth, color = year)) +
  geom_point(size = 4) +
  geom_text(aes(label = year), vjust = -0.8, size = 3) +
  geom_smooth(method = "lm", se = TRUE, color = "gray50", alpha = 0.2) +
  scale_color_viridis_c(option = "plasma", guide = "none") +
  labs(title = "אינפלציה vs. צמיחה",
       x = "אינפלציה (%)", y = "צמיחת תמ\"ג (%)") +
  theme_econlab()

# גרף 4: lollipop אבטלה
p4 <- macro_df %>%
  mutate(year = factor(year)) %>%
  ggplot(aes(x = unemployment, y = reorder(year, unemployment))) +
  geom_segment(aes(xend = 0, yend = reorder(year, unemployment)),
               color = "gray80", linewidth = 0.8) +
  geom_point(color = "#1565C0", size = 4) +
  geom_text(aes(label = paste0(unemployment, "%")),
            hjust = -0.4, size = 3.2) +
  labs(title = "שיעור אבטלה לפי שנה",
       x = "אבטלה (%)", y = NULL) +
  theme_econlab() +
  theme(panel.grid.major.y = element_blank(),
        panel.grid.major.x = element_line(color = "gray92"))

# חיבור ב-patchwork
combined <- (p1 | p2) / (p3 | p4) +
  plot_annotation(
    title    = "נתוני מאקרו ישראל 2018–2024: ניתוח מקיף",
    subtitle = "ארבעה מדדים עיקריים",
    caption  = "מקור: בנק ישראל | EconLab PPE",
    theme    = theme(
      plot.title    = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12, color = "gray50")
    )
  )

ggsave("macro_4panel.png", combined, width = 14, height = 10, dpi = 300)
```

---

## חלק ג – scales ו-coordinate systems מתקדמים

```r
library(scales)

# --- לוגריתמי: GDP absolute ---
gdp_level <- tibble(
  year = 2018:2024,
  gdp_bn = c(370, 395, 388, 468, 564, 590, 610),  # מיליארד ₪
  exports = c(60, 68, 59, 73, 82, 75, 78)         # מיליארד $
)

ggplot(gdp_level, aes(x = year, y = gdp_bn)) +
  geom_line(linewidth = 2, color = "#1565C0") +
  geom_point(size = 3, color = "#1565C0") +
  scale_y_continuous(
    labels = label_number(scale = 1, suffix = " מיליארד ₪",
                          big.mark = ","),
    limits = c(350, 650)
  ) +
  scale_x_continuous(breaks = 2018:2024) +
  labs(title = "תמ\"ג ישראל – ערך נומינלי",
       x = NULL, y = NULL) +
  theme_econlab()

# --- percent scale ---
ggplot(macro_df, aes(x = year)) +
  geom_line(aes(y = inflation / 100), color = "orange", linewidth = 2) +
  geom_point(aes(y = inflation / 100), color = "orange", size = 3) +
  scale_y_continuous(labels = percent_format(accuracy = 0.1)) +
  labs(title = "אינפלציה – פורמט אחוזים") +
  theme_econlab()

# --- coord_flip: גרף עמודות אופקי ---
macro_df %>%
  arrange(gdp_growth) %>%
  mutate(year = factor(year, levels = year)) %>%
  ggplot(aes(x = year, y = gdp_growth,
             fill = gdp_growth > 0)) +
  geom_col(show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#C62828")) +
  coord_flip() +
  labs(title = "שנות צמיחה ומיתון – ממוין",
       x = NULL, y = "% צמיחה") +
  theme_econlab()
```

---

## חלק ד – R Markdown: דוח מחקר מלא

### מה זה R Markdown?

**R Markdown** = מסמך שמשלב:
- **Markdown** (טקסט)
- **R Code Chunks** (קוד שרץ ומציג תוצאות)
- **פלט**: HTML, PDF, Word

### מבנה מסמך

```yaml
---
title: "ניתוח שוק הדיור הישראלי 2018–2024"
author: "שם הסטודנט | EconLab PPE"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    toc_float: true
    theme: flatly
    code_folding: hide
    df_print: paged
  pdf_document:
    latex_engine: xelatex
lang: he
---
```

### חלקים של המסמך

````markdown
## 1. רקע ושאלת מחקר

שוק הדיור הישראלי חווה עלייה חדה במחירים בשנים 2020–2022,
ולאחר מכן ירידה קלה עם העלאת הריבית.
נשאלת השאלה: **האם ריבית גבוהה גרמה לירידת מחירים?**

## 2. נתונים

```r
library(tidyverse)
library(stargazer)
library(knitr)
library(kableExtra)

knitr::opts_chunk$set(
  echo    = TRUE,
  warning = FALSE,
  message = FALSE,
  fig.width  = 9,
  fig.height = 5.5
)
```

```r
# טעינת נתונים
housing <- read_csv("housing_data.csv")
macro   <- read_csv("macro_data.csv")

# תצוגה בטבלה נחמדה
housing %>%
  head(10) %>%
  kable(caption = "10 שורות ראשונות – נתוני דיור") %>%
  kable_styling(bootstrap_options = "striped", full_width = FALSE)
```

## 3. תיאור נתונים

```r
macro %>%
  select(-year) %>%
  summary() %>%
  kable(caption = "סטטיסטיקה תיאורית") %>%
  kable_styling()
```

```r
ggplot(macro, aes(x = year, y = gdp_growth)) +
  geom_col(aes(fill = gdp_growth > 0), show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#C62828")) +
  labs(x = NULL, y = "% צמיחה") +
  theme_econlab()
```

## 4. ניתוח אקונומטרי

```r
model1 <- lm(house_price_idx ~ interest, data = macro)
model2 <- lm(house_price_idx ~ interest + gdp_growth, data = macro)
model3 <- lm(house_price_idx ~ interest + gdp_growth + inflation, data = macro)
```

```r
stargazer(model1, model2, model3,
          type      = "html",
          title     = "טבלה 1: גורמי מחירי הדיור",
          dep.var.labels = "מדד מחירי דיור",
          covariate.labels = c("ריבית", "צמיחת תמ\"ג", "אינפלציה"),
          no.space  = TRUE,
          digits    = 3)
```

## 5. ממצאים ומסקנות

```r
did_coef <- coef(model1)["interest"]
```

ניתוח הרגרסיה מצביע כי עלייה של 1% בריבית קשורה לשינוי של
**`r round(did_coef, 2)`** נקודות במדד הדיור (p < 0.05).

ממצא זה עולה בקנה אחד עם תיאוריה כלכלית...
````

### Render המסמך

```r
# ב-RStudio: לחץ "Knit" → בחר פורמט
# או בקונסול:
rmarkdown::render("housing_analysis.Rmd", output_format = "html_document")
rmarkdown::render("housing_analysis.Rmd", output_format = "pdf_document")
```

---

## חלק ה – plotly אינטראקטיבי ב-R Markdown

```r
# install.packages("plotly")
library(plotly)

# ggplot → plotly אינטראקטיבי!
p <- ggplot(macro_df, aes(x = year, y = gdp_growth,
                           text = paste("שנה:", year,
                                        "<br>צמיחה:", gdp_growth, "%"))) +
  geom_col(aes(fill = gdp_growth > 0), show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#C62828")) +
  labs(title = "צמיחת תמ\"ג", x = NULL, y = "%") +
  theme_econlab()

# המרה ל-plotly (אינטראקטיבי ב-HTML!)
ggplotly(p, tooltip = "text")
```

---

## חלק ו – שפת gtsummary: טבלאות מחקר

```r
install.packages("gtsummary")
library(gtsummary)

# טבלה מסכמת מקצועית
macro_df %>%
  select(gdp_growth, inflation, interest, unemployment) %>%
  tbl_summary(
    label = list(
      gdp_growth   ~ "צמיחת תמ\"ג (%)",
      inflation    ~ "אינפלציה (%)",
      interest     ~ "ריבית (%)",
      unemployment ~ "אבטלה (%)"
    ),
    statistic = all_continuous() ~ "{mean} ({sd})",
    digits    = all_continuous() ~ 2
  ) %>%
  modify_caption("**טבלה 1: סטטיסטיקה תיאורית – ישראל 2018-2024**")

# טבלת regression מקצועית
library(broom)
lm(gdp_growth ~ interest + inflation + unemployment, data = macro_df) %>%
  tbl_regression(
    label = list(
      interest     ~ "ריבית (%)",
      inflation    ~ "אינפלציה (%)",
      unemployment ~ "אבטלה (%)"
    )
  ) %>%
  add_significance_stars() %>%
  modify_caption("**טבלה 2: רגרסיה – גורמי צמיחת תמ\"ג**")
```

---

## משימות השבוע

### משימה 1: Theme מותאם + 4 גרפים (30 נקודות)

```r
# 1. צור theme_yourname() מותאם אישית (צבעים, גופן, grid)
# 2. צור 4 גרפים שונים (bar, line, scatter, lollipop)
#    על נתוני מאקרו ישראל – כולם עם theme_yourname()
# 3. חבר ב-patchwork עם plot_annotation()
# 4. ggsave() ב-dpi=300, 14×10 אינץ'
```

### משימה 2: R Markdown דוח מלא (40 נקודות)

```r
# כתוב "housing_analysis.Rmd" שכולל:
# - YAML header עם TOC
# - 5 sections: רקע, נתונים, תיאורי, רגרסיה, מסקנות
# - kable() לתצוגת נתונים
# - 3 גרפים ggplot2 (fig.cap)
# - stargazer() / gtsummary() לרגרסיה
# - Inline stats: "ממוצע הצמיחה היה `r round(mean(gdp), 2)`%"
# - Render ל-HTML
```

### משימה 3: ggplot2 + plotly אינטראקטיבי (30 נקודות)

```r
# 1. גרף ggplot2 מלא (5 שכבות, עיצוב מקצועי)
# 2. המרה ל-plotly עם ggplotly() + tooltip מותאם
# 3. הטמע ב-R Markdown → HTML אינטראקטיבי
# 4. שמור כ-widget HTML עצמאי:
htmlwidgets::saveWidget(ggplotly(p), "interactive_macro.html")
```

---

## הגשה

```
Members/YourName/Week_18/
├── ggplot2_advanced.R
├── housing_analysis.Rmd
├── housing_analysis.html        ← rendered
├── macro_4panel.png
├── gdp_economist_style.png
└── interactive_macro.html
```

---

**המודול הבא:** Power BI ו-Tableau – דשבורדים לביזנס → [שבוע 19](../Week_19_BI_Tools/README.md)

### 💻 תרגול מעשי (Hands-on)

<p>לחצו על המשולש (Play) כדי להפעיל את סביבת הפיתוח בתוך העמוד, או פתחו בלשונית חדשה לנוחות מירבית.</p>
<iframe src="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_18_Visualization_R/starter_notebook.ipynb" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
<p><br><em>* אם המסך לא נטען או מבקש הרשאות אבטחה, <a href="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_18_Visualization_R/starter_notebook.ipynb" target="_blank">לחצו כאן לפתיחת המחברת במסך מלא</a>.</em></p>
