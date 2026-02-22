# שבוע 22 – DSGE מלא: אמידה בייזיאנית, תחזיות ופרויקט סיום

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=YXcPdS9htl4 >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=q6gOtyo1J4Y >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=rWl-P0L7-Q4 >}}

:::
## סקירת המסע – 22 שבועות

```
Excel → SQL → Python → APIs → R → Econometrics → Visualization → BI → DSGE
  1-4    5-7    8-10    11-12  13-14    15-16         17-18       19-20  21-22
```

**מה בנית עד כאן:**
- ✅ עבודה עם Excel: pivot, VLOOKUP, גרפים
- ✅ SQL: שאילתות, JOINs, CTEs
- ✅ Python: Pandas pipeline, ניקוי, ניתוח
- ✅ APIs: BOI, World Bank, FRED
- ✅ R + Tidyverse: dplyr, ggplot2
- ✅ אקונומטריקה: OLS, DiD, ARIMA, Panel
- ✅ Visualization: Plotly, Dash, ggplot2 מקצועי, R Markdown
- ✅ BI Tools: Power BI, Tableau
- ✅ DSGE מבוא: RBC, NK model, IRF

**השבוע הזה:** הכל יחד.

---

## חלק א – אמידה בייזיאנית של DSGE

### למה בייזיאנית?

**בעיה עם Maximum Likelihood (ML):**
- מודל DSGE יש בו הרבה פרמטרים
- ML מוצא local maximum (לא global)
- ML לא מנצל ידע מוקדם (Prior)

**פתרון Bayesian:**
```
Posterior ∝ Likelihood × Prior
```

אנחנו אומרים: "אני חושב ש-β ≈ 0.99 (Prior), הנתונים יכוונו אותי."

### Prior Distribution לפרמטרים

| פרמטר | Prior | Mean | SD |
|---|---|---|---|
| β (discount factor) | Beta | 0.99 | 0.002 |
| σ (CRRA) | Normal | 1.5 | 0.37 |
| h (habits) | Beta | 0.7 | 0.1 |
| φ_π (Taylor) | Normal | 1.5 | 0.25 |
| φ_y (Taylor) | Normal | 0.125 | 0.05 |
| ρ_a (TFP persist.) | Beta | 0.9 | 0.05 |
| σ_a (TFP sd) | InvGamma | 0.01 | 0.02 |

### אמידה ב-R עם `bvarsv` / `BVAR`

```r
# install.packages("BVAR")
library(BVAR)
library(tidyverse)

# נתוני מאקרו ישראל (רבעוני 2000-2024)
israel_data <- read_csv("israel_quarterly.csv") %>%
  select(date, gdp_growth, inflation, interest) %>%
  mutate(across(-date, function(x) (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)))

# הפיכה ל-matrix
y_mat <- as.matrix(israel_data %>% select(-date))

# Prior Bayesian
mn <- bvar_prior(
  y    = y_mat,
  lags = 4,
  mn   = list(
    b0 = 0,    # Litterman prior B0
    psi = list(scale = 0.04, mode = 0.004),
    lambda = list(mode = 0.2, sd = 0.4, min = 0.0001, max = 5),
    alpha  = list(mode = 2, sd = 2, min = 1, max = 3)
  )
)

# אמידה MCMC
run_bvar <- bvar(y = y_mat,
                 lags = 4,
                 n_draw   = 20000,
                 n_burn   = 5000,
                 n_thin   = 2,
                 priors   = mn,
                 verbose  = TRUE)

# תוצאות
summary(run_bvar)

# IRFs
irfs <- irf(run_bvar,
             impulse   = "interest",
             response  = c("gdp_growth", "inflation"),
             horizon   = 20,
             sign_restr = NULL)

plot(irfs,
     main = "Israel BVAR: Interest Rate Shock",
     ylab = "% Deviation from SS")
```

---

## חלק ב – BVAR: Vector Autoregression בייזיאני

BVAR = VAR עם Prior בייזיאני. פחות תיאורטי מ-DSGE אבל חזק יותר לתחזיות.

### מודל VAR(p)

```
Yₜ = A₁Yₜ₋₁ + A₂Yₜ₋₂ + ... + AₚYₜ₋ₚ + εₜ

Y = vector of variables (GDP, CPI, Interest, Unemployment)
A = coefficient matrices
ε ~ N(0, Σ)
```

### אמידה ב-R

