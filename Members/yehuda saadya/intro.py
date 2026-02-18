# intro.py
# EconLab PPE - my intro

def main():
    name = "השם שלך באנגלית"
    degree = "התואר שלך (למשל: B.A Economics / M.A Public Policy)"
    location = "Israel"
    goal = (
        "להתמקצע בכלים תכנותיים לכלכלנים דרך עבודה מסודרת בניהול פרויקטים, "
        "כדי להבין באמת בפרקטיקה ולבנות יכולת ללמד אחרים."
    )
    mission = (
        "להקים 'סיירת כלכלנים' שיודעת לקחת נתונים ציבוריים, לנקות, לנתח, "
        "לבנות מודלים וכלים, ולהפיק תוצרים שמסייעים בקבלת החלטות."
    )
    focus_areas = [
        "Python לדאטה ואוטומציה (pandas, visualization)",
        "R לאקונומטריקה (regression, DiD, time series)",
        "SQL להבנת מסדי נתונים ושאילתות",
        "ניתוח תקציב המדינה ונתוני מאקרו (בנק ישראל, למ״ס, OECD)",
    ]

    print("=== EconLab PPE | Intro ===")
    print(f"Name: {name}")
    print(f"Degree: {degree}")
    print(f"Location: {location}")
    print()
    print("Why I'm here:")
    print(goal)
    print()
    print("My mission:")
    print(mission)
    print()
    print("Focus areas:")
    for i, item in enumerate(focus_areas, start=1):
        print(f"{i}. {item}")


if __name__ == "__main__":
    main()
