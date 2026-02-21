# שבוע 14 – Tidyverse: dplyr, tidyr ו-ggplot2

> **רמה:** בינוני – מניח שסיימת שבוע 13 (R Basics)
> **מטרת השבוע:** לשלוט ב-Tidyverse – מה שהופך R לשפה המועדפת של כלכלנים-מחקר

---

## מה זה Tidyverse?

**Tidyverse** = אוסף חבילות R שחולקות פילוסופיה ותחביר אחידים. כתובה על ידי Hadley Wickham.

```r
# חבילה אחת שמתקינה את כולן
install.packages("tidyverse")
library(tidyverse)

# כוללת:
# - dplyr   → מניפולציה של נתונים (כמו Pandas + SQL)
# - tidyr   → ניקוי ועיצוב נתונים (melt/pivot)
# - ggplot2 → ויזואליזציה
# - readr   → קריאת CSV מהיר ונכון
# - tibble  → data.frame משופר
# - stringr → עבודה עם מחרוזות
# - lubridate → עבודה עם תאריכים
# - purrr   → תכנות פונקציונלי
```

---

## חלק א – dplyr: מניפולציה של נתונים

### ה-5 פעולות הבסיסיות

```r
library(tidyverse)

# נתוני מאקרו ישראל
macro_df <- tibble(
  year         = 2018:2024,
  gdp_growth   = c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation    = c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5),
  unemployment = c(4.0, 3.8, 4.3, 5.0, 3.7, 3.5, 4.2),
  interest     = c(0.1, 0.25, 0.1, 0.1, 3.25, 4.75, 4.5),
)
```

### 1. filter() – סינון שורות

```r
# שנות צמיחה חיובית
macro_df %>% filter(gdp_growth > 0)

# שנות אינפלציה גבוהה
macro_df %>% filter(inflation > 3)

# מספר תנאים
macro_df %>% filter(gdp_growth > 0, inflation > 3)  # AND
macro_df %>% filter(gdp_growth < 0 | inflation > 5)  # OR

# שנת 2022 ומעלה
macro_df %>% filter(year >= 2022)
```

### 2. select() – בחירת עמודות

```r
# עמודות ספציפיות
macro_df %>% select(year, gdp_growth, inflation)

# הסרת עמודה
macro_df %>% select(-unemployment)

# עמודות לפי דפוס
macro_df %>% select(starts_with("g"))
macro_df %>% select(ends_with("t"))
macro_df %>% select(contains("rate"))

# סדר מחדש
macro_df %>% select(year, interest, everything())
```

### 3. mutate() – הוספת עמודות

```r
# הוסף עמודות מחושבות
macro_df <- macro_df %>%
  mutate(
    real_rate   = interest - inflation,
    gdp_index   = cumprod(1 + gdp_growth/100) * 100,  # אינדקס (בסיס 100)
    era         = if_else(year <= 2021, "ריבית נמוכה", "ריבית גבוהה"),
    status      = case_when(
      gdp_growth < 0 ~ "מיתון",
      gdp_growth < 2 ~ "צמיחה איטית",
      gdp_growth < 4 ~ "צמיחה נורמלית",
      TRUE           ~ "צמיחה גבוהה"
    )
  )

print(macro_df)
```

### 4. arrange() – מיון

```r
# מיון עולה
macro_df %>% arrange(gdp_growth)

# מיון יורד
macro_df %>% arrange(desc(inflation))

# מיון על כמה עמודות
macro_df %>% arrange(era, desc(gdp_growth))
```

### 5. summarise() + group_by() – סיכום וקיבוץ

```r
# סיכום כולל
macro_df %>%
  summarise(
    avg_gdp       = mean(gdp_growth),
    avg_inflation = mean(inflation),
    sd_gdp        = sd(gdp_growth),
    n_recession   = sum(gdp_growth < 0),
    n_years       = n()
  )

# סיכום לפי קבוצה
macro_df %>%
  group_by(era) %>%
  summarise(
    avg_gdp       = mean(gdp_growth),
    avg_inflation = mean(inflation),
    avg_interest  = mean(interest),
    avg_real_rate = mean(real_rate),
    n_years       = n()
  )

# across(): אותה פונקציה על כמה עמודות
macro_df %>%
  group_by(era) %>%
  summarise(across(where(is.numeric), mean, .names = "avg_{col}"))
```

