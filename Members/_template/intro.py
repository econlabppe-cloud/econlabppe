"""
intro.py – EconLab PPE
=======================
ערוך את הקובץ הזה עם הפרטים שלך והרץ אותו:
    python Members/YourName/intro.py

זוהי המשימה הראשונה שלך: לוודא ש-Python עובד
ולהציג את עצמך לשאר חברי המעבדה.
"""


def main():
    # ===== ערוך כאן =====
    name = "Your Name"                   # שמך באנגלית
    degree = "B.A. Economics"            # התואר שלך
    university = "Your University"       # שם האוניברסיטה
    year_of_study = "2nd year"           # שנת לימודים
    economic_interests = [
        "כתוב כאן תחום כלכלי שמעניין אותך",
        "תחום נוסף",
        "תחום שלישי",
    ]
    why_econlab = (
        "כתוב כאן במשפט אחד למה הצטרפת ל-EconLab PPE "
        "ומה אתה מקווה ללמוד."
    )
    # ====================

    print("=" * 50)
    print("  EconLab PPE | היכרות ראשונה")
    print("=" * 50)
    print(f"  שם:          {name}")
    print(f"  תואר:        {degree}")
    print(f"  אוניברסיטה:  {university}")
    print(f"  שנה:         {year_of_study}")
    print()
    print("  תחומי עניין כלכליים:")
    for i, interest in enumerate(economic_interests, start=1):
        print(f"    {i}. {interest}")
    print()
    print("  למה EconLab?")
    print(f"    {why_econlab}")
    print("=" * 50)

    # בדיקת סביבה
    import sys
    print(f"\n  Python version: {sys.version.split()[0]}")
    try:
        import pandas as pd
        print(f"  pandas version: {pd.__version__}  ✓")
    except ImportError:
        print("  pandas: לא מותקן! הרץ: pip install pandas")

    try:
        import numpy as np
        print(f"  numpy version:  {np.__version__}  ✓")
    except ImportError:
        print("  numpy: לא מותקן! הרץ: pip install numpy")

    print("\n  הכל תקין! ברוך הבא ל-EconLab PPE.")


if __name__ == "__main__":
    main()
