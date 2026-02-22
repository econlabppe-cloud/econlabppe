# משימה 10 – DSGE: מודלים מאקרו-כלכליים דינמיים


### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {.panel-tabset}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video [https://www.youtube.com/watch?v=eMOA1pPVUc4](https://www.youtube.com/watch?v=eMOA1pPVUc4) >}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video [https://www.youtube.com/watch?v=h4hOPGo4UVU](https://www.youtube.com/watch?v=h4hOPGo4UVU) >}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video [https://www.youtube.com/watch?v=Kk6piJkoIEw](https://www.youtube.com/watch?v=Kk6piJkoIEw) >}}
:::



## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=eMOA1pPVUc4 >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=0GrciaGYzV0 >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=zYttXz_59gU >}}

:::
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

### 💻 תרגול מעשי (Hands-on)

<p>לחצו על המשולש (Play) כדי להפעיל את סביבת הפיתוח בתוך העמוד, או פתחו בלשונית חדשה לנוחות מירבית.</p>
<iframe src="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_10_DSGE/starter_notebook.ipynb" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
<p><br><em>* אם המסך לא נטען או מבקש הרשאות אבטחה, <a href="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_10_DSGE/starter_notebook.ipynb" target="_blank">לחצו כאן לפתיחת המחברת במסך מלא</a>.</em></p>
---
### 🧠 בחן את עצמך (שאלות סיכום)
הגענו לשלבים המתקדמים של עיבוד נתונים בפנדס. ודאו שאתם שולטים בכלים:

<details>
<summary><b>שאלה 1: מה ההבדל בין פונקציית pd.concat לבין פונקציית pd.merge?</b> 👁️ לחץ לתשובה</summary>
<br>
<b>concat</b> משמשת לרוב ל"הדבקה" של טבלאות זו תחת זו (כמו צירוף קובץ ינואר לקובץ פברואר) או זו לצד זו, ללא צורך במפתח משותף.
<br><b>merge</b> פועלת בדיוק כמו JOIN ב-SQL - היא ממזגת טבלאות על בסיס <b>עמודת מפתח משותפת</b> (למשל, מיזוג נתוני מדינות עם נתוני תמ"ג לפי עמודת "שם המדינה").
</details>

<details>
<summary><b>שאלה 2: למה כדאי להפוך את עמודת התאריכים ל-DatetimeIndex כשעובדים עם סדרות עתיות (Time Series)?</b> 👁️ לחץ לתשובה</summary>
<br>
ברגע שהאינדקס של הטבלה הוא מסוג תאריך-זמן, פנדס פותח בפנינו יכולות קסם: אנחנו יכולים לסנן נתונים בקלות (למשל `df['2023']`), ולהשתמש בפונקציה <b>resample</b> כדי להמיר אוטומטית נתונים יומיים לממוצעים חודשיים או שנתיים בשורת קוד אחת.
</details>


---

### 💬 הערות, שאלות ודיונים
יש לכם שאלה על החומר של פרק זה? משהו לא עבד במחברת התרגול? מצאתם דרך יעילה יותר לכתוב את הקוד?
**כתבו לנו כאן למטה!** המערכת מחוברת ישירות לגיטהאב של הקורס. כל שאלה שתשאלו כאן תישמר אוטומטית בצורה מסודרת תחת נושא זה, והצוות (או סטודנטים אחרים) יוכלו לענות לכם ולעזור.