### ה-Pipe `%>%`: שרשור פעולות

```r
# בלי pipe – קשה לקרוא
result <- summarise(group_by(filter(macro_df, year >= 2020), era), avg = mean(gdp_growth))

# עם pipe – ברור וקריא
result <- macro_df %>%
  filter(year >= 2020) %>%
  group_by(era) %>%
  summarise(avg_gdp = mean(gdp_growth)) %>%
  arrange(desc(avg_gdp))

print(result)
```

### פעולות נוספות ב-dplyr

```r
# count() – ספירה
macro_df %>% count(status)
macro_df %>% count(era, status)

# slice() – שורות לפי מיקום
macro_df %>% slice(1:3)           # שורות 1-3
macro_df %>% slice_max(gdp_growth, n = 3)  # 3 הצמיחות הגבוהות
macro_df %>% slice_min(inflation, n = 2)   # 2 האינפלציות הנמוכות

# rename()
macro_df %>% rename(growth = gdp_growth)

# distinct() – שורות ייחודיות
macro_df %>% distinct(era)
macro_df %>% distinct(status, .keep_all = TRUE)

# lag() / lead() – ערך קודם/הבא
macro_df <- macro_df %>%
  mutate(
    gdp_lag1   = lag(gdp_growth, 1),    # שנה קודמת
    gdp_change = gdp_growth - lag(gdp_growth, 1)  # שינוי
  )
```

### מיזוג: join

```r
# נתוני ייצוא
exports_df <- tibble(
  year       = c(2019, 2020, 2021, 2022, 2023, 2024),
  exports_bn = c(68.6, 58.9, 73.5, 82.1, 75.4, 78.2),
)

# inner_join (רק שורות משותפות)
combined <- macro_df %>% inner_join(exports_df, by = "year")

# left_join (כל macro, גם ללא exports)
combined <- macro_df %>% left_join(exports_df, by = "year")

# מיזוג על כמה עמודות
df1 %>% left_join(df2, by = c("year", "district"))
```

---

## חלק ב – tidyr: עיצוב נתונים

### pivot_longer() – Wide → Long

```r
# נתונים Wide (לכל מדד עמודה)
wide_data <- tibble(
  year      = 2018:2024,
  gdp       = c(4.2, 3.8, -1.9, 8.6, 6.5, 2.0, 1.1),
  inflation = c(0.8, 0.8, -0.6, 1.5, 5.1, 4.2, 3.5),
  interest  = c(0.1, 0.25, 0.1, 0.1, 3.25, 4.75, 4.5),
)

# המרה ל-Long
long_data <- wide_data %>%
  pivot_longer(
    cols      = c(gdp, inflation, interest),  # עמודות להמיר
    names_to  = "indicator",                   # שם עמודת הקטגוריה
    values_to = "value"                        # שם עמודת הערך
  )

print(long_data)
# year | indicator | value
# 2018 | gdp       | 4.2
# 2018 | inflation | 0.8
# 2018 | interest  | 0.1
# 2019 | gdp       | 3.8
# ...
```

### pivot_wider() – Long → Wide

```r
# הפוך: Long חזרה ל-Wide
wide_again <- long_data %>%
  pivot_wider(
    names_from  = "indicator",
    values_from = "value"
  )
```

### separate() ו-unite()

```r
# separate: עמודה אחת → שתיים
df <- tibble(date_label = c("2022-Q1", "2022-Q2", "2023-Q1"))
df <- df %>% separate(date_label, into = c("year", "quarter"), sep = "-")

# unite: שתי עמודות → אחת
df <- df %>% unite("date_label", year, quarter, sep = "-")
```

### drop_na() ו-fill()

```r
# הסרת שורות עם NAs
clean_df <- macro_df %>% drop_na()

# מילוי NAs
df %>% fill(gdp_growth, .direction = "down")   # מילוי מהשורה הקודמת
df %>% replace_na(list(gdp_growth = 0))         # מילוי בערך קבוע
```

