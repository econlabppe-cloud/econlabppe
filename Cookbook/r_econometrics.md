# Cookbook: R לאקונומטריקה

> מדריך R מהיר לכלכלנים – מרגרסיה בסיסית ועד DiD ו-ARIMA.
> כל הקוד מוכן להרצה ב-RStudio.

---

## הכנה: חבילות נדרשות

```r
# הרץ פעם אחת:
install.packages(c(
  "tidyverse",   # dplyr, ggplot2, tidyr
  "lmtest",      # בדיקות אבחון
  "sandwich",    # Robust Standard Errors
  "forecast",    # ARIMA, time series
  "stargazer",   # טבלאות רגרסיה יפות
  "patchwork",   # שילוב ggplot2 panels
  "fixest"       # רגרסיה Fixed Effects (מהיר)
))
```

---

## 1. רגרסיה לינארית בסיסית

```r
library(tidyverse)

# נתונים
df <- tibble(
  year         = 2010:2024,
  gdp_growth   = c(5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                   -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation    = c(2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                   -0.6, 1.5, 5.1, 4.2, 3.5),
  interest_rate = c(1.5, 2.5, 2.25, 1.5, 0.25, 0.1, 0.1, 0.1, 0.1, 0.25,
                    0.1, 0.1, 3.25, 4.75, 4.5)
)

# מודל 1: אינפלציה ~ ריבית
m1 <- lm(inflation ~ interest_rate, data = df)
summary(m1)
# Estimate (interest_rate): כל עלייה של 1% בריבית → שינוי X% באינפלציה

# מודל 2: מרובת משתנים
m2 <- lm(inflation ~ interest_rate + gdp_growth, data = df)
summary(m2)

# השוואת מודלים
AIC(m1, m2)
BIC(m1, m2)
```

---

## 2. טבלת רגרסיה יפה (stargazer)

```r
library(stargazer)

stargazer(m1, m2,
          type = "text",           # "html" לשמירה בקובץ
          title = "Determinants of Inflation – Israel 2010-2024",
          dep.var.labels = "Inflation (%)",
          covariate.labels = c("Interest Rate", "GDP Growth"),
          omit.stat = c("f", "ser"),
          digits = 3)
```

---

## 3. Robust Standard Errors

```r
library(lmtest)
library(sandwich)

# בדיקת הטרוסקדסטיות
bptest(m2)
# אם p < 0.05: יש הטרוסקדסטיות → השתמש ב-Robust SE

# תיקון: HC3 Robust SE
coeftest(m2, vcov = vcovHC(m2, type = "HC3"))
```

---

## 4. Difference-in-Differences (DiD)

```r
# דוגמה: הערכת השפעת מדיניות על שוק הדיור
# נניח שיש לנו נתונים על ערים עם/בלי מדיניות

# בניית נתונים דמויי-פנל
set.seed(42)
df_panel <- expand_grid(city = paste0("city_", 1:20),
                        year = 2018:2024) |>
  mutate(
    treated   = city %in% paste0("city_", 1:10),   # 10 ערים "טופלו"
    post      = year >= 2022,
    did       = as.integer(treated & post),
    house_price = 100 +
                  10 * treated +           # הפרש בסיסי
                  5  * post +              # מגמה כללית
                  8  * did +               # אפקט הטיפול (האמת)
                  rnorm(n(), sd = 5)       # רעש
  )

# מודל DiD
did_model <- lm(house_price ~ treated + post + did, data = df_panel)
summary(did_model)
# המקדם של did הוא האומדן שלנו לאפקט המדיניות
# אמור להיות קרוב ל-8

# עם Fixed Effects (עדיף בפנל):
library(fixest)
fe_model <- feols(house_price ~ did | city + year, data = df_panel)
summary(fe_model)
```

---

## 5. סדרות עתיות: ARIMA

```r
library(forecast)

# צור אובייקט time series
inflation_ts <- ts(df$inflation, start = 2010, frequency = 1)

# ACF ו-PACF לאבחון
par(mfrow = c(1, 2))
acf(inflation_ts, main = "ACF – Autocorrelation")
pacf(inflation_ts, main = "PACF – Partial Autocorrelation")

# ARIMA אוטומטי
model_arima <- auto.arima(inflation_ts, stepwise = FALSE,
                          approximation = FALSE)
print(model_arima)

# חיזוי
fc <- forecast(model_arima, h = 3)
autoplot(fc) +
  labs(title = "תחזית אינפלציה ישראל 2025–2027",
       x = "שנה", y = "אינפלציה %") +
  theme_minimal()
```

---

## 6. Panel Data עם fixest

```r
library(fixest)

# נניח שיש נתוני פנל: מדינות × שנים
df_countries <- tibble(
  country = rep(c("ISR", "USA", "DEU", "GBR"), each = 10),
  year    = rep(2015:2024, 4),
  inflation = c(
    c(0.0, 0.5, 1.2, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5, 3.0),  # ISR
    c(0.7, 2.1, 2.1, 2.4, 1.2, 4.7, 8.0, 4.1, 3.4, 2.9),  # USA
    c(0.2, 1.7, 1.6, 1.8, 0.5, 3.1, 8.7, 5.9, 2.5, 2.1),  # DEU
    c(0.0, 1.0, 2.7, 2.5, 1.8, 2.5, 9.1, 7.3, 2.6, 2.3)   # GBR
  ),
  interest_rate = runif(40, 0, 5)
)

# Fixed Effects: שולטים על הבדלים קבועים בין מדינות ובין שנים
fe <- feols(inflation ~ interest_rate | country + year,
            data = df_countries,
            vcov = "twoway")  # Clustered SE
summary(fe)
etable(fe)  # טבלה נקייה
```

---

## שגיאות נפוצות ב-R

| שגיאה | משמעות | פתרון |
|---|---|---|
| `object 'df' not found` | הרצת הקוד בסדר שגוי | הרץ שוב מהתחלה |
| `package 'X' not installed` | חבילה חסרה | `install.packages("X")` |
| `NA introduced by coercion` | המרת טקסט למספר נכשלה | בדוק עמודת המקור |
| `singular fit` | Multicollinearity | הסר משתנה אחד |

---

*עודכן: 2025*
