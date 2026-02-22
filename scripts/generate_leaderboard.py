import os
from datetime import datetime

def generate():
    members_dir = "Members"
    scores = {}

    # Check if Members directory exists
    if os.path.exists(members_dir):
        # Iterate over student folders
        for student in os.listdir(members_dir):
            student_path = os.path.join(members_dir, student)
            if os.path.isdir(student_path):
                # Count unique assignment folders submitted by the student
                assignments = [d for d in os.listdir(student_path) if os.path.isdir(os.path.join(student_path, d))]
                scores[student] = len(assignments)

    # Sort students by score descending
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Generate Markdown content for Quarto
    md = [
        "---",
        "title: '🏆 לוח תוצאות'",
        "comments: false",
        "---",
        "",
        "כאן תוכלו לראות את ההתקדמות של חברי הקהילה! הלוח מתעדכן אוטומטית בכל פעם שסטודנט מגיש מחברת פתורה לתיקייה שלו.",
        "",
        "| מיקום | שם הסטודנט | משימות שהושלמו |",
        "|:---:|:---|:---:|"
    ]

    if not sorted_scores:
        md.append("| - | עדיין אין הגשות. תהיו הראשונים! | 0 |")
    else:
        for i, (student, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**{i}**"
            clean_name = student.replace('_', ' ')
            md.append(f"| {medal} | {clean_name} | **{score}** |")

    md.append("")
    md.append(f"*עודכן לאחרונה: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")

    with open("leaderboard.qmd", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    generate()
