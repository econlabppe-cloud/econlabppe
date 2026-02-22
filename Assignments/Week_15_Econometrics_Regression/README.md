# שבוע 15 – אקונומטריקה: רגרסיה לינארית ב-R
### 🎥 סרטון הדרכה מרכזי
צפו בסרטון הבא שמכסה את ליבת החומר הטכני של שבוע זה:
{{< video https://www.youtube.com/watch?v=66z_MRkVZVw >}}


> **רמה:** בינוני-מתקדם – מניח שסיימת שבועות 13-14 (R + Tidyverse)
> **מטרת השבוע:** לבצע רגרסיה לינארית כלכלית נכונה – מהיפותזה עד טבלת תוצאות לפרסום

---

## מה זה אקונומטריקה?

**אקונומטריקה** = שימוש בסטטיסטיקה לבדיקת תיאוריות כלכליות עם נתונים.

השאלות שנענה השבוע:
- האם ריבית גבוהה מקטינה צמיחה? (בכמה? ובמובהקות?)
- האם אינפלציה קשורה לייצוא?
- אילו גורמים מסבירים מחירי דיור?
- האם ישנה בעיית רב-קוליניאריות?

---

## חלק א – OLS: רגרסיה לינארית רגילה

### הגדרת המודל

```
Y = β₀ + β₁X₁ + β₂X₂ + ... + ε

Y    = משתנה תלוי (dependent)
X    = משתנים בלתי-תלויים (independent/regressors)
β    = מקדמי הרגרסיה (אותם נרצה לאמוד)
ε    = שגיאה (מה המודל לא מסביר)
```

### lm(): פונקציית הרגרסיה של R

```r
library(tidyverse)
library(broom)      # לניקוי תוצאות lm()

# נתוני מאקרו
macro <- tibble(
  year         = 2000:2023,
  gdp_growth   = c(9.0, -0.5, -0.6, 1.7, 4.8, 5.1, 5.6, 5.3, 4.0, 0.8,
                    5.7, 4.6, 3.0, 4.2, 3.3, 2.5, 4.0, 3.4, 3.5, 3.8,
                    -1.9, 8.6, 6.5, 2.0),
  inflation    = c(1.1, 1.1, 5.7, 0.7, -0.4, 1.3, 2.1, 0.5, 4.6, 3.3,
                    2.7, 0.5, 1.6, 1.5, 0.5, -1.0, 0.0, 0.2, 0.8, 0.8,
                    -0.6, 1.5, 5.1, 4.2),
  interest     = c(10.0, 5.8, 3.8, 2.7, 4.2, 3.7, 5.1, 4.0, 4.1, 0.5,
                    1.5, 3.2, 2.5, 1.7, 0.25, 0.1, 0.1, 0.1, 0.1, 0.25,
                    0.1, 0.1, 3.25, 4.75),
  unemployment = c(8.8, 9.4, 10.3, 10.7, 10.4, 9.0, 8.4, 7.3, 6.1, 7.6,
                    6.7, 5.6, 6.9, 6.3, 5.9, 5.3, 4.8, 4.3, 4.0, 3.8,
                    4.3, 5.0, 3.7, 3.5),
)

# --- רגרסיה פשוטה: האם ריבית מסבירה אבטלה? ---
model_simple <- lm(unemployment ~ interest, data = macro)

# תוצאות
summary(model_simple)
```

### קריאת תוצאות summary()

```
Call:
lm(formula = unemployment ~ interest, data = macro)

Residuals:
    Min      1Q  Median      3Q     Max
-3.2485 -1.0556 -0.1234  0.9901  4.2376

Coefficients:
             Estimate Std. Error t value Pr(>|t|)
(Intercept)   5.0421     0.5612   8.986  < 2e-16 ***
interest      0.3182     0.1124   2.831   0.0097 **

Signif. codes: 0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 1.842 on 22 degrees of freedom
Multiple R-squared: 0.267,  Adjusted R-squared: 0.232
F-statistic: 8.015 on 1 and 22 DF,  p-value: 0.009694
```

**פרשנות:**
- `interest: Estimate = 0.318` → עלייה של 1% בריבית קשורה לעלייה של 0.32% באבטלה
- `Pr(>|t|) = 0.0097 **` → מובהק ברמה 1% (p < 0.01)
- `R-squared = 0.267` → הריבית מסבירה 26.7% מהשונות באבטלה

### כוכביות המובהקות

| *** | ** | * | . | (ריק) |
|---|---|---|---|---|
| p < 0.001 | p < 0.01 | p < 0.05 | p < 0.1 | p > 0.1 |
| מובהק מאוד | מובהק | מובהק | גבולי | לא מובהק |

---

## חלק ב – רגרסיה מרובה

```r
# --- מודל מרובה: מה מסביר צמיחה? ---
model_multi <- lm(
  gdp_growth ~ interest + inflation + unemployment,
  data = macro
)

summary(model_multi)

# --- השוואת מודלים ---
model1 <- lm(gdp_growth ~ interest, data = macro)
model2 <- lm(gdp_growth ~ interest + inflation, data = macro)
model3 <- lm(gdp_growth ~ interest + inflation + unemployment, data = macro)

# AIC / BIC – מדד התאמה (קטן יותר = טוב יותר)
AIC(model1, model2, model3)
BIC(model1, model2, model3)

# anova() – האם המודל המרובה טוב יותר?
anova(model1, model2, model3)
```

### tidy() מה-broom package

```r
library(broom)

# tidy: מקדמים + מובהקות כ-tibble
tidy(model_multi)
# # A tibble: 4 × 5
#   term         estimate std.error statistic  p.value
#   <chr>           <dbl>     <dbl>     <dbl>    <dbl>
# 1 (Intercept)    11.19      2.31       4.85  7.55e-5
# 2 interest       -0.354     0.119     -2.97  6.79e-3
# 3 inflation      -0.312     0.215     -1.45  1.61e-1
# 4 unemployment   -0.984     0.359     -2.74  1.21e-2

# glance: R², F-stat, AIC כ-tibble
glance(model_multi)

# augment: תחזיות + שגיאות ל-data.frame
aug <- augment(model_multi, data = macro)
print(aug)
# כולל: .fitted (ערכים מותאמים), .resid (שגיאות), .hat, .cooksd
```

---

## חלק ג – בדיקת ההנחות

### 1. ליניאריות – Residuals vs. Fitted

```r
par(mfrow = c(2, 2))
plot(model_multi)
# גרף 1: Residuals vs Fitted – בדוק ליניאריות
# גרף 2: Normal Q-Q – בדוק נורמליות שגיאות
# גרף 3: Scale-Location – בדוק הומוסקדסטיות
# גרף 4: Cook's Distance – זיהוי outliers משפיעים

par(mfrow = c(1, 1))

# עם ggplot2
library(ggfortify)
autoplot(model_multi) + theme_minimal()
```

### 2. נורמליות שגיאות – Shapiro-Wilk

```r
residuals_vec <- residuals(model_multi)

shapiro.test(residuals_vec)
# H0: השגיאות מתפלגות נורמלית
# אם p > 0.05 → לא דוחים H0 (נורמלי)

# ויזואלי
ggplot(data.frame(res = residuals_vec), aes(x = res)) +
  geom_histogram(bins = 8, fill = "steelblue", alpha = 0.8) +
  geom_density(aes(y = ..count..), color = "red", linewidth = 1) +
  labs(title = "התפלגות שגיאות הרגרסיה") +
  theme_minimal()
```

### 3. הומוסקדסטיות – Breusch-Pagan

```r
library(lmtest)

bptest(model_multi)
# H0: שונות השגיאות קבועה (הומוסקדסטיות)
# p < 0.05 → הטרוסקדסטיות (בעיה!)
```

### 4. רב-קוליניאריות – VIF

```r
library(car)

vif(model_multi)
# VIF > 5  → קוליניאריות מתונה
# VIF > 10 → קוליניאריות חמורה – בעיה!

# בדיקת קורלציות בין משתנים
macro %>%
  select(interest, inflation, unemployment) %>%
  cor() %>%
  round(3)
```

### 5. אוטוקורלציה – Durbin-Watson

```r
library(lmtest)

dwtest(model_multi)
# DW ≈ 2    → אין אוטוקורלציה
# DW < 1.5  → אוטוקורלציה חיובית (בעיה!)
# DW > 2.5  → אוטוקורלציה שלילית

# תוספת: Breusch-Godfrey (יותר מדויק)
bgtest(model_multi, order = 2)
```

---

## חלק ד – שגיאות סטנדרטיות חזקות (Robust SE)

כשיש הטרוסקדסטיות, נשתמש בשגיאות HC (Heteroscedasticity-Consistent).

```r
library(lmtest)
library(sandwich)

# OLS רגיל
model <- lm(gdp_growth ~ interest + inflation + unemployment, data = macro)

# שגיאות HC3 (הנפוצות ביותר)
coeftest(model, vcov = vcovHC(model, type = "HC3"))

# HC0, HC1, HC2, HC3, HC4 – וריאנטים שונים
# HC3 = המומלץ ברוב המקרים

# NeweyWest – לסדרות עתיות (מטפל גם באוטוקורלציה)
coeftest(model, vcov = NeweyWest(model))
```

---

## חלק ה – stargazer: טבלות לפרסום

```r
install.packages("stargazer")
library(stargazer)

# שלושה מודלים
m1 <- lm(gdp_growth ~ interest, data = macro)
m2 <- lm(gdp_growth ~ interest + inflation, data = macro)
m3 <- lm(gdp_growth ~ interest + inflation + unemployment, data = macro)

# טבלה למסך (text)
stargazer(m1, m2, m3,
          type     = "text",
          title    = "גורמי צמיחת תמ\"ג – ישראל 2000-2023",
          dep.var.labels = "GDP Growth (%)",
          covariate.labels = c("Interest Rate", "Inflation", "Unemployment"),
          omit.stat = c("f", "ser"),
          no.space  = TRUE)

# HTML (לפרסום בדוח)
stargazer(m1, m2, m3,
          type     = "html",
          out      = "regression_table.html",
          title    = "Determinants of GDP Growth – Israel 2000–2023",
          dep.var.labels  = "GDP Growth (%)",
          covariate.labels = c("Interest Rate (%)", "Inflation (%)", "Unemployment (%)"),
          add.lines = list(
            c("Robust SE", "No", "No", "No"),
            c("Year FE",   "No", "No", "No")
          ),
          notes.append = FALSE,
          notes = "HC3 robust standard errors in parentheses. *** p<0.01, ** p<0.05, * p<0.1")
```

**תוצאה:**
```
=================================================
                   Dependent variable:
               ----------------------------------
                          gdp_growth
                   (1)        (2)        (3)
-------------------------------------------------
interest         -0.239     -0.215     -0.354**
                (0.197)    (0.196)    (0.119)
inflation                   -0.228     -0.312
                            (0.240)   (0.215)
unemployment                           -0.984**
                                      (0.359)
Constant        4.103***   4.419***   11.191***
               (0.725)    (0.749)    (2.306)
-------------------------------------------------
Observations      24         24         24
R²              0.053      0.099      0.332
Adjusted R²     0.011      0.015      0.230
=================================================
```

---

## חלק ו – ניבוי ותחזית

```r
# ניבוי על נתוני train
aug <- augment(model_multi, data = macro)
aug %>%
  ggplot(aes(x = year)) +
  geom_line(aes(y = gdp_growth, color = "בפועל"), linewidth = 1.5) +
  geom_line(aes(y = .fitted, color = "מודל"), linewidth = 1.5, linetype = "dashed") +
  geom_ribbon(aes(ymin = .fitted - 1.96*.se.fit,
                  ymax = .fitted + 1.96*.se.fit), alpha = 0.2, fill = "steelblue") +
  scale_color_manual(values = c("בפועל" = "black", "מודל" = "steelblue")) +
  labs(title = "צמיחת תמ\"ג: בפועל מול מודל OLS", color = NULL) +
  theme_minimal()

# ניבוי על נתוני out-of-sample
new_data <- tibble(
  interest     = c(3.5, 3.0, 2.5),
  inflation    = c(3.0, 2.5, 2.0),
  unemployment = c(4.0, 3.8, 3.5)
)

predictions <- predict(model_multi, newdata = new_data,
                       interval = "prediction", level = 0.95)
cbind(new_data, predictions)
#   interest inflation unemployment     fit    lwr    upr
# 1      3.5       3.0          4.0   2.35  -2.18   6.88
```

---

## חלק ז – רגרסיה עם Dummy Variables

```r
# משתנה ממין (dummy)
macro <- macro %>%
  mutate(
    post_covid      = as.integer(year >= 2021),
    high_inflation  = as.integer(inflation > 3),
    era_factor      = factor(if_else(year <= 2021, "low_rates", "high_rates"))
  )

# מודל עם dummy
model_dummy <- lm(gdp_growth ~ interest + inflation + post_covid, data = macro)
summary(model_dummy)

# interaction term (אינטראקציה)
model_interact <- lm(
  gdp_growth ~ interest * era_factor + inflation,
  data = macro
)
# interest:era_factorhigh_rates = האם האפקט של הריבית שונה בתקופת ריבית גבוהה?
summary(model_interact)
```

---

## משימות השבוע

### משימה 1: רגרסיה בסיסית (25 נקודות)

```r
# שאלת מחקר: מה מסביר שיעור האבטלה בישראל?
# X1: gdp_growth, X2: interest, X3: inflation
# 1. הרץ OLS רגיל
# 2. בדוק VIF – יש רב-קוליניאריות?
# 3. בדוק Breusch-Pagan – יש הטרוסקדסטיות?
# 4. בדוק Durbin-Watson – יש אוטוקורלציה?
# 5. אם יש בעיות – השתמש ב-HC3 robust SE
```

### משימה 2: השוואת מודלים (35 נקודות)

```r
# שאלת מחקר: מה מסביר מחירי דיור בישראל?
# נתונים: house_price_index ~ interest + gdp + construction_starts + wage
# 1. 4 מודלים: m1 (interest), m2 (+gdp), m3 (+construction), m4 (+wage)
# 2. AIC/BIC comparison table
# 3. anova() test
# 4. stargazer() table
# 5. גרף: actual vs. fitted של המודל הטוב ביותר
```

### משימה 3: רגרסיה עם Dummies (40 נקודות)

```r
# שאלת מחקר: האם הריבית הגבוהה (post-2022) שינתה את הקשר בין ריבית לצמיחה?
# שימוש: interaction term: interest * post_2022
# 1. הרץ מודל עם interaction
# 2. פרש: האם המקדם של interaction מובהק?
# 3. Marginal effect plot: מה האפקט של ריבית בכל תקופה?
# 4. stargazer() עם כל המודלים
# 5. דוח קצר: מה הממצא הכלכלי?
```

---

## הגשה

```
Members/YourName/Week_15/
├── ols_basics.R
├── model_comparison.R
├── dummy_interaction.R
├── regression_results.html
└── regression_findings.md
```

**בדוח `regression_findings.md`:**
```markdown
## ממצאים: גורמי צמיחת תמ"ג בישראל

### 1. שאלת מחקר
### 2. מתודולוגיה
### 3. תוצאות עיקריות (הפנה לטבלת stargazer)
### 4. בדיקות אבחון (נורמליות, הטרוסקדסטיות, אוטוקורלציה)
### 5. מסקנה כלכלית
```

---

**השבוע הבא:** DiD, ARIMA ו-Panel Data → [שבוע 16](../Week_16_Econometrics_Advanced/README.md)
