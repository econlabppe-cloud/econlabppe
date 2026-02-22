# שבוע 17 – ויזואליזציה אינטראקטיבית עם Plotly (Python)

### 🎥 סרטוני הדרכה לשבוע זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:

::: {.panel-tabset}

## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{< video https://www.youtube.com/watch?v=u4VOc4qE9LM >}}

## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{< video https://www.youtube.com/watch?v=hSPmj7mK6ng >}}

## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{< video https://www.youtube.com/watch?v=GkXG51eY12M >}}

:::
## Matplotlib vs. Plotly

| Matplotlib | Plotly |
|---|---|
| סטטי – PNG/PDF | **אינטראקטיבי** – HTML |
| מעולה לפרסום אקדמי | מעולה לדשבורדים ואתרים |
| הרבה קוד לעיצוב | עיצוב מקצועי מהקופסה |
| לא responsive | Responsive (עובד בכל מכשיר) |

**מתי לבחור מה?**
- גרף לתזה/מאמר → **Matplotlib**
- גרף לדשבורד/אתר/דוח HTML → **Plotly**

---

## חלק א – Plotly Express: מהיר ופשוט

### התקנה

```bash
pip install plotly kaleido
# kaleido → לשמירת גרפים כ-PNG/PDF
```

### גרפים בסיסיים עם px

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# נתוני מאקרו
df = pd.DataFrame({
    "year":         [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "gdp_growth":   [4.2,  3.8, -1.9, 8.6,  6.5,  2.0,  1.1],
    "inflation":    [0.8,  0.8, -0.6, 1.5,  5.1,  4.2,  3.5],
    "unemployment": [4.0,  3.8,  4.3, 5.0,  3.7,  3.5,  4.2],
    "interest":     [0.1, 0.25,  0.1, 0.1,  3.25, 4.75, 4.5],
    "era":          ["נמוכה"]*4 + ["גבוהה"]*3
})

# --- גרף קווי ---
fig = px.line(
    df, x="year", y="gdp_growth",
    title="צמיחת תמ\"ג ישראל 2018-2024",
    labels={"year": "שנה", "gdp_growth": "% צמיחה"},
    markers=True,
    template="plotly_white"
)
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.show()

# --- גרף עמודות ---
df["color"] = df["gdp_growth"].apply(lambda x: "חיובי" if x > 0 else "שלילי")
fig = px.bar(
    df, x="year", y="gdp_growth",
    color="color",
    color_discrete_map={"חיובי": "#2196F3", "שלילי": "#F44336"},
    title="צמיחת תמ\"ג – ישראל",
    text="gdp_growth",
    template="plotly_white"
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.show()

# --- scatter עם hover מידע ---
fig = px.scatter(
    df,
    x="inflation", y="gdp_growth",
    size="unemployment",
    color="era",
    text="year",
    title="אינפלציה vs. צמיחה (גודל עיגול = אבטלה)",
    hover_data={"year": True, "interest": True},
    template="plotly_white"
)
fig.update_traces(textposition="top center")
fig.show()
```

### Subplots עם Plotly Express

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=["צמיחת תמ\"ג", "אינפלציה", "ריבית", "אבטלה"],
    shared_xaxes=True
)

# Row 1, Col 1 – bar
colors = ["#2196F3" if g > 0 else "#F44336" for g in df["gdp_growth"]]
fig.add_trace(
    go.Bar(x=df["year"], y=df["gdp_growth"], marker_color=colors, name="GDP"),
    row=1, col=1
)

# Row 1, Col 2 – line
fig.add_trace(
    go.Scatter(x=df["year"], y=df["inflation"],
               mode="lines+markers", name="Inflation",
               line=dict(color="orange", width=2)),
    row=1, col=2
)

# Row 2, Col 1 – step line (ריבית)
fig.add_trace(
    go.Scatter(x=df["year"], y=df["interest"],
               mode="lines", name="Interest",
               line=dict(color="royalblue", width=2, shape="hv")),  # hv = step
    row=2, col=1
)

# Row 2, Col 2 – scatter
fig.add_trace(
    go.Scatter(x=df["year"], y=df["unemployment"],
               mode="lines+markers", name="Unemployment",
               line=dict(color="green", width=2)),
    row=2, col=2
)

# עיצוב כולל
fig.update_layout(
    title_text="דשבורד מאקרו – ישראל 2018-2024",
    title_font_size=18,
    height=600,
    showlegend=False,
    template="plotly_white",
)

fig.show()
fig.write_html("macro_dashboard.html")
```

---

## חלק ב – Plotly Graph Objects: שליטה מלאה

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Dual-axis: ריבית ו-שע"ח ---
fig = make_subplots(specs=[[{"secondary_y": True}]])

# ציר ראשי: ריבית
fig.add_trace(
    go.Scatter(x=df["year"], y=df["interest"],
               name="ריבית (%)",
               mode="lines+markers",
               line=dict(color="royalblue", width=3, shape="hv"),
               marker=dict(size=8)),
    secondary_y=False
)

# ציר שני: אינפלציה
fig.add_trace(
    go.Scatter(x=df["year"], y=df["inflation"],
               name="אינפלציה (%)",
               mode="lines+markers",
               line=dict(color="tomato", width=2, dash="dot"),
               marker=dict(size=6)),
    secondary_y=True
)

# Annotation: מלחמה
fig.add_annotation(
    x=2023, y=4.75,
    text="מלחמת<br>אוקטובר",
    showarrow=True, arrowhead=2,
    font=dict(size=11, color="darkred"),
    arrowcolor="darkred"
)

# עיצוב צירים
fig.update_yaxes(title_text="ריבית בנק ישראל (%)", secondary_y=False)
fig.update_yaxes(title_text="אינפלציה (%)", secondary_y=True)
fig.update_layout(
    title="מדיניות מוניטרית – ריבית ואינפלציה",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)

fig.show()
```

### Animated Chart – גרף מונפש

```python
# נתוני cross-country לאורך זמן (כמו Gapminder!)
countries_data = pd.DataFrame({
    "year":    [2018]*5 + [2019]*5 + [2020]*5 + [2021]*5 + [2022]*5 + [2023]*5,
    "country": ["Israel","USA","Germany","Japan","UK"] * 6,
    "gdp":     [4.2, 2.9, 1.5, 0.6, 1.7,
                3.8, 2.3, 1.1, -0.4, 1.5,
                -1.9, -3.4, -4.6, -4.1, -9.3,
                8.6, 5.9, 2.6, 2.1, 7.6,
                6.5, 2.1, 1.8, 1.0, 7.6,
                2.0, 2.5, 0.4, 1.9, 0.4],
    "inflation":[0.8, 2.1, 1.8, 1.0, 2.5,
                 0.8, 2.3, 1.3, 0.5, 1.8,
                 -0.6, 1.2, 0.5, 0.0, 0.9,
                 1.5, 4.7, 3.2, -0.2, 2.5,
                 5.1, 8.0, 7.9, 3.0, 9.1,
                 4.2, 4.1, 5.9, 3.2, 6.8],
    "unemployment":[3.9, 3.9, 3.1, 2.4, 4.1,
                    3.8, 3.7, 3.0, 2.4, 3.8,
                    4.3, 8.1, 4.2, 2.8, 4.5,
                    5.0, 5.4, 3.5, 2.8, 4.5,
                    3.7, 3.6, 3.0, 2.6, 3.7,
                    3.5, 3.4, 3.0, 2.6, 4.3],
})

fig = px.scatter(
    countries_data,
    x="gdp", y="inflation",
    animation_frame="year",
    animation_group="country",
    size="unemployment",
    color="country",
    hover_name="country",
    range_x=[-6, 10],
    range_y=[-1, 10],
    title="GDP vs. Inflation: ישראל ומדינות מפותחות 2018-2023",
    labels={"gdp": "צמיחת תמ\"ג (%)", "inflation": "אינפלציה (%)"},
    template="plotly_white"
)
fig.update_layout(
    updatemenus=[{"type": "buttons", "showactive": False}]
)
fig.show()
fig.write_html("animated_macro.html")
```

---

## חלק ג – Choropleth Map: מפות כלכליות

```python
# מפת עולם – GDP per capita
world_data = pd.DataFrame({
    "iso_alpha": ["ISR", "USA", "DEU", "JPN", "GBR", "FRA", "KOR", "AUS",
                  "CAN", "CHE", "NOR", "SWE", "NLD", "BEL", "AUT"],
    "country":   ["Israel","USA","Germany","Japan","UK","France","South Korea",
                  "Australia","Canada","Switzerland","Norway","Sweden",
                  "Netherlands","Belgium","Austria"],
    "gdp_pc_2023": [54000, 80000, 54000, 33000, 46000, 43000, 35000,
                    65000, 56000, 93000, 89000, 62000, 58000, 50000, 56000],
    "gdp_growth_2023": [2.0, 2.5, 0.4, 1.9, 0.4, 0.9, 1.4, 2.0,
                        1.2, 1.0, 2.0, 0.5, 0.1, 1.5, 0.4],
})

# מפת GDP per capita
fig = px.choropleth(
    world_data,
    locations="iso_alpha",
    color="gdp_pc_2023",
    hover_name="country",
    hover_data={"gdp_growth_2023": True, "gdp_pc_2023": True},
    color_continuous_scale="Blues",
    title="GDP Per Capita 2023 (USD)",
    template="plotly_white"
)
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    coloraxis_colorbar_title="USD"
)
fig.show()
fig.write_html("world_gdp_map.html")
```

---

## חלק ד – Heatmap ו-Correlation Matrix

```python
# מטריצת קורלציות כלכליות
import numpy as np

indicators = ["gdp_growth", "inflation", "unemployment", "interest"]
data_matrix = df[indicators].corr().round(2)

# Heatmap עם annotations
fig = go.Figure(data=go.Heatmap(
    z=data_matrix.values,
    x=indicators,
    y=indicators,
    colorscale="RdBu",
    zmid=0,
    text=data_matrix.values,
    texttemplate="%{text:.2f}",
    textfont={"size": 14},
    hovertemplate="Row: %{y}<br>Col: %{x}<br>Corr: %{z:.3f}<extra></extra>"
))

fig.update_layout(
    title="מטריצת קורלציות – מדדי מאקרו ישראל",
    template="plotly_white",
    height=450
)
fig.show()

# Distribution (violin plot)
df_long = df[["year", "gdp_growth", "inflation", "interest"]].melt(
    id_vars="year", var_name="indicator", value_name="value"
)

fig = px.violin(
    df_long, x="indicator", y="value",
    box=True, points="all",
    title="התפלגות מדדים כלכליים",
    labels={"indicator": "מדד", "value": "ערך (%)"},
    template="plotly_white"
)
fig.show()
```

---

## חלק ה – Dash: דשבורד אינטראקטיבי מלא

```bash
pip install dash dash-bootstrap-components
```

```python
"""
macro_dashboard.py – דשבורד כלכלי אינטראקטיבי מלא
הרץ: python macro_dashboard.py
פתח: http://127.0.0.1:8050/
"""

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# נתונים
df = pd.DataFrame({
    "year":         [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "gdp_growth":   [4.2,  3.8, -1.9, 8.6,  6.5,  2.0,  1.1],
    "inflation":    [0.8,  0.8, -0.6, 1.5,  5.1,  4.2,  3.5],
    "unemployment": [4.0,  3.8,  4.3, 5.0,  3.7,  3.5,  4.2],
    "interest":     [0.1, 0.25,  0.1, 0.1,  3.25, 4.75, 4.5],
})

# אפליקציה
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("דשבורד מאקרו-כלכלי – ישראל", className="text-primary"),
            html.P("נתונים: בנק ישראל | EconLab PPE", className="text-muted")
        ])
    ], className="mb-4"),

    # Controls
    dbc.Row([
        dbc.Col([
            html.Label("בחר מדד:"),
            dcc.Dropdown(
                id="indicator-dropdown",
                options=[
                    {"label": "צמיחת תמ\"ג", "value": "gdp_growth"},
                    {"label": "אינפלציה",      "value": "inflation"},
                    {"label": "אבטלה",         "value": "unemployment"},
                    {"label": "ריבית",          "value": "interest"},
                ],
                value="gdp_growth",
                clearable=False
            )
        ], width=4),

        dbc.Col([
            html.Label("טווח שנים:"),
            dcc.RangeSlider(
                id="year-slider",
                min=2018, max=2024,
                value=[2018, 2024],
                marks={y: str(y) for y in range(2018, 2025)},
                step=1
            )
        ], width=8)
    ], className="mb-4"),

    # KPI Cards
    dbc.Row(id="kpi-cards", className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id="main-chart"), width=8),
        dbc.Col(dcc.Graph(id="scatter-chart"), width=4),
    ]),

], fluid=True)