```r
library(bvartools)  # install.packages("bvartools")
library(tidyverse)

# נתוני ישראל רבעוני
data_vars <- israel_data %>%
  select(gdp_growth, inflation, interest, unemployment) %>%
  ts(start = c(2000, 1), frequency = 4)

# יצירת מודל VAR
# בחירת lag עם AIC/BIC
library(vars)
lag_sel <- VARselect(data_vars, lag.max = 8, type = "const")
print(lag_sel$selection)  # AIC, BIC, HQ מסכימים על p=?

# VAR(p) OLS
p_opt <- lag_sel$selection["AIC(n)"]
var_model <- VAR(data_vars, p = p_opt, type = "const")
summary(var_model)

# BVAR עם Minnesota Prior
library(BVAR)
bvar_model <- bvar(
  data_vars,
  lags   = p_opt,
  n_draw = 15000,
  n_burn = 5000
)

# IRF: מה קורה לכלכלה אחרי עלייה בריבית?
irf_bvar <- irf(bvar_model,
                impulse   = "interest",
                response  = c("gdp_growth", "inflation", "unemployment"),
                horizon   = 20)

plot(irf_bvar)

# תחזית 8 רבעונים
fc <- predict(bvar_model, horizon = 8, conf_bands = 0.1)
plot(fc)
```

### Forecast Error Variance Decomposition (FEVD)

```r
# כמה מהשונות בGDP מוסבר על ידי הלם ריבית?
fevd_result <- fevd(bvar_model, horizon = 20)
plot(fevd_result)

# תרשים עוגה: מקורות השונות
# אחרי 4 רבעונים: GDP shock 60%, Interest 25%, Inflation 15%
```

---

## חלק ג – Smets-Wouters Model (Abridged)

המודל SW הוא ה-DSGE הנפוץ ביותר. מוסיף ל-RBC הבסיסי:
- **Habit formation** בצריכה: Cₜ - hCₜ₋₁
- **Capital adjustment costs**: Φ(Iₜ/Kₜ)
- **Calvo pricing**: פירמות לא יכולות לשנות מחיר בכל תקופה
- **Wage rigidity**: עובדים לא יכולים לשנות שכר חופשי
- **7 הלמים**: technology, preference, investment, government, price markup, wage markup, monetary

```r
# הגדרת Smets-Wouters ב-gEcon (קצר)
# הקובץ .gcn מלא מגיע עם חבילת gEcon

library(gEcon)

# קובץ מוכן מספריית gEcon
sw_model <- make_model(system.file("examples", "rbc.gcn", package = "gEcon"))
sw_model <- steady_state(sw_model)
sw_model <- solve_pert(sw_model, loglin = TRUE)

# אמידה בייזיאנית (דורשת Dynare או IRIS לביצוע מלא)
# דוגמה: הצגת Posterior distributions

# Prior means (SW 2003)
priors_sw <- tibble(
  parameter = c("sigma_c", "h", "xi_w", "sigma_l", "xi_p",
                "iota_w", "iota_p", "psi", "phi_p",
                "r_pi", "r_y", "r_Delta_y", "rho"),
  distribution = c("Normal","Beta","Beta","Normal","Beta",
                   "Beta","Beta","Beta","Normal",
                   "Normal","Normal","Normal","Beta"),
  mean = c(1.39, 0.71, 0.73, 1.92, 0.65,
           0.59, 0.69, 0.54, 1.61,
           1.68, 0.10, 0.16, 0.60),
  sd   = c(0.37, 0.10, 0.05, 0.75, 0.10,
           0.15, 0.15, 0.15, 0.10,
           0.30, 0.05, 0.05, 0.10)
)

# תרשים Prior distributions
priors_sw %>%
  ggplot(aes(x = reorder(parameter, mean), y = mean)) +
  geom_point(size = 4, color = "#1565C0") +
  geom_errorbar(aes(ymin = mean - 2*sd, ymax = mean + 2*sd),
                width = 0.3, color = "#1565C0", alpha = 0.6) +
  coord_flip() +
  labs(title = "Smets-Wouters (2003): Prior Distributions",
       subtitle = "Mean ± 2SD",
       x = "Parameter", y = "Prior Value") +
  theme_minimal()
```

---

## חלק ד – Pipeline: נתונים עד תחזית

