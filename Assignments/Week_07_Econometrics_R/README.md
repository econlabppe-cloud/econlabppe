# משימה 7 – R: אקונומטריקה מעשית


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=Ww71knvhQ-s](https://www.youtube.com/watch?v=Ww71knvhQ-s) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=cNgMWD2mMWU](https://www.youtube.com/watch?v=cNgMWD2mMWU) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=zAmJTGEGzAM](https://www.youtube.com/watch?v=zAmJTGEGzAM) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=cNgMWD2mMWU >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=Ww71knvhQ-s >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=zAmJTGEGzAM >}}

:::
## חלק א – רגרסיה לינארית: `lm()`

```r
library(tidyverse)

# נתוני מאקרו ישראל
df <- data.frame(
  year         = 2010:2024,
  gdp_growth   = c(5.7, 5.1, 3.0, 4.2, 3.5, 2.5, 4.0, 3.5, 3.5, 3.8,
                   -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation    = c(2.7, 2.2, 1.6, 1.5, -0.5, -1.0, 0.0, 0.5, 1.2, 0.8,
                   -0.6, 1.5, 5.1, 4.2, 3.5),
  unemployment = c(6.6, 5.6, 6.9, 6.3, 6.0, 5.3, 4.8, 4.3, 4.0, 3.8,
                   4.3, 5.0, 3.7, 3.5, 4.2),
  interest_rate = c(1.5, 2.5, 2.25, 1.5, 0.25, 0.1, 0.1, 0.1, 0.1, 0.25,
                    0.1, 0.1, 3.25, 4.75, 4.5)
)

# ---- רגרסיה: האם ריבית מסבירה אינפלציה? ----
model1 <- lm(inflation ~ interest_rate, data = df)
summary(model1)

# פרשנות:
# Estimate (Intercept): אינפלציה בסיסית כשריבית = 0
# Estimate (interest_rate): השפעה של עלייה ב-1% בריבית על האינפלציה
# R-squared: כמה % מהשונות מוסבר

# ---- רגרסיה מרובת משתנים ----
model2 <- lm(inflation ~ interest_rate + unemployment + gdp_growth, data = df)
summary(model2)

# השוואת מודלים
AIC(model1, model2)  # מודל עם AIC נמוך יותר עדיף
```

---

## חלק ב – Difference-in-Differences (DiD)

שיטה להערכת השפעת מדיניות. **הרעיון:** השווה קבוצה שחוותה שינוי מדיניות לקבוצה שלא.

```r
# דוגמה: האם עליית הריבית ב-2022 הפחיתה אינפלציה?
# "טיפול": שנים 2022-2024 (ריבית גבוהה)
# "ביקורת": שנים 2018-2021 (ריבית נמוכה)

df_did <- df |>
  filter(year >= 2018) |>
  mutate(
    post_treatment = if_else(year >= 2022, 1, 0),
    treatment      = 1  # כאן ישראל = הקבוצה היחידה
    # בניתוח אמיתי: צריך קבוצת ביקורת (מדינה אחרת)
  )

did_model <- lm(inflation ~ post_treatment, data = df_did)
summary(did_model)

# הערה: DiD אמיתי דורש Parallel Trends Assumption –
# שתי הקבוצות היו "מתנהגות אותו דבר" ללא הטיפול
```

---

## חלק ג – סדרות עתיות: ARIMA

```r
# install.packages("forecast")
library(forecast)

# צור אובייקט ts (time series)
inflation_ts <- ts(df$inflation, start = 2010, frequency = 1)

# חיזוי עם ARIMA אוטומטי
model_arima <- auto.arima(inflation_ts)
print(model_arima)

# חיזוי ל-3 שנים קדימה
forecast_3y <- forecast(model_arima, h = 3)
plot(forecast_3y,
     main = "תחזית אינפלציה 2025-2027 (ARIMA)",
     xlab = "שנה", ylab = "אינפלציה %")

# שמור את התחזית
print(forecast_3y)
```

---

## חלק ד – בדיקות אבחון

```r
# ---- בדיקת שאריות (Residuals) ----
par(mfrow = c(2, 2))
plot(model2)  # 4 גרפי אבחון אוטומטיים

# ---- בדיקת נורמליות (Shapiro-Wilk) ----
shapiro.test(residuals(model2))
# p > 0.05: השאריות נורמליות (טוב)

# ---- Heteroskedasticity (Breusch-Pagan) ----
# install.packages("lmtest")
library(lmtest)
bptest(model2)
# p < 0.05: יש הטרוסקדסטיות – צריך SE חזקים (robust SE)

# ---- תיקון עם Robust Standard Errors ----
# install.packages("sandwich")
library(sandwich)
library(lmtest)
coeftest(model2, vcov = vcovHC(model2, type = "HC3"))
```

---

## המשימה שלך

### תרגיל 1: רגרסיה
הרץ רגרסיה שבה:
- משתנה תלוי: `gdp_growth`
- משתנים מסבירים: `interest_rate`, `inflation`, `unemployment`

פרש את התוצאות:
- מה אומר המקדם של `interest_rate`?
- מה ה-R²? מה המשמעות שלו כאן?

### תרגיל 2: ARIMA
- הרץ ARIMA על `gdp_growth`
- הצג תחזית ל-2025–2027
- האם התחזית הגיונית? מדוע?

### תרגיל 3: שאלה כלכלית
בחר **מדינה אחת** מ-OECD (נתונים מ-World Bank).
הרץ רגרסיה בין הריבית לאינפלציה שם.
השווה ל-ישראל: האם התוצאות דומות?

---

## הגשה

תיקייה: `Members/YourName/Week_07/`
- [ ] `econometrics.R` – כל הקוד
- [ ] `results.md` – פרשנות התוצאות (3-5 משפטים לכל מודל)

---

**השבוע הבא:** ויזואליזציה → [משימה 8](../Week_08_Visualization/README.md)

### 💻 תרגול מעשי (Hands-on)

<p>לחצו על המשולש (Play) כדי להפעיל את סביבת הפיתוח בתוך העמוד, או פתחו בלשונית חדשה לנוחות מירבית.</p>
<iframe src="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_07_Econometrics_R/starter_notebook.ipynb" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
<p><br><em>* אם המסך לא נטען או מבקש הרשאות אבטחה, <a href="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_07_Econometrics_R/starter_notebook.ipynb" target="_blank">לחצו כאן לפתיחת המחברת במסך מלא</a>.</em></p>