---

## חלק ג – lubridate: תאריכים

```r
library(lubridate)

# המרה לתאריך
today()                     # תאריך היום
now()                       # חותמת זמן

date1 <- ymd("2024-01-15")    # yyyy-mm-dd
date2 <- dmy("15/01/2024")    # dd/mm/yyyy (ישראלי!)
date3 <- mdy("01-15-2024")    # mm-dd-yyyy (אמריקאי)

# רכיבים
year(date1)     # 2024
month(date1)    # 1
day(date1)      # 15
quarter(date1)  # 1
week(date1)     # 3

# חישובים
date1 + years(1)     # שנה קדימה
date1 - months(6)    # חצי שנה אחורה
as.numeric(date1 - date2)  # הפרש בימים

# יצירת רצף תאריכים
dates <- seq(ymd("2022-01-01"), ymd("2024-12-31"), by = "month")
```

---

## חלק ד – ggplot2: ויזואליזציה מקצועית

### הפילוסופיה: Grammar of Graphics

```r
ggplot(data = <DATA>,
       aes(x = <X>, y = <Y>, color = <COLOR>, fill = <FILL>)) +
  geom_<TYPE>() +
  labs(...) +
  theme_<THEME>()
```

### גרפים בסיסיים

```r
library(ggplot2)

# --- גרף קווי ---
ggplot(macro_df, aes(x = year, y = gdp_growth)) +
  geom_line(color = "royalblue", linewidth = 1.5) +
  geom_point(color = "royalblue", size = 3) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.5) +
  labs(
    title    = "צמיחת תמ\"ג ישראל 2018-2024",
    subtitle = "מקור: בנק ישראל",
    x        = "שנה",
    y        = "שיעור צמיחה שנתי (%)",
    caption  = "EconLab PPE"
  ) +
  theme_minimal()

# --- גרף עמודות ---
ggplot(macro_df, aes(x = year, y = gdp_growth,
                      fill = gdp_growth > 0)) +
  geom_col(show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "steelblue", "FALSE" = "tomato")) +
  labs(title = "צמיחת תמ\"ג", x = NULL, y = "%") +
  theme_minimal()

# --- scatter ---
ggplot(macro_df, aes(x = inflation, y = gdp_growth)) +
  geom_point(aes(color = era), size = 4) +
  geom_text(aes(label = year), vjust = -0.8, size = 3) +
  geom_smooth(method = "lm", se = TRUE, color = "gray40") +
  labs(title = "אינפלציה vs. צמיחה", color = "עידן") +
  theme_minimal()
```

### Facets: כמה גרפים בבת אחת

```r
# Long format נחוץ לרוב ל-facet
long_data <- macro_df %>%
  select(year, gdp_growth, inflation, interest, real_rate) %>%
  pivot_longer(-year, names_to = "indicator", values_to = "value")

# facet_wrap: גרף נפרד לכל indicator
ggplot(long_data, aes(x = year, y = value)) +
  geom_line(aes(color = indicator), linewidth = 1.5, show.legend = FALSE) +
  geom_point(aes(color = indicator), size = 2, show.legend = FALSE) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.4) +
  facet_wrap(~indicator, scales = "free_y", ncol = 2) +
  labs(title = "מדדי מאקרו ישראל 2018-2024",
       x = "שנה", y = NULL) +
  theme_minimal()
```

### עיצוב מתקדם

