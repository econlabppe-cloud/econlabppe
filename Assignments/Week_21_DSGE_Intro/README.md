# שבוע 21 – מבוא ל-DSGE: מודלים מאקרו-כלכליים דינמיים

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=KtYVbdiiCHo >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=H7R75Boz6XU >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=8I_n_pX-q9g >}}

:::
## מה זה DSGE?

**Dynamic Stochastic General Equilibrium**:

| מילה | משמעות |
|---|---|
| **Dynamic** | המשק מתפתח לאורך זמן (period by period) |
| **Stochastic** | יש הלמים אקראיים (technology shocks, policy shocks) |
| **General Equilibrium** | כל השווקים בשיווי משקל בו-זמנית |

**DSGE = המודל שבנקים מרכזיים ו-IMF משתמשים בו לניתוח מדיניות.**

---

## מה DSGE עושה שרגרסיה לא עושה?

| רגרסיה OLS | DSGE |
|---|---|
| מתאר קשרים עבר | **מדמה** את כל הכלכלה |
| "ריבית קשורה לצמיחה" | "מה יקרה לצמיחה אם ריבית תעלה ב-1%?" |
| לא ניתן להשתמש בניתוח מדיניות | **ניתוח מדיניות נגדית** |
| Lucas Critique | עמיד ל-Lucas Critique |

**Lucas Critique**: פרמטרים שנאמדים מנתונים עבר ישתנו לאחר שינוי מדיניות.

---

## חלק א – בלוקי הבניין של DSGE

### 1. Households (משקי בית)

משק הבית פותר בעיית מקסום תועלת:

```
max E₀[Σᵢ βᵗ U(Cₜ, Lₜ)]

כפוף ל:
Cₜ + Iₜ = Yₜ = Wₜ·Hₜ + Rₜ·Kₜ

C = צריכה, L = פנאי, I = השקעה
K = הון, W = שכר, R = תשואת הון
β = discount factor (0 < β < 1)
```

תנאי First Order (Euler Equation):
```
U_C(t) = β·E[U_C(t+1)·(Rₜ₊₁ + 1 - δ)]
```

### 2. Firms (פירמות)

פירמה פותרת מקסום רווח:

```
max Yₜ - Wₜ·Hₜ - Rₜ·Kₜ

Yₜ = Aₜ·Kₜᵅ·Hₜ^(1-α)   [Cobb-Douglas]

A = total factor productivity (TFP)
α = capital share (~0.33)
```

תנאי First Order:
```
Wₜ = (1-α)·Yₜ/Hₜ   (שכר = MPHL)
Rₜ = α·Yₜ/Kₜ       (תשואת הון = MPK)
```

### 3. Technology Shock (הלם טכנולוגי)

```
log(Aₜ) = ρ·log(Aₜ₋₁) + εₜ,   εₜ ~ N(0, σ²)

ρ = persistence (0 < ρ < 1)
ε = white noise shock
```

### 4. Market Clearing

```
Yₜ = Cₜ + Iₜ           (שוק מוצרים)
Hₜ = H̄ = 1             (שוק עבודה – נרמול)
Kₜ₊₁ = (1-δ)·Kₜ + Iₜ  (צבירת הון)
```

---

## חלק ב – RBC: Real Business Cycle Model

**RBC** = המודל DSGE הבסיסי ביותר. ניר Kydland ו-Prescott (נובל 2004).

**הרעיון:** מחזורי עסקים נובעים מהלמי טכנולוגיה (TFP shocks), **לא** מכשלי שוק.

### פתרון RBC: Log-Linearization

ליד ה-Steady State:

```
Steady State:
R* = 1/β - (1-δ)           (ריבית ריאלית)
K*/Y* = α·β/(1-β(1-δ))     (יחס הון-תוצרת)
C*/Y* = 1 - δ·K*/Y*        (יחס צריכה)

Log-linearized equations (hat = % deviation from SS):
ĉₜ = Eₜ[ĉₜ₊₁] - (R*/σ)·(rₜ - ρᶜ)    [Euler]
yₜ = α·kₜ + (1-α)·hₜ + aₜ             [Production]
yₜ = (C*/Y*)·cₜ + (I*/Y*)·iₜ          [Resource constraint]
aₜ = ρ·aₜ₋₁ + εₜ                       [Technology]
```