```r
# ===========================================================
# DSGE MACRO FORECASTING PIPELINE – ישראל 2025
# ===========================================================

library(tidyverse)
library(BVAR)
library(forecast)
library(vars)

cat("=== Pipeline תחזית מאקרו – ישראל ===\n\n")

# ---- STEP 1: שליפת נתונים ----
cat("[1] שולפת נתוני BOI...\n")
source("boi_pipeline.R")  # מ-שבוע 11

macro_q <- fetch_boi_quarterly(
  series = c("INT_RATE", "CPI_1Y", "RER_USD_ILS"),
  start  = "2000-01",
  end    = "2024-12"
)

# נתוני תמ"ג (מ-CBS)
gdp_q <- read_csv("gdp_quarterly_cbs.csv") %>%
  mutate(gdp_qoq = (gdp / lag(gdp, 1) - 1) * 100)

# מיזוג
all_data <- macro_q %>%
  left_join(gdp_q, by = "date") %>%
  drop_na()

cat(sprintf("  ✓ %d רבעונים נטענו\n", nrow(all_data)))

# ---- STEP 2: עיצוב ל-VAR ----
cat("\n[2] מכין מטריצת נתונים...\n")

y_mat <- all_data %>%
  select(gdp_qoq, CPI_1Y, INT_RATE) %>%
  as.matrix()

y_ts <- ts(y_mat, start = c(2000, 1), frequency = 4)

# בחירת lag
lag_sel <- VARselect(y_ts, lag.max = 8)
p_opt   <- lag_sel$selection["AIC(n)"]
cat(sprintf("  ✓ Lag אופטימלי: %d\n", p_opt))

# ---- STEP 3: אמידת BVAR ----
cat("\n[3] מאמד BVAR...\n")
bvar_fit <- bvar(y_ts, lags = p_opt, n_draw = 20000, n_burn = 5000)
cat("  ✓ MCMC הסתיים\n")

# ---- STEP 4: IRF ----
cat("\n[4] מחשב IRF...\n")
irf_res <- irf(bvar_fit,
               impulse   = "INT_RATE",
               response  = c("gdp_qoq", "CPI_1Y"),
               horizon   = 16)

# ---- STEP 5: תחזית 8 רבעונים ----
cat("\n[5] מייצר תחזית 2025-2026...\n")
fc <- predict(bvar_fit, horizon = 8, conf_bands = c(0.16, 0.84))

# ---- STEP 6: ויזואליזציה ----
cat("\n[6] מייצר גרפים...\n")

# IRF Plot
par(mfrow = c(1, 2))
plot(irf_res, main = "IRF: הלם ריבית → GDP + אינפלציה")

# Forecast Plot
plot(fc)
par(mfrow = c(1, 1))

# ggplot מקצועי
fc_df <- as_tibble(fc$fcast$gdp_qoq) %>%
  rename(point = `50%`, lo_16 = `16%`, hi_84 = `84%`) %>%
  mutate(period = seq(as.Date("2025-01-01"),
                      by = "quarter", length.out = 8),
         type = "תחזית")

hist_df <- tibble(
  period = all_data$date[all_data$date >= as.Date("2022-01-01")],
  point  = all_data$gdp_qoq[all_data$date >= as.Date("2022-01-01")],
  lo_16  = NA, hi_84 = NA,
  type   = "היסטורי"
)

combined_fc <- bind_rows(hist_df, fc_df)

ggplot(combined_fc, aes(x = period)) +
  geom_ribbon(data = filter(combined_fc, type == "תחזית"),
              aes(ymin = lo_16, ymax = hi_84),
              fill = "steelblue", alpha = 0.25) +
  geom_line(aes(y = point, color = type, linetype = type),
            linewidth = 1.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray40") +
  scale_color_manual(values = c("היסטורי" = "black", "תחזית" = "steelblue")) +
  scale_linetype_manual(values = c("היסטורי" = "solid", "תחזית" = "dashed")) +
  labs(
    title    = "תחזית צמיחת תמ\"ג ישראל – BVAR",
    subtitle = "תחזית 8 רבעונים עם רווח סמך 68%",
    x        = NULL, y = "% שינוי רבעוני",
    color    = NULL, linetype = NULL,
    caption  = "מקור: בנק ישראל, הלמ\"ס | EconLab PPE | מודל BVAR(4)"
  ) +
  theme_minimal() +
  theme(legend.position = "top")

ggsave("gdp_forecast_bvar.png", width = 10, height = 5.5, dpi = 300)

# ---- STEP 7: דוח ----
cat("\n[7] שומר תוצאות...\n")
write_csv(fc_df, "gdp_forecast_2025_2026.csv")

cat("\n✓ Pipeline הסתיים! תחזית שמורה.\n")
```

---

## חלק ה – פרויקט גמר: דוח מחקר מקיף

### "ניתוח מאקרו-כלכלי של ישראל 2018-2026: מדיניות מוניטרית, צמיחה ותחזית"

**מה להגיש:**