# Callbacks
@callback(
    Output("main-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("kpi-cards", "children"),
    Input("indicator-dropdown", "value"),
    Input("year-slider", "value")
)
def update_charts(indicator, year_range):
    filtered = df[df["year"].between(year_range[0], year_range[1])]

    labels = {
        "gdp_growth": "צמיחת תמ\"ג (%)",
        "inflation": "אינפלציה (%)",
        "unemployment": "שיעור אבטלה (%)",
        "interest": "ריבית בנק ישראל (%)"
    }
    label = labels[indicator]

    # גרף ראשי
    if indicator == "gdp_growth":
        colors = ["#2196F3" if g > 0 else "#F44336" for g in filtered["gdp_growth"]]
        main_fig = go.Figure(go.Bar(
            x=filtered["year"], y=filtered[indicator],
            marker_color=colors, name=label
        ))
    else:
        main_fig = px.line(filtered, x="year", y=indicator,
                           markers=True, template="plotly_white")

    main_fig.update_layout(
        title=f"{label} – ישראל {year_range[0]}–{year_range[1]}",
        template="plotly_white"
    )

    # scatter
    scatter_fig = px.scatter(
        filtered, x=indicator, y="gdp_growth",
        text="year", trendline="ols",
        title=f"{label} vs. צמיחת תמ\"ג",
        template="plotly_white"
    )

    # KPI cards
    avg = filtered[indicator].mean()
    latest = filtered[indicator].iloc[-1]
    peak = filtered[indicator].max()

    cards = [
        dbc.Col(dbc.Card([
            dbc.CardHeader("ממוצע תקופה"),
            dbc.CardBody(html.H3(f"{avg:.2f}%"))
        ], color="light"), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("ערך אחרון"),
            dbc.CardBody(html.H3(f"{latest:.2f}%"))
        ], color="info", inverse=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("שיא"),
            dbc.CardBody(html.H3(f"{peak:.2f}%"))
        ], color="warning", inverse=True), width=4),
    ]

    return main_fig, scatter_fig, cards