---

## חלק ג – DSGE ב-R: חבילת `gEcon`

```r
# התקנה
install.packages("gEcon")
library(gEcon)
```

### מודל RBC ב-gEcon

שמור כ-`rbc_model.gcn`:

```
# rbc_model.gcn

options
{
    output logfile = TRUE;
    output LaTeX = FALSE;
};

tryreduce
{
    # Reduce steady state variables
};

block HOUSEHOLD
{
    definitions
    {
        u[] = C[]^(1-sigma) / (1-sigma) - chi * H[]^(1+phi) / (1+phi);
    };

    controls
    {
        C[], H[], I[], K[];
    };

    objective
    {
        U[] = u[] + beta * E[][U[1]];
    };

    constraints
    {
        C[] + I[] = W[] * H[] + R[] * K[-1];
        K[] = (1 - delta) * K[-1] + I[];
    };

    calibration
    {
        beta  = 0.99;   # discount factor (quarterly)
        sigma = 1;      # CRRA coefficient
        chi   = 1;      # labor disutility
        phi   = 1;      # inverse Frisch elasticity
        delta = 0.025;  # depreciation rate (quarterly)
    };
};

block FIRM
{
    controls
    {
        H_f[], K_f[];
    };

    objective
    {
        Pi[] = Y[] - W[] * H_f[] - R[] * K_f[-1];
    };

    constraints
    {
        Y[] = A[] * K_f[-1]^alpha * H_f[]^(1 - alpha);
    };

    calibration
    {
        alpha = 0.33;
    };
};

block TECHNOLOGY_SHOCK
{
    identities
    {
        log(A[]) = rho * log(A[-1]) + epsilon_A[];
    };

    shocks
    {
        epsilon_A[];
    };

    calibration
    {
        rho = 0.9;
    };
};

block EQUILIBRIUM
{
    identities
    {
        # Market clearing
        K_f[] = K[-1];
        H_f[] = H[];
    };
};
```

### הרצה בR

```r
library(gEcon)

# טעינה ופתרון
rbc <- make_model("rbc_model.gcn")

# Steady State
rbc <- steady_state(rbc)
get_ss_values(rbc, to_tex = FALSE)

# פרמטריזציה ופתרון
rbc <- solve_pert(rbc, loglin = TRUE)

# Impulse Response Functions (IRF)
rbc <- set_shock_cov_mat(rbc, shock_matrix = matrix(0.01^2), shock_order = "epsilon_A")
rbc <- compute_irf(rbc, shocks = "epsilon_A", periods = 40)

# גרף IRF
plot_irf(rbc,
         variables = c("Y", "C", "I", "H", "K"),
         shocks    = "epsilon_A",
         main      = "RBC: Technology Shock IRF")
```

---

## חלק ד – New Keynesian Model: הוספת rigidities

**הבדל מ-RBC:**
- מחירים דביקים (Calvo pricing)
- כוח שוק של פירמות
- **מדיניות מוניטרית משנה את הכלכלה הריאלית!**

### 3 משוואות מרכזיות (3-Equation NK Model)

```
# IS Curve (Dynamic)
ỹₜ = Eₜ[ỹₜ₊₁] - (1/σ)·(iₜ - Eₜ[πₜ₊₁] - r*) + demand_shock

# Phillips Curve (NKPC)
πₜ = β·Eₜ[πₜ₊₁] + κ·ỹₜ + cost_push_shock

# Taylor Rule
iₜ = r* + φ_π·πₜ + φ_y·ỹₜ + monetary_shock

ỹ = output gap (תוצרת בפועל פחות פוטנציאל)
π = inflation
i = nominal interest rate
```

### פרמטרים טיפוסיים

