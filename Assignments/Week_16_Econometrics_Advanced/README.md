# שבוע 16 – אקונומטריקה מתקדמת: DiD, ARIMA ו-Panel Data
### 🎥 סרטון הדרכה מרכזי
צפו בסרטון הבא שמכסה את ליבת החומר הטכני של שבוע זה:
{{< video https://www.youtube.com/watch?v=5MtcxFAq8wM >}}


> **רמה:** מתקדם – מניח שסיימת שבוע 15 (רגרסיה OLS)
> **מטרת השבוע:** שלוש שיטות אקונומטריות שמשמשות בכל מחקר כלכלי מקצועי

---

## שלוש שיטות שתלמד השבוע

| שיטה | שאלה | דוגמה |
|---|---|---|
| **DiD** | האם מדיניות X שינתה Y? | האם העלאת ריבית הפחיתה מחירי דיור? |
| **ARIMA** | מה יהיה Y בתקופה הבאה? | תחזית אינפלציה לשנה הבאה |
| **Panel Data** | מה האפקט של X על Y בין ישויות? | מה השפעת ריבית על אבטלה ב-38 מדינות OECD? |

---

## חלק א – Difference-in-Differences (DiD)

### הרעיון

DiD = שיטה לזיהוי **סיבתיות** (לא רק קורלציה).

**שאלה:** האם מדיניות X גרמה לשינוי ב-Y?

**בעיה:** לא ניתן לראות מה היה קורה ל-treated ללא הטיפול.

**פתרון DiD:**
```
DiD = (Treated_After - Treated_Before) - (Control_After - Control_Before)
```

### הנחת מגמות מקבילות (Parallel Trends)

לפני ההתערבות, treated ו-control היו מתפתחים באופן מקביל.

### דוגמה: השפעת מחסום 2022 על שוק הדיור

**רקע:** בנק ישראל העלה ריבית חדות ב-2022. האם זה הפחית מחירי דיור?

**Design:**
- **Treated:** ערים עם משכנתאות גבוהות במיוחד
- **Control:** ערים עם משכנתאות נמוכות
- **Before:** 2019-2021
- **After:** 2022-2024

```r
library(tidyverse)
library(broom)

# נתוני דיור (סינטטי)
set.seed(42)
housing_data <- tibble(
  city_id   = rep(1:20, each = 12),   # 20 ערים
  period    = rep(1:12, times = 20),  # 12 תקופות (רבעונים 2021-2023)
  year      = rep(rep(2021:2023, each = 4), times = 20),
  quarter   = rep(1:4, times = 60),
  treated   = rep(c(rep(1, 10), rep(0, 10)), each = 12),  # 10 ערים treated
  post_2022 = as.integer(year >= 2022),
  price_idx = 100 +
    rep(c(rep(15, 10*12), rep(10, 10*12))) +  # treated קצת גבוה יותר בהתחלה
    rep(1:12, times = 20) * 2 +               # מגמה כללית
    (rep(c(rep(1, 10), rep(0, 10)), each = 12) *
     as.integer(rep(year >= 2022, 1)) * -8) + # DiD effect: treated ירד בpost
    rnorm(240, 0, 3)
)

# --- מודל DiD בסיסי ---
did_model <- lm(
  price_idx ~ treated + post_2022 + treated:post_2022,
  data = housing_data
)

summary(did_model)
# treated:post_2022 → הוא ה-DiD estimator
# אם שלילי ומובהק → העלאת הריבית הפחיתה מחירים דווקא בערים עם משכנתא גבוהה

tidy(did_model) %>%
  filter(str_detect(term, "treated|post"))
```

### DiD עם Two-Way Fixed Effects (TWFE)

מודל מתקדם שמטפל בהטרוגניות לא נצפית.

```r
library(fixest)  # install.packages("fixest")

# שלב 1: הוסף fixed effects
twfe_model <- feols(
  price_idx ~ treated:post_2022 | city_id + period,
  data = housing_data,
  cluster = ~city_id   # cluster SEs ברמת עיר
)

summary(twfe_model)
etable(twfe_model)  # טבלה יפה

# שלב 2: event study (בדיקת parallel trends)
housing_data <- housing_data %>%
  mutate(period_rel = period - 5)  # period 5 = "פגישת" 2022

event_model <- feols(
  price_idx ~ i(period_rel, treated, ref = -1) | city_id + period,
  data = housing_data,
  cluster = ~city_id
)

# גרף event study
iplot(event_model,
      main = "Event Study: השפעת הריבית על מחירי דיור",
      xlab = "רבעונים מההתערבות",
      ylab = "שינוי מחיר (נקודות)")
```

### stargazer ל-DiD

```r
library(stargazer)

m1 <- lm(price_idx ~ treated + post_2022 + treated:post_2022,
         data = housing_data)
m2 <- feols(price_idx ~ treated:post_2022 | city_id, data = housing_data)
m3 <- feols(price_idx ~ treated:post_2022 | city_id + period,
            data = housing_data, cluster = ~city_id)

# stargazer (רק לlm)
stargazer(m1, type = "text",
          covariate.labels = c("Treated", "Post-2022", "DiD (Treated×Post)"),
          dep.var.labels = "Housing Price Index",
          title = "Impact of Rate Hike on Housing Prices – DiD")

# etable ל-fixest
etable(m2, m3,
       title = "TWFE DiD Models",
       headers = c("City FE", "City + Period FE"))
```

---

## חלק ב – ARIMA: ניתוח וחיזוי סדרות עתיות

### מה זה ARIMA?

**ARIMA(p,d,q)**:
- **AR(p)**: Autoregressive – Y_t תלוי בערכים קודמים
- **I(d)**: Integrated – כמה פעמים לגזור כדי שהסדרה תהיה stationary
- **MA(q)**: Moving Average – Y_t תלוי בשגיאות עבר

### Pipeline ARIMA

```r
library(forecast)  # install.packages("forecast")
library(tseries)   # install.packages("tseries")
library(tidyverse)

# נתוני CPI חודשי
cpi_monthly <- c(
  100.0, 100.3, 100.5, 100.8, 101.0, 101.2,  # 2021
  101.5, 101.9, 102.4, 102.8, 103.1, 103.5,
  104.0, 104.6, 105.2, 105.9, 106.5, 107.0,  # 2022
  107.6, 108.0, 108.3, 108.5, 108.7, 108.9,
  109.1, 109.3, 109.5, 109.7, 109.9, 110.1,  # 2023
  110.3, 110.4, 110.5, 110.6, 110.7, 110.8,
  110.9, 111.0, 111.2, 111.3, 111.5, 111.6   # 2024
)

# המרה ל-ts object
cpi_ts <- ts(cpi_monthly, start = c(2021, 1), frequency = 12)

# ---- שלב 1: בדיקת Stationarity ----
adf.test(cpi_ts)
# H0: הסדרה non-stationary (יש unit root)
# p < 0.05 → stationary (אפשר להמשיך)
# p > 0.05 → non-stationary (צריך לגזור)

# גזירה ראשונה (d=1)
cpi_diff <- diff(cpi_ts, differences = 1)
adf.test(cpi_diff)  # בדוק שוב

# ---- שלב 2: בחירת p, q – ACF ו-PACF ----
par(mfrow = c(1, 2))
acf(cpi_diff, main = "ACF של השינויים")     # → q
pacf(cpi_diff, main = "PACF של השינויים")   # → p
par(mfrow = c(1, 1))

# ---- שלב 3: auto.arima() – בחירה אוטומטית ----
arima_auto <- auto.arima(
  cpi_ts,
  stepwise    = FALSE,
  approximation = FALSE,
  trace       = TRUE     # הצג את כל המודלים שנבדקו
)

summary(arima_auto)
# Best model: ARIMA(1,1,1)
# AIC = 123.45

# ---- שלב 4: בדיקת שגיאות ----
checkresiduals(arima_auto)
# Ljung-Box test:
# H0: השגיאות הן white noise
# p > 0.05 → המודל תקין!

# ---- שלב 5: חיזוי 12 חודשים ----
forecast_12m <- forecast(arima_auto, h = 12, level = c(80, 95))

# גרף
autoplot(forecast_12m) +
  labs(
    title    = "תחזית CPI ישראל – 12 חודשים",
    subtitle = paste("ARIMA", arima_auto$arma),
    x        = "חודש",
    y        = "מדד CPI"
  ) +
  theme_minimal()

# תוצאות
print(forecast_12m)
#           Point Forecast    Lo 80   Hi 80     Lo 95   Hi 95
# Jan 2025         112.01   111.36  112.67    111.01  113.02
# ...
```

### ARIMA עם Regressors (ARIMAX)

```r
# ARIMA עם גורם חיצוני (ריבית)
xreg_train <- matrix(cpi_monthly[1:36], ncol = 1)  # placeholder

arima_x <- auto.arima(
  cpi_ts,
  xreg = matrix(c(rep(0.1, 24), rep(3.25, 6), rep(4.75, 12)), ncol = 1)
)

summary(arima_x)
# בדוק אם הריבית כגורם חיצוני משפרת את המודל (AIC נמוך יותר?)
```

---

## חלק ג – Panel Data: Fixed Effects

### מה זה Panel Data?

**Panel** = נתונים על **כמה ישויות** (מדינות, ערים) לאורך **כמה תקופות** (שנים, רבעונים).

**יתרון:** שולטים בהטרוגניות לא נצפית (unobserved heterogeneity).

### דוגמה: גורמי אבטלה ב-OECD

```r
library(fixest)
library(tidyverse)

# נתוני Panel סינטטי: 20 מדינות × 10 שנים
set.seed(42)
n_countries <- 20
n_years     <- 10

panel_data <- tibble(
  country    = rep(paste0("C", 1:n_countries), each = n_years),
  year       = rep(2014:2023, times = n_countries),
  gdp_growth = rnorm(n_countries * n_years, 2, 2),
  inflation  = rnorm(n_countries * n_years, 2, 1.5),
  interest   = rnorm(n_countries * n_years, 2, 2),
  unemployment = 5 +
    0.5 * rep(rnorm(n_countries), each = n_years) +  # country FE
    -0.3 * rnorm(n_countries * n_years, 2, 2) +       # gdp effect
    0.2 * rnorm(n_countries * n_years, 2, 1.5) +      # inflation effect
    rnorm(n_countries * n_years, 0, 0.5)               # error
)

# ---- OLS Pooled (מתעלם מ-FE) ----
m_pooled <- lm(unemployment ~ gdp_growth + inflation + interest, data = panel_data)
summary(m_pooled)

# ---- Fixed Effects: country ----
m_fe_country <- feols(
  unemployment ~ gdp_growth + inflation + interest | country,
  data = panel_data
)
summary(m_fe_country)

# ---- Two-Way Fixed Effects: country + year ----
m_twfe <- feols(
  unemployment ~ gdp_growth + inflation + interest | country + year,
  data    = panel_data,
  cluster = ~country  # SEs clustered by country
)
summary(m_twfe)

# ---- Random Effects (אם ישים) ----
library(plm)  # install.packages("plm")
panel_plm <- pdata.frame(panel_data, index = c("country", "year"))
m_re <- plm(unemployment ~ gdp_growth + inflation + interest,
            data   = panel_plm,
            model  = "random")
summary(m_re)

# ---- Hausman Test: FE vs RE? ----
m_fe_plm <- plm(unemployment ~ gdp_growth + inflation + interest,
                data  = panel_plm,
                model = "within")
phtest(m_fe_plm, m_re)
# H0: RE עדיף (אין קורלציה בין FE לרגרסורים)
# p < 0.05 → FE עדיף!
```

### השוואת מודלים – etable

```r
etable(
  m_pooled,
  m_fe_country,
  m_twfe,
  headers    = c("Pooled OLS", "Country FE", "Country + Year FE"),
  title      = "Panel Regression: Determinants of Unemployment in OECD",
  se.below   = TRUE,
  keep       = c("gdp_growth", "inflation", "interest")
)
```

---

## חלק ד – Synthetic Control

שיטה מתקדמת לניתוח מקרה בודד (single treated unit).

```r
# install.packages("Synth") / "tidysynth"
library(tidysynth)

# דוגמה: מה קרה לצמיחה בישראל אחרי המלחמה ב-2023?
# control units: מדינות OECD דומות
# treated: ישראל

# (הדוגמה כאן עקרונית – נדרש dataset מלא)
synth_result <- panel_data %>%
  synthetic_control(
    outcome   = unemployment,
    unit      = country,
    time      = year,
    i_unit    = "C1",        # treated unit
    i_time    = 2022,        # intervention time
    generate_placebos = TRUE
  ) %>%
  generate_predictor(
    time_window = 2014:2021,
    gdp_growth  = mean(gdp_growth),
    inflation   = mean(inflation)
  ) %>%
  generate_weights() %>%
  generate_control()

synth_result %>% plot_trends()     # Treated vs. Synthetic Control
synth_result %>% plot_differences() # Gap plot
synth_result %>% plot_placebos()    # Placebo inference
```

---

## משימות השבוע

### משימה 1: DiD – השפעת מדיניות (35 נקודות)

**שאלת מחקר:** האם העלאת שכר המינימום ב-2023 הפחיתה תעסוקה?

```r
# design:
# treated = מגזרים שהמינימום הרלוונטי להם (קמעונאות, מלונאות)
# control = מגזרים עם שכר גבוה (טכנולוגיה, פיננסים)
# pre = 2021-2022, post = 2023-2024

# 1. הרץ DiD בסיסי
# 2. הרץ TWFE עם sector FE + time FE
# 3. בדוק parallel trends (event study)
# 4. stargazer() / etable()
# 5. פרש את ה-DiD estimator כלכלית
```

### משימה 2: ARIMA – תחזית אינפלציה (35 נקודות)

```r
# שלוף CPI ישראל חודשי 2015-2024 מ-API בנק ישראל (שבוע 11)
# 1. בדוק stationarity (ADF test)
# 2. ACF + PACF
# 3. auto.arima()
# 4. checkresiduals()
# 5. תחזית 6 חודשים קדימה
# 6. גרף עם CI 80% ו-95%
# 7. מה תחזית האינפלציה ל-6 חודשים?
```

### משימה 3: Panel Data OECD (30 נקודות)

```r
# שלוף נתוני OECD: unemployment + gdp_growth + inflation
# לפחות 15 מדינות × 10 שנים (שבוע 12)
# 1. Pooled OLS
# 2. Country FE
# 3. TWFE
# 4. Hausman test
# 5. etable() השוואה
# 6. מסקנה: האם שיעור צמיחה מסביר אבטלה גם בתוך-מדינות?
```

---

## הגשה

```
Members/YourName/Week_16/
├── did_analysis.R
├── arima_forecast.R
├── panel_regression.R
├── regression_tables/
│   ├── did_table.html
│   ├── panel_table.html
│   └── forecast_plot.png
└── advanced_econometrics_report.md
```

---

**השבוע הבא:** ויזואליזציה אינטראקטיבית עם Plotly (Python) → [שבוע 17](../Week_17_Visualization_Python/README.md)
