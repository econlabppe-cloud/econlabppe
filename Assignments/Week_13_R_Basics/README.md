# שבוע 13 – R מאפס: שפת הסטטיסטיקה של כלכלנים

> **רמה:** מוחלט מאפס ב-R – מניח שסיימת מודול Python (שבועות 8-12)
> **מטרת השבוע:** ללמוד R עד הרמה שנוכל לבצע רגרסיה ולנתח נתונים כלכליים בשבועות הבאים

---

## למה ללמוד R אחרי Python?

| Python | R |
|---|---|
| שפה כללית (web, ML, automation) | שפה מיוחדת לסטטיסטיקה |
| Pandas טוב לעיבוד נתונים | Tidyverse **מעולה** לעיבוד נתונים |
| matplotlib/plotly | **ggplot2** – הגרף הכי יפה בעולם |
| statsmodels (רגרסיה) | **lm(), lmtest** – אקונומטריקה מובנית |
| חוקרים בינה מלאכותית | חוקרים בכלכלה, סטטיסטיקה, מדעי חברה |

**כלכלן מקצועי יודע את שתי השפות.**

---

## חלק א – הגדרת סביבה

### התקנה

1. **R עצמה:** [r-project.org](https://r-project.org) ← הורד עבור Windows/Mac/Linux
2. **RStudio:** [posit.co/rstudio](https://posit.co/download/rstudio-desktop/) ← ה-IDE הסטנדרטי ל-R
3. **חלופה בענן:** [posit.cloud](https://posit.cloud) – עובד בדפדפן, ללא התקנה

### מבנה RStudio

```
┌─────────────────┬───────────────────┐
│   Source Editor │   Environment     │
│  (הקוד שלך)    │  (משתנים)        │
├─────────────────┼───────────────────┤
│    Console      │     Files/Plots   │
│  (תוצאות)      │  (גרפים/קבצים)   │
└─────────────────┴───────────────────┘
```

### קיצורי מקלדת חיוניים

| קיצור | פעולה |
|---|---|
| **Ctrl+Enter** | הרץ שורה/בלוק נבחר |
| **Ctrl+Shift+Enter** | הרץ כל הסקריפט |
| **Alt+-** | הכנס `<-` (אופרטור השמה) |
| **Ctrl+Shift+C** | הפעל/כבה הערה |
| **Tab** | השלמה אוטומטית |
| **?function** | עזרה על פונקציה |

---

## חלק ב – R Console: קלחת הכימאי

פתח RStudio → Console (למטה שמאל):

```r
# R כמחשבון
2 + 2
1000 * 1.05^10      # ₪1000 ב-5% ל-10 שנים
sqrt(16)            # שורש: 4
log(100)            # לוג טבעי: 4.60
log10(100)          # לוג בסיס 10: 2
exp(1)              # e: 2.718

# בדל"ם מ-Python:
# R משתמשת ב-<- (לא =) כאופרטור השמה
# = גם עובד אבל <-  זה ה-style הנכון
```

---

## חלק ג – משתנים ו-Vectors

### אופרטור ההשמה `<-`

```r
# משתנים
gdp_growth <- 2.0
inflation  <- 4.2
year       <- 2023
country    <- "ישראל"
is_growing <- TRUE

print(gdp_growth)   # 2.0
class(gdp_growth)   # "numeric"
class(country)      # "character"
class(is_growing)   # "logical"
```

### Vector – הכלי המרכזי ב-R

ב-R, **הכל הוא vector**. אפילו מספר בודד הוא vector באורך 1.

```r
# יצירת vector עם c() (combine)
years      <- c(2018, 2019, 2020, 2021, 2022, 2023, 2024)
gdp_growth <- c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1)
inflation  <- c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5)
countries  <- c("ישראל", "ארה''ב", "גרמניה", "יפן")

# מידע על vector
length(years)          # 7
class(gdp_growth)      # "numeric"
summary(gdp_growth)    # min, max, mean, quartiles
```

### פעולות וקטוריות

```r
# פעולות מתבצעות על כל האיברים!
gdp_growth * 2           # כפל כל איבר ב-2
gdp_growth + inflation   # חיבור element-wise
gdp_growth > 0           # TRUE/FALSE לכל איבר

# ריבית ריאלית לכל שנה
interest <- c(0.1, 0.25, 0.1, 0.1, 3.25, 4.75, 4.5)
real_rate <- interest - inflation
print(real_rate)
```

### גישה לאיברים – אינדקס מ-1 !

```r
# ⚠️ ב-R, אינדקסים מתחילים מ-1 (לא 0 כמו Python!)
gdp_growth[1]        # איבר ראשון: 4.2
gdp_growth[7]        # איבר שביעי: 1.1
gdp_growth[c(1, 3, 5)]  # איברים 1, 3, 5
gdp_growth[2:5]      # איברים 2 עד 5 (כולל!)
gdp_growth[-1]       # כולם חוץ מהראשון

# גישה בתנאי (Boolean indexing)
gdp_growth[gdp_growth > 0]           # רק ערכים חיוביים
years[gdp_growth < 0]                # שנות מיתון
gdp_growth[inflation > 3]            # צמיחה בשנות אינפלציה גבוהה
```

### פונקציות וקטוריות מובנות

```r
mean(gdp_growth)       # ממוצע: 3.61
median(gdp_growth)     # חציון: 3.8
sd(gdp_growth)         # סטיית תקן
var(gdp_growth)        # שונות
min(gdp_growth)        # מינימום: -1.9
max(gdp_growth)        # מקסימום: 8.6
sum(gdp_growth)        # סכום
range(gdp_growth)      # c(min, max)
cumsum(gdp_growth)     # סכום מצטבר
cumprod(1 + gdp_growth/100)  # מכפלה מצטברת (מדד)
which.max(gdp_growth)  # אינדקס המקסימום
which.min(gdp_growth)  # אינדקס המינימום
sort(gdp_growth)       # מיון עולה
rev(gdp_growth)        # היפוך
```

---

## חלק ד – Factors, Matrices, ו-Lists

### Factor – משתנה קטגורי

```r
# Factor = קטגוריות (כמו Categorical ב-Pandas)
status <- factor(
  c("מיתון", "צמיחה", "מיתון", "צמיחה", "צמיחה"),
  levels = c("מיתון", "צמיחה"),  # סדר הרמות
)

table(status)    # ספירה לפי קטגוריה
levels(status)   # הרמות
nlevels(status)  # מספר הרמות: 2
```

### Matrix

```r
# Matrix = טבלה דו-מימדית
macro_matrix <- matrix(
  c(gdp_growth, inflation, interest),
  nrow = 7,
  ncol = 3,
  dimnames = list(years, c("GDP", "Inflation", "Interest"))
)

print(macro_matrix)
macro_matrix[3, ]   # שורה 3 (שנת 2020)
macro_matrix[, 2]   # עמודת אינפלציה
macro_matrix[2:4, 1:2]  # תת-טבלה
```

### List – אוסף מעורב

```r
# List = כמו dict ב-Python, יכול להחזיק כל טיפוס
israel_2023 <- list(
  year = 2023,
  gdp_growth = 2.0,
  inflation = 4.2,
  unemployment = 3.5,
  interest_rate = 4.75,
  cities = c("תל אביב", "ירושלים", "חיפה")
)

# גישה
israel_2023$gdp_growth      # 2.0 (עם $)
israel_2023[["inflation"]]  # 4.2 (עם [[]])
israel_2023$cities[2]       # "ירושלים"

# בדיקה
names(israel_2023)    # שמות האיברים
length(israel_2023)   # 6
```

---

## חלק ה – Data Frame: הטבלה של R

`data.frame` ב-R = `DataFrame` ב-Pandas.

```r
# יצירת data.frame
macro_df <- data.frame(
  year       = c(2018, 2019, 2020, 2021, 2022, 2023, 2024),
  gdp_growth = c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation  = c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5),
  interest   = c(0.1, 0.25, 0.1, 0.1, 3.25, 4.75, 4.5),
  stringsAsFactors = FALSE  # חשוב: לא להפוך strings ל-factors אוטומטית
)

# בדיקה ראשונה
head(macro_df)          # 6 שורות ראשונות
tail(macro_df, 3)       # 3 שורות אחרונות
str(macro_df)           # מבנה (כמו .info() ב-Pandas)
summary(macro_df)       # סטטיסטיקה (כמו .describe())
nrow(macro_df)          # מספר שורות
ncol(macro_df)          # מספר עמודות
dim(macro_df)           # c(7, 4)
colnames(macro_df)      # שמות עמודות
```

### גישה לנתונים

```r
# עמודה
macro_df$gdp_growth            # vector
macro_df[["inflation"]]        # vector
macro_df[, "interest"]         # vector

# שורות
macro_df[1, ]                  # שורה 1
macro_df[3:5, ]                # שורות 3-5

# תא ספציפי
macro_df[2, "gdp_growth"]      # 3.8

# סינון
macro_df[macro_df$gdp_growth > 0, ]              # שנות צמיחה
macro_df[macro_df$inflation > 3, c("year", "inflation")]  # שנות אינפלציה גבוהה
```

### הוספת עמודות

```r
# עמודה חדשה
macro_df$real_rate <- macro_df$interest - macro_df$inflation

# עמודה עם תנאי
macro_df$status <- ifelse(macro_df$gdp_growth > 0, "צמיחה", "מיתון")

# ifelse מקונן (שקול ל-np.select)
macro_df$era <- ifelse(
  macro_df$year <= 2021,
  "ריבית נמוכה",
  "ריבית גבוהה"
)

print(macro_df)
```

---

## חלק ו – קריאת נתונים מקבצים

```r
# CSV (הנפוץ ביותר)
df <- read.csv("macro_data.csv",
               header = TRUE,
               stringsAsFactors = FALSE,
               fileEncoding = "UTF-8")

# CSV עם פסיק ישראלי (נקודה ורגולה)
df <- read.csv2("data.csv", fileEncoding = "UTF-8-BOM")

# Excel – צריך חבילה
install.packages("readxl")
library(readxl)
df <- read_excel("data.xlsx", sheet = "annual_data")

# בדיקה מיידית
cat("שורות:", nrow(df), "\n")
cat("עמודות:", ncol(df), "\n")
cat("NAs:", sum(is.na(df)), "\n")
```

### כתיבה לקבצים

```r
# CSV
write.csv(macro_df, "output.csv", row.names = FALSE, fileEncoding = "UTF-8")

# Excel
install.packages("writexl")
library(writexl)
write_xlsx(macro_df, "output.xlsx")
```

---

## חלק ז – לולאות ופונקציות

### לולאות

```r
# for loop
for (year in years) {
  cat("שנה:", year, "\n")
}

# with index
for (i in seq_along(gdp_growth)) {
  cat(years[i], ":", gdp_growth[i], "%\n")
}

# while
balance <- 100000
rate    <- 0.05
n       <- 0
while (balance < 200000) {
  balance <- balance * (1 + rate)
  n <- n + 1
}
cat("כפלנו ב-", n, "שנים\n")

# apply משפחה (עדיפה ללולאות על vectors/data.frames)
means <- sapply(macro_df[, -1], mean)    # ממוצע לכל עמודה
sds   <- sapply(macro_df[, -1], sd)      # sd לכל עמודה
```

### פונקציות

```r
# הגדרת פונקציה
real_rate <- function(nominal, inflation) {
  return(nominal - inflation)
}

# שימוש
real_rate(4.75, 4.2)    # 0.55

# עם ברירת מחדל
future_value <- function(principal, rate, years, compound = 1) {
  principal * (1 + rate / compound)^(compound * years)
}

future_value(100000, 0.05, 10)           # 162,889
future_value(100000, 0.05, 10, 12)       # ריבית חודשית: 164,700

# פונקציה שמחזירה כמה ערכים (list)
analyze_series <- function(x) {
  list(
    mean   = mean(x, na.rm = TRUE),
    median = median(x, na.rm = TRUE),
    sd     = sd(x, na.rm = TRUE),
    min    = min(x, na.rm = TRUE),
    max    = max(x, na.rm = TRUE),
    n      = length(x)
  )
}

result <- analyze_series(gdp_growth)
cat("ממוצע:", result$mean, "\n")
cat("סטיית תקן:", result$sd, "\n")
```

---

## חלק ח – ויזואליזציה בסיסית: Base R

R מגיעה עם מערכת גרפים מובנית (Base R graphics).

```r
# הגדרת הנתונים
years      <- 2018:2024
gdp        <- c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1)
inflation  <- c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5)

# --- גרף קווי ---
plot(years, gdp,
     type = "o",          # "o" = קו + נקודות
     col  = "royalblue",
     lwd  = 2,            # עובי קו
     pch  = 19,           # צורת נקודה (19 = עיגול מלא)
     main = "צמיחת תמ\"ג ישראל 2018-2024",
     xlab = "שנה",
     ylab = "% צמיחה",
     ylim = c(-3, 10))

# הוסף קו אפס
abline(h = 0, col = "black", lty = 2)  # lty=2 = מקווקו

# הוסף קו אינפלציה
lines(years, inflation, col = "darkorange", lwd = 2, type = "o", pch = 17)

# אגדה
legend("topright",
       legend = c("צמיחת תמ\"ג", "אינפלציה"),
       col    = c("royalblue", "darkorange"),
       lwd    = 2,
       pch    = c(19, 17))

# --- גרף עמודות ---
bar_colors <- ifelse(gdp > 0, "steelblue", "tomato")
barplot(gdp,
        names.arg = years,
        col       = bar_colors,
        main      = "צמיחת תמ\"ג",
        ylab      = "% צמיחה",
        border    = "white")
abline(h = 0, col = "black")

# --- scatter ---
plot(inflation, gdp,
     pch  = 19,
     col  = "darkgreen",
     main = "אינפלציה vs. צמיחה",
     xlab = "אינפלציה (%)",
     ylab = "צמיחת תמ\"ג (%)")
text(inflation, gdp, labels = years, pos = 3, cex = 0.7)

# --- histograמ ---
hist(gdp,
     breaks = 6,
     col    = "steelblue",
     main   = "התפלגות שיעורי צמיחה",
     xlab   = "% צמיחה")

# שמירה לקובץ
png("base_macro_plot.png", width = 800, height = 600, res = 120)
# ... [קוד הגרף] ...
dev.off()
```

---

## חלק ט – ניקוי נתונים ב-Base R

```r
# נתונים עם בעיות
df <- data.frame(
  year       = c(2019, 2019, 2020, NA, 2022),
  gdp_growth = c(3.8, 3.8, NA, 8.6, 6.5),
  country    = c("  ישראל ", "ישראל", "ישראל", "ישראל", "ישראל"),
  stringsAsFactors = FALSE
)

# 1. NAs
is.na(df)              # TRUE/FALSE לכל תא
sum(is.na(df))         # סה"כ NAs
colSums(is.na(df))     # NAs לכל עמודה
df_clean <- na.omit(df)  # מחיקת שורות עם NAs
df$gdp_growth[is.na(df$gdp_growth)] <- mean(df$gdp_growth, na.rm = TRUE)  # מילוי

# 2. כפולות
duplicated(df)          # TRUE אם כפול
df_clean <- df[!duplicated(df), ]

# 3. ניקוי טקסט
df$country <- trimws(df$country)    # הסר רווחים (trim whitespace)
df$country <- toupper(df$country)   # אותיות גדולות
df$country <- tolower(df$country)   # אותיות קטנות

# 4. תיקון טיפוסים
df$year <- as.integer(df$year)
df$gdp_growth <- as.numeric(df$gdp_growth)

# 5. בדיקת ערכים חריגים
boxplot(df$gdp_growth)   # ויזואלית
outliers <- df$gdp_growth[abs(df$gdp_growth - mean(df$gdp_growth, na.rm=TRUE)) >
                           3 * sd(df$gdp_growth, na.rm=TRUE)]
```

---

## חלק י – הסתברות וסטטיסטיקה בסיסית

```r
# התפלגויות
set.seed(42)  # לשחזוריות

# Normal distribution
x <- rnorm(1000, mean = 2, sd = 1)  # 1000 נקודות
hist(x, main = "התפלגות נורמלית", col = "lightblue")

# שאלות הסתברות
pnorm(0, mean = 2, sd = 1)   # P(X < 0) = 0.0228
qnorm(0.95, mean = 2, sd = 1) # ה-95th percentile

# t-test: האם הצמיחה שונה מ-0?
gdp_growth <- c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1)
t.test(gdp_growth, mu = 0)
# p-value < 0.05 → דוחים H0, יש צמיחה מובהקת

# t-test: השוואת שתי קבוצות
pre_2022  <- c(4.2, 3.8, -1.9, 8.6)  # לפני עלייה בריבית
post_2022 <- c(6.5, 2.0, 1.1)        # אחרי עלייה בריבית
t.test(pre_2022, post_2022)

# קורלציה
cor(gdp_growth, inflation)       # מקדם קורלציה
cor.test(gdp_growth, inflation)  # עם מובהקות סטטיסטית
```

---

## משימות השבוע

### משימה 1: R Fundamentals (30 נקודות)

כתוב סקריפט `r_basics.R`:

```r
# 1. יצירת vector מאקרו ישראל 2015-2024
# 2. חישוב: ממוצע, SD, min/max של כל סדרה
# 3. מציאת שנות מיתון (gdp < 0)
# 4. מציאת שנות אינפלציה חריגה (inflation > 4%)
# 5. חישוב ריבית ריאלית לכל שנה
# 6. השוואה: ממוצע ריבית ריאלית לפני/אחרי 2022
```

### משימה 2: Data Frame Operations (35 נקודות)

כתוב `dataframe_analysis.R`:

1. קרא קובץ CSV (או צור data.frame עם 20+ שורות)
2. ניקוי: NAs, כפולות, trimws
3. הוסף עמודות: ריבית ריאלית, era, status, index קצה (base=100 לשנת 2015)
4. סינון: הדפס רק שנות "ריבית גבוהה" עם צמיחה < 3%
5. `tapply(gdp, era, mean)` – ממוצע לפי עידן

### משימה 3: ויזואליזציה (35 נקודות)

כתוב `visualization.R`:

בצע **4 גרפים** בחלון אחד (`par(mfrow = c(2,2))`):
1. קו: ריבית + CPI לאורך זמן
2. עמודות: צמיחה עם צבעים ירוק/אדום
3. scatter: ריבית ריאלית vs. צמיחה (עם labels שנה)
4. histogram: התפלגות שיעורי אינפלציה

שמור לקובץ PNG באיכות גבוהה.

---

## הגשה

```
Members/YourName/Week_13/
├── r_basics.R
├── dataframe_analysis.R
├── visualization.R
└── base_macro_plot.png
```

---

**השבוע הבא:** Tidyverse – `dplyr`, `tidyr`, `ggplot2` → [שבוע 14](../Week_14_R_Tidyverse/README.md)
