# משימה 10 – DSGE: מודלים מאקרו-כלכליים דינמיים
### 🎥 סרטון הדרכה מרכזי
צפו בסרטון הבא שמכסה את ליבת החומר הטכני של שבוע זה:
{{< video https://www.youtube.com/watch?v=eMOA1pPVUc4 >}}


> DSGE (Dynamic Stochastic General Equilibrium) הוא הכלי שבנקים מרכזיים
> (בנק ישראל, ה-Fed, ה-ECB) משתמשים בו לתחזיות ולניתוח מדיניות.

---

## מה זה DSGE?

**D**ynamic – משק מתפתח לאורך זמן
**S**tochastic – יש הלמים אקראיים (supply shocks, demand shocks)
**G**eneral **E**quilibrium – כל השווקים מאוזנים בו-זמנית

### המודל הבסיסי: RBC (Real Business Cycle)
משק עם:
- **משקי בית** (הצרכן): ממקסמים תועלת (צריכה + פנאי)
- **פירמות**: ממקסמות רווח, עם טכנולוגיה שנתונה להלמים
- **שוק עמל ושוק הון**: מתנקים בכל תקופה

---

## חלק א – התקנת gEcon (R)

```r
# gEcon – חבילת R לפתרון מודלי DSGE
install.packages("gEcon")
library(gEcon)
```

---

## חלק ב – מודל RBC בסיסי ב-gEcon

```r
library(gEcon)

# ---- הגדרת המודל ----
# gEcon קורא קבצי .gcn (model files)
# המודל כתוב בקובץ rbc_model.gcn (ראה בתיקייה)

# קמפל את המודל
rbc <- make_model("rbc_basic.gcn")

# פתרון
rbc <- steady_state(rbc)
rbc <- solve_pert(rbc, loglin = TRUE)

# Impulse Response Functions
rbc_irf <- compute_irf(rbc, var_list = c("Y", "C", "I", "L"),
                        shock_list = c("epsilon_A"),
                        periods = 20)
plot_irf(rbc_irf,
         title = "IRF: תגובת המשק להלם טכנולוגי חיובי (RBC)")
```

---

## חלק ג – קובץ מודל RBC בסיסי

צור קובץ `rbc_basic.gcn`:

```
# rbc_basic.gcn – Basic RBC Model
# EconLab PPE – Week 10

options
{
    output logfile = TRUE;
    output LaTeX = TRUE;
};

tryreduce
{
    lambda[], mu[];
};

block CONSUMER
{
    definitions
    {
        u[] = log(C[]) + chi * log(1 - L[]);
    };

    objective
    {
        U[] = u[] + beta * E[][U[1]];
    };

    controls
    {
        C[], L[], K[1];
    };

    constraints
    {
        C[] + K[1] = (1 - delta) * K[-1] + r[] * K[-1] + W[] * L[];
    };

    calibration
    {
        beta = 0.99;   # פקטור הנחה רבעוני
        chi  = 1.5;    # משקל פנאי
        delta = 0.025; # פחת רבעוני
    };
};

block FIRM
{
    objective
    {
        pi[] = A[] * K[-1]^alpha * L[]^(1 - alpha) - r[] * K[-1] - W[] * L[];
    };

    controls
    {
        K[-1], L[];
    };

    calibration
    {
        alpha = 0.36;  # נתח ההון בתמ"ג
    };
};

block TECHNOLOGY
{
    identities
    {
        A[1] = A[]^rho_A * exp(epsilon_A[1]);
        Y[]  = A[] * K[-1]^alpha * L[]^(1 - alpha);
    };

    shocks
    {
        epsilon_A[];
    };

    calibration
    {
        rho_A   = 0.95;  # התמדת הלם הטכנולוגיה
        alpha   = 0.36;
    };
};

block EQUILIBRIUM
{
    identities
    {
        Y[] = C[] + K[1] - (1 - delta) * K[-1];
    };
};
```

---

## חלק ד – פרשנות IRF

Impulse Response Function מראה: **אחרי הלם חיובי של 1% בטכנולוגיה, מה קורה לתמ"ג, צריכה, השקעות ועבודה בעוד 1, 2, ... 20 רבעונים?**

**תוצאות צפויות ב-RBC:**
- תמ"ג (Y): עולה ומתכנס בחזרה לשיווי-משקל
- צריכה (C): עולה בהדרגה (Consumption Smoothing)
- השקעות (I): עולה מיד (לנצל טכנולוגיה טובה)
- עבודה (L): **שנוי במחלוקת** – תלוי בפרמטרים

---

## חלק ה – כיול על נתוני ישראל

```r
# כיול פרמטרים על נתוני ישראל
# נתונים: World Bank / BOI
# - alpha = נתח ההון בתמ"ג ≈ 0.33 לישראל
# - delta = פחת שנתי / 4 ≈ 0.025 (רבעוני)
# - beta  = 1/(1 + ריבית ריאלית ארוכת-טווח) ≈ 0.99

# בדיקת Moments: האם המודל מתאים?
# - Variance of Output
# - Autocorrelation
# - Cross-correlation (C/Y, I/Y)
```

---

## המשימה שלך

### תרגיל 1: הבנה תיאורטית
כתוב הסבר (עברית, חצי עמוד) על:
- מהי ה-Euler Equation ב-RBC?
- למה בנקים מרכזיים מוסיפים "Nominal Rigidities" (DSGE עם New Keynesian)?

### תרגיל 2: הרצת המודל
- הרץ את מודל ה-RBC הנ"ל
- הפק IRFs לכל 4 המשתנים
- שמור כ-PNG

### תרגיל 3: שינוי פרמטר
- שנה `rho_A` (התמדת הלם) מ-0.95 ל-0.5
- מה ההבדל ב-IRF? הסבר כלכלית.

---

## הגשה

תיקייה: `Members/YourName/Week_10/`
- [ ] `rbc_basic.gcn` (קובץ המודל)
- [ ] `dsge_analysis.R` (קוד ה-R)
- [ ] `irf_technology_shock.png`
- [ ] `dsge_report.md` – ניתוח ותשובות

---

## מברכים – סיימת את המסלול!

אחרי 10 שבועות יש לך:
- ✅ Excel מקצועי
- ✅ SQL על בסיסי נתונים אמיתיים
- ✅ Python + Pandas + APIs
- ✅ R + אקונומטריקה
- ✅ ויזואליזציה ידידותית לקובעי מדיניות
- ✅ Power BI / Tableau
- ✅ מודל DSGE מוריץ

**זה תיק העבודות שלך. הצג אותו.**