```r
# Economist-style theme
economist_theme <- theme_minimal() +
  theme(
    plot.title       = element_text(size = 14, face = "bold"),
    plot.subtitle    = element_text(size = 10, color = "gray50"),
    plot.caption     = element_text(size = 8, color = "gray60"),
    axis.title       = element_text(size = 10),
    panel.grid.major = element_line(color = "gray90"),
    panel.grid.minor = element_blank(),
    plot.background  = element_rect(fill = "white", color = NA),
    legend.position  = "top",
  )

# גרף עם עיצוב מקצועי + background shading
ggplot(macro_df, aes(x = year, y = gdp_growth)) +
  # הדגשת תקופת ריבית גבוהה
  annotate("rect",
           xmin = 2021.5, xmax = 2024.5,
           ymin = -Inf,   ymax = Inf,
           alpha = 0.1, fill = "red") +
  annotate("text", x = 2023, y = 9,
           label = "תקופת\nריבית גבוהה",
           color = "red", size = 3, alpha = 0.7) +
  geom_col(aes(fill = gdp_growth > 0), show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#2196F3", "FALSE" = "#F44336")) +
  scale_x_continuous(breaks = 2018:2024) +
  labs(
    title    = "צמיחת תמ\"ג ישראל – לפני ואחרי עידן הריבית הגבוהה",
    subtitle = "שיעור שינוי שנתי של התמ\"ג הריאלי",
    x        = NULL,
    y        = "% שינוי שנתי",
    caption  = "מקור: בנק ישראל | EconLab PPE"
  ) +
  economist_theme

ggsave("gdp_publication_quality.png", width = 10, height = 6, dpi = 300)
```

### ggplot2 עם Long Data – כמה סדרות

```r
# השוואת כמה מדינות
countries_data <- tibble(
  year    = rep(2019:2024, 4),
  country = rep(c("Israel", "USA", "Germany", "Japan"), each = 6),
  gdp     = c(
    3.8, -1.9, 8.6, 6.5, 2.0, 1.1,   # Israel
    2.3, -3.4, 5.9, 2.1, 2.5, 2.8,   # USA
    1.1, -4.6, 2.6, 1.8, 1.5, 0.4,   # Germany
    -0.4, -4.1, 2.1, 1.0, 1.5, 1.9,  # Japan
  )
)

ggplot(countries_data, aes(x = year, y = gdp, color = country,
                            linewidth = country == "Israel")) +
  geom_line() +
  geom_point(aes(size = country == "Israel"), show.legend = FALSE) +
  scale_linewidth_manual(values = c("TRUE" = 2, "FALSE" = 1), guide = "none") +
  scale_size_manual(values = c("TRUE" = 3, "FALSE" = 1.5)) +
  scale_color_manual(values = c(
    "Israel"  = "#0038b8",
    "USA"     = "#B22234",
    "Germany" = "#000000",
    "Japan"   = "#BC002D"
  )) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.4) +
  labs(
    title  = "GDP Growth: Israel vs. Developed Economies",
    x      = NULL, y = "% Annual Growth",
    color  = NULL,
    caption = "Source: World Bank"
  ) +
  theme_minimal() +
  theme(legend.position = "top")

ggsave("international_comparison.png", width = 10, height = 6, dpi = 300)
```

---

## חלק ה – Pipeline מלא: Tidyverse Style