if __name__ == "__main__":
    app.run(debug=True)
```

---

## משימות השבוע

### משימה 1: Plotly Express – 5 גרפים (25 נקודות)

```python
# עם נתוני BOI שהורדת בשבוע 11:
# 1. px.line: ריבית + CPI על ציר זמן (dual axis עם go)
# 2. px.bar: שינוי שנתי בשע"ח (צבע ירוק/אדום)
# 3. px.scatter: ריבית vs. שע"ח עם text=year
# 4. px.choropleth: GDP per capita לפחות 20 מדינות
# 5. Heatmap: מטריצת קורלציות של 5 מדדי BOI
```

### משימה 2: Animated Dashboard (35 נקודות)

```python
# שלוף נתונים מ-World Bank (שבוע 12)
# בנה animated scatter כמו Gapminder:
# x = gdp_per_capita, y = life_expectancy (או inflation)
# animation_frame = year (2000-2023)
# size = population, color = region
# הדגש את ישראל
```

### משימה 3: Dash Dashboard מלא (40 נקודות)

```python
# הרחב את macro_dashboard.py:
# 1. הוסף Dropdown לבחירת מדינה (ישראל + 4 מדינות OECD)
# 2. הוסף Date Range Picker
# 3. הוסף Tab שני: רגרסיה (scatter + trendline)
# 4. הוסף Tab שלישי: מפת עולם choropleth
# 5. Deploy: python macro_dashboard.py → שלח URL
```

---

## הגשה

```
Members/YourName/Week_17/
├── plotly_basics.py
├── animated_macro.html
├── world_gdp_map.html
├── macro_dashboard.py         ← Dash app
├── macro_dashboard.html       ← Static export
└── dashboard_screenshot.png
```

---

**השבוע הבא:** ggplot2 מתקדם ו-R Markdown → [שבוע 18](../Week_18_Visualization_R/README.md)

---

### 💻 תרגול מעשי (Hands-on)
קראתם את התיאוריה וראיתם את הסרטונים? עכשיו תורכם ללכלך את הידיים! 
הכנו עבורכם מחברת תרגול מוכנה. לחצו על הכפתור כדי לפתוח אותה ישירות בדפדפן שלכם:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/econlabppe-cloud/econlabppe/blob/main/Assignments/Week_17_Visualization_Python/starter_notebook.ipynb)

[או לחצו כאן להורדת המחברת למחשב (קובץ ipynb)](starter_notebook.ipynb)