```r
# NK Model Parameters
params <- list(
  beta    = 0.99,    # discount factor
  sigma   = 1.0,     # inter-temporal elasticity
  kappa   = 0.1,     # Phillips curve slope
  phi_pi  = 1.5,     # Taylor Rule: inflation coefficient
  phi_y   = 0.5,     # Taylor Rule: output gap coefficient
  rho_a   = 0.9,     # technology persistence
  rho_nu  = 0.5      # monetary shock persistence
)
```

---

## חלק ה – סימולציה ידנית: 3-Equation NK

```r
library(tidyverse)

# === פרמטרים ===
beta   <- 0.99
sigma  <- 1.0
kappa  <- 0.1
phi_pi <- 1.5
phi_y  <- 0.5
rho_a  <- 0.9

# === Forward-Looking Solution (Blanchard-Kahn) ===
# בקיצור: נניח expectation ניתנת לפתרון אנליטי
# ונדמה תגובה להלם

T <- 40  # תקופות

# ===== הלם ביקוש (demand shock) =====
simulate_nk <- function(shock_type = "demand",
                        shock_size = 1.0) {
  y     <- numeric(T)
  pi    <- numeric(T)
  i     <- numeric(T)
  shock <- numeric(T)

  shock[1] <- shock_size

  for (t in 2:T) {
    shock[t] <- rho_a * shock[t-1]

    # תגובה פשוטה (backward-looking approximation)
    if (shock_type == "demand") {
      y[t]  <- 0.7 * y[t-1] + shock[t] - 0.5 * (i[t-1] - pi[t-1])
      pi[t] <- 0.9 * pi[t-1] + kappa * y[t]
    } else if (shock_type == "cost_push") {
      pi[t] <- 0.9 * pi[t-1] + shock[t]
      y[t]  <- 0.7 * y[t-1] - 0.5 * (i[t-1] - pi[t-1])
    } else {  # monetary
      i[t] <- 0.8 * i[t-1] + shock[t]
      y[t] <- 0.7 * y[t-1] - 0.5 * i[t]
      pi[t] <- 0.9 * pi[t-1] + kappa * y[t]
    }

    # Taylor Rule
    i[t] <- phi_pi * pi[t] + phi_y * y[t]
  }

  tibble(
    period = 1:T,
    output_gap  = y,
    inflation   = pi,
    interest    = i,
    shock       = shock,
    shock_type  = shock_type
  )
}

# === הרצת שלושת ההלמים ===
demand_irf   <- simulate_nk("demand",    1.0)
cost_irf     <- simulate_nk("cost_push", 0.5)
monetary_irf <- simulate_nk("monetary",  1.0)

all_irfs <- bind_rows(demand_irf, cost_irf, monetary_irf) %>%
  pivot_longer(c(output_gap, inflation, interest),
               names_to = "variable", values_to = "value") %>%
  mutate(
    variable = factor(variable,
      levels = c("output_gap", "inflation", "interest"),
      labels = c("פער תוצרת", "אינפלציה", "ריבית")),
    shock_type = factor(shock_type,
      levels = c("demand", "cost_push", "monetary"),
      labels = c("הלם ביקוש", "הלם מחירים", "הלם מוניטרי"))
  )

# === ויזואליזציה ===
ggplot(all_irfs, aes(x = period, y = value, color = shock_type)) +
  geom_line(linewidth = 1.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  facet_grid(variable ~ shock_type, scales = "free_y") +
  scale_color_brewer(palette = "Set1", guide = "none") +
  labs(
    title    = "Impulse Response Functions – New Keynesian Model",
    subtitle = "תגובת הכלכלה לשלושה סוגי הלמים",
    x        = "תקופות אחרי ההלם",
    y        = "% סטייה מ-Steady State",
    caption  = "מודל NK פשוט – 3 משוואות | EconLab PPE"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold"),
    strip.text = element_text(face = "bold")
  )

ggsave("nk_irf.png", width = 12, height = 8, dpi = 300)
```

---

## חלק ו – קריאה: DSGE בפרקטיקה

### כלי DSGE מרכזיים