```r
library(tidyverse)
library(lubridate)

# =========================================================
# STEP 1: קריאת נתונים
# =========================================================
macro_raw <- read_csv("macro_quarterly.csv", locale = locale(encoding = "UTF-8"))

# =========================================================
# STEP 2: ניקוי ועיצוב
# =========================================================
macro_clean <- macro_raw %>%
  # ניקוי שמות עמודות
  rename_with(~ str_to_lower(str_replace_all(., " ", "_"))) %>%
  # תיקון תאריכים
  mutate(date = ymd(date)) %>%
  # הסרת כפולות ו-NAs
  distinct() %>%
  drop_na(gdp_growth, inflation) %>%
  # פילטר תקין
  filter(between(gdp_growth, -20, 20),
         between(inflation, -5, 20)) %>%
  # מיון
  arrange(date)

# =========================================================
# STEP 3: הנדסת פיצ'רים
# =========================================================
macro_features <- macro_clean %>%
  mutate(
    year         = year(date),
    quarter      = quarter(date),
    real_rate    = interest - inflation,
    era          = if_else(date < ymd("2022-04-01"), "ריבית נמוכה", "ריבית גבוהה"),
    status       = case_when(
      gdp_growth < 0 ~ "מיתון",
      gdp_growth < 2 ~ "צמיחה איטית",
      TRUE           ~ "צמיחה"
    ),
    gdp_ma4      = zoo::rollmean(gdp_growth, 4, fill = NA),  # ממוצע נע 4 רבעונים
    gdp_yoy      = gdp_growth - lag(gdp_growth, 4)
  )

# =========================================================
# STEP 4: ניתוח
# =========================================================
era_summary <- macro_features %>%
  group_by(era) %>%
  summarise(
    n_quarters    = n(),
    avg_gdp       = mean(gdp_growth, na.rm = TRUE),
    avg_inflation = mean(inflation, na.rm = TRUE),
    avg_interest  = mean(interest, na.rm = TRUE),
    avg_real_rate = mean(real_rate, na.rm = TRUE),
    pct_recession = mean(gdp_growth < 0, na.rm = TRUE) * 100
  ) %>%
  arrange(era)

print(era_summary)

# =========================================================
# STEP 5: ויזואליזציה
# =========================================================
p <- macro_features %>%
  select(date, gdp_growth, inflation, real_rate) %>%
  pivot_longer(-date, names_to = "indicator", values_to = "value") %>%
  mutate(indicator = factor(indicator,
    levels = c("gdp_growth", "inflation", "real_rate"),
    labels = c("צמיחת תמ\"ג", "אינפלציה", "ריבית ריאלית"))) %>%
  ggplot(aes(x = date, y = value, color = indicator)) +
  geom_line(linewidth = 1.2) +
  geom_hline(yintercept = 0, linetype = "dashed", alpha = 0.4) +
  facet_wrap(~indicator, scales = "free_y", nrow = 3) +
  scale_color_brewer(palette = "Set1", guide = "none") +
  labs(title = "מדדי מאקרו ישראל – ניתוח רבעוני",
       x = NULL, y = NULL,
       caption = "מקור: בנק ישראל | EconLab PPE") +
  theme_minimal()

ggsave("macro_dashboard.png", p, width = 12, height = 8, dpi = 300)

# =========================================================
# STEP 6: ייצוא
# =========================================================
write_csv(macro_features, "macro_processed.csv")
cat("\n✓ Pipeline הסתיים!\n")
```

---

## משימות השבוע

### משימה 1: dplyr מלא (30 נקודות)

```r
# עם נתוני מאקרו ישראל 2010-2024:
# 1. filter(): שנים עם gdp > 3 ו-inflation < 3 (תקופת זוהר)
# 2. mutate(): gdp_index (base=100 בשנת 2010), ריבית ריאלית
# 3. group_by(era) %>% summarise(): השוואה סטטיסטית מלאה
# 4. arrange(desc(gdp_growth)) %>% slice_head(n=5): 5 שנות שיא
# 5. left_join() עם נתוני ייצוא
```

### משימה 2: tidyr + ggplot2 (35 נקודות)

```r
# 1. pivot_longer() על 4 מדדים
# 2. facet_wrap() עם scales = "free_y"
# 3. צביעה לפי era (אפקט ויזואלי!)
# 4. הוסף annotation: מלחמת אוקטובר 2023
# 5. ggsave() באיכות גבוהה (dpi = 300)
```

### משימה 3: פרויקט – דוח שוק העבודה (35 נקודות)

השתמש בנתוני CBS (אבטלה, שכר, תעסוקה לפי מחוז):

```r
# ↓ Pipeline מלא:
# read_csv() → rename_with() → drop_na() → mutate() →
# group_by(district) %>% summarise() → left_join(map_data) →
# pivot_longer() → ggplot() + facet_wrap(~district) →
# ggsave()
#
# תובנות שחייבים לענות:
# 1. איזה מחוז ראה את עליית השכר הגבוהה ביותר 2020-2024?
# 2. האם ירידת אבטלה אחרי 2021 הייתה אחידה בכל המחוזות?
```

---

## הגשה

```
Members/YourName/Week_14/
├── dplyr_basics.R
├── ggplot2_analysis.R
├── tidyverse_pipeline.R
├── macro_dashboard.png
├── gdp_publication_quality.png
└── labor_market_report.md
```

---

**השבוע הבא:** אקונומטריקה – רגרסיה לינארית ב-R → [שבוע 15](../Week_15_Econometrics_Regression/README.md)