```
Members/YourName/Week_22_Final_Project/
├── 1_data_collection/
│   ├── boi_pipeline.R          ← נתוני BOI
│   ├── worldbank_fetch.py      ← נתוני World Bank
│   └── data_combined.csv       ← נתונים מאוחדים
│
├── 2_eda/
│   ├── exploratory_analysis.R  ← ניתוח תיאורי
│   └── eda_plots.png
│
├── 3_econometrics/
│   ├── ols_regression.R        ← OLS + diagnostic
│   ├── did_analysis.R          ← DiD: השפעת ריבית
│   ├── arima_cpi.R             ← ARIMA CPI
│   └── regression_table.html
│
├── 4_dsge/
│   ├── nk_simulation.R         ← NK Model IRF
│   ├── bvar_model.R            ← BVAR + forecast
│   └── nk_irf.png
│
├── 5_visualization/
│   ├── dashboard.py            ← Dash dashboard
│   ├── macro_report.Rmd        ← R Markdown
│   └── macro_report.html       ← rendered
│
└── final_report.md             ← דוח מסכם
```

### מבנה הדוח `final_report.md`

```markdown
# ניתוח מאקרו-כלכלי: ישראל בעידן הריבית הגבוהה (2018-2026)

## תקציר מנהלים (Executive Summary)
- 3 ממצאים מרכזיים בשפה עממית

## 1. רקע ושאלות מחקר
- תיאור המצב הכלכלי 2018-2024
- 4 שאלות מחקר ספציפיות

## 2. מתודולוגיה ונתונים
- מקורות: BOI, CBS, World Bank, FRED
- כלים: Python (Pandas, Plotly), R (tidyverse, lm, BVAR)
- 3 שיטות: OLS, DiD, BVAR

## 3. ניתוח תיאורי
- 4 גרפי מאקרו מקצועיים
- טבלת סטטיסטיקה תיאורית

## 4. ניתוח אקונומטרי
- רגרסיה: גורמי צמיחה (R² = ?, p-values)
- DiD: השפעת הריבית על שוק הדיור
- ARIMA: תחזית CPI

## 5. מודל DSGE/BVAR
- IRF: 16 תקופות אחרי הלם ריבית
- תחזית: 2025-2026

## 6. השוואה בין-לאומית
- ישראל מול OECD (World Bank data)
- מדדי מאקרו 2022-2024

## 7. מסקנות ומדיניות
- תשובה לכל שאלת מחקר
- המלצות מדיניות (עם סייגים!)

## 8. מגבלות המחקר
- מה לא כיסינו, איפה הנתונים חסרים

## נספחים
- קוד מלא (link to GitHub)
- נתונים גולמיים (link to Google Drive)
- טבלאות רגרסיה מלאות
```

---

## ציר הזמן לפרויקט גמר

| שבוע | משימה |
|---|---|
| **22 יום 1-2** | שליפת נתונים, ניקוי, EDA |
| **22 יום 3-4** | אקונומטריקה (OLS, DiD, ARIMA) |
| **22 יום 5** | BVAR + תחזית |
| **22 יום 6** | Dash Dashboard + R Markdown |
| **22 יום 7** | כתיבת הדוח המסכם |

---

## הגשה הסופית

```
Members/YourName/Final_Project/
├── [כל התיקיות מלעיל]
├── final_report.html           ← R Markdown rendered
├── macro_dashboard.html        ← Dash app exported
└── presentation.pdf            ← 10 שקפים לפרזנטציה
```

### קריטריונים להערכה

| קריטריון | משקל |
|---|---|
| **איכות נתונים** (מקורות, ניקוי, תיעוד) | 20% |
| **ניתוח אקונומטרי** (שיטות, אבחון, פרשנות) | 30% |
| **DSGE/BVAR** (מודל, IRF, תחזית) | 20% |
| **ויזואליזציה** (גרפים, דשבורד) | 15% |
| **דוח ופרזנטציה** (בהירות, ממצאים) | 15% |

---

## מה עכשיו? – Next Steps

ברכות! סיימת 22 שבועות של הכשרת כלכלן-נתונים.

**כישורים שרכשת:**
- ✅ ניתוח נתונים (Python + R)
- ✅ API data collection
- ✅ אקונומטריקה יישומית
- ✅ ויזואליזציה מקצועית
- ✅ DSGE ומאקרו-כלכלה מתקדמת

**המשך הדרך:**
1. **Portfolio:** הוסף פרויקטים ל-GitHub ול-Tableau Public
2. **כלים נוספים:** Julia (DSGE), Stata (אקדמיה), Dynare (בנקים מרכזיים)
3. **מחקר:** קרא את ה-BOI Working Papers, NBER, IMF WP
4. **קהילה:** EconLab PPE – הישאר פעיל, עזור לחברים חדשים

---

*"An economist who can program is an economist who can answer questions."*
*― EconLab PPE*

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_22_DSGE_Advanced/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