| כלי | שפה | שימוש |
|---|---|---|
| **Dynare** | MATLAB/Octave | הכי נפוץ בבנקים מרכזיים |
| **gEcon** | R | Open source, מתאים לסטודנטים |
| **DSGE.jl** | Julia | מהיר מאוד |
| **pydsge** | Python | Python-friendly |
| **IRIS** | MATLAB | BOE, Norges Bank |

### מה בנק ישראל משתמש?

בנק ישראל משתמש במספר מודלים:
- **BOTAC**: מודל DSGE מלא עם פקטור הון אנושי
- **MOISE**: מודל לתחזיות קצר טווח
- **SIGMA**: מודל בין-לאומי מ-Federal Reserve

### קריאה מומלצת

1. **Gali (2015)**: *Monetary Policy, Inflation, and the Business Cycle* – הספר הסטנדרטי ל-NK DSGE
2. **Kydland & Prescott (1982)**: "Time to Build and Aggregate Fluctuations" – המאמר המקורי של RBC
3. **Smets & Wouters (2003)**: מודל SW – ה-DSGE הנפוץ ביותר בבנקים מרכזיים

---

## משימות השבוע

### משימה 1: RBC Steady State (35 נקודות)

```r
# נתון: alpha=0.33, beta=0.99, delta=0.025
# חשב ידנית (ב-R):
# 1. R* = 1/beta - (1-delta)
# 2. K*/Y* = alpha*beta / (1 - beta*(1-delta))
# 3. C*/Y* = 1 - delta*(K*/Y*)
# 4. W* = (1-alpha) * Y*/H* (עם H*=1)
# 5. הצג כטבלה: Steady State Values
# 6. שנה alpha=0.25, 0.33, 0.40 → כיצד משתנה K*/Y*?
# 7. גרף: K*/Y* כפונקציה של alpha (0.1 עד 0.5)
```

### משימה 2: 3-Equation NK Simulation (35 נקודות)

```r
# השתמש בפונקציה simulate_nk() מחלק ה:
# 1. הרץ הלם ביקוש בגדלים שונים: 0.5, 1.0, 2.0
# 2. גרף: כיצד גודל ההלם משנה את הפער תוצרת / אינפלציה?
# 3. שנה phi_pi: 1.2, 1.5, 2.0 (Taylor Rule aggressiveness)
#    → האם תגובה חזקה יותר מייצבת מהר יותר?
# 4. הצג Sacrifice Ratio: כמה פער תוצרת צריך ל-1% ירידת אינפלציה?
# 5. כתוב ממצא כלכלי: מה תלמד מהסימולציה?
```

### משימה 3: קריאה וסיכום (30 נקודות)

```markdown
# סיכום קריאה: מודל DSGE בבנק ישראל

## 1. מה ה-Lucas Critique?
   (בעיה עם רגרסיה פשוטה לניתוח מדיניות)

## 2. הבדל RBC vs. New Keynesian
   (טבלת השוואה)

## 3. שלוש משוואות NK – פרש כלכלית
   IS Curve / Phillips Curve / Taylor Rule

## 4. Impulse Response Function – מה היא מראה?

## 5. יישום: אילו שאלות כלכליות אפשר לענות עם DSGE שלא אפשר עם רגרסיה?
```

---

## הגשה

```
Members/YourName/Week_21/
├── rbc_steady_state.R
├── nk_simulation.R
├── nk_irf.png
└── dsge_reading_summary.md
```

---

**השבוע הבא:** DSGE מלא – gEcon/Dynare, אמידה בייזיאנית, תחזיות → [שבוע 22](../Week_22_DSGE_Advanced/README.md)

### 💻 תרגול מעשי (Hands-on)

<p>לחצו על המשולש (Play) כדי להפעיל את סביבת הפיתוח בתוך העמוד, או פתחו בלשונית חדשה לנוחות מירבית.</p>
<iframe src="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_21_DSGE_Intro/starter_notebook.ipynb" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
<p><br><em>* אם המסך לא נטען או מבקש הרשאות אבטחה, <a href="https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_21_DSGE_Intro/starter_notebook.ipynb" target="_blank">לחצו כאן לפתיחת המחברת במסך מלא</a>.</em></p>
