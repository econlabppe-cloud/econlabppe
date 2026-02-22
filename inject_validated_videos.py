import os
import re
videos = {
    "Week_01": [
        "[https://www.youtube.com/watch?v=RGOj5yH7evk](https://www.youtube.com/watch?v=RGOj5yH7evk)",
        "[https://www.youtube.com/watch?v=e2IbNHi4uCI](https://www.youtube.com/watch?v=e2IbNHi4uCI)",
        "[https://www.youtube.com/watch?v=Uszj_k0DGsg](https://www.youtube.com/watch?v=Uszj_k0DGsg)"
    ],
    "Week_02": [
        "[https://www.youtube.com/watch?v=k1VUZEVuDJ8](https://www.youtube.com/watch?v=k1VUZEVuDJ8)",
        "[https://www.youtube.com/watch?v=g1kmDtCyVLg](https://www.youtube.com/watch?v=g1kmDtCyVLg)",
        "[https://www.youtube.com/watch?v=9IeD-wB8kWE](https://www.youtube.com/watch?v=9IeD-wB8kWE)"
    ],
    "Week_03": [
        "[https://www.youtube.com/watch?v=m0wI61ahfvY](https://www.youtube.com/watch?v=m0wI61ahfvY)",
        "[https://www.youtube.com/watch?v=igSovq_H24A](https://www.youtube.com/watch?v=igSovq_H24A)",
        "[https://www.youtube.com/watch?v=sUxrA8NIVK0](https://www.youtube.com/watch?v=sUxrA8NIVK0)"
    ],
    "Week_04": [
        "[https://www.youtube.com/watch?v=QXzopqpHlSs](https://www.youtube.com/watch?v=QXzopqpHlSs)",
        "[https://www.youtube.com/watch?v=L4Bhs_v1BBA](https://www.youtube.com/watch?v=L4Bhs_v1BBA)",
        "[https://www.youtube.com/watch?v=sOen7Z8tKpw](https://www.youtube.com/watch?v=sOen7Z8tKpw)"
    ],
    "Week_05": [
        "[https://www.youtube.com/watch?v=HXV3zeQKqGY](https://www.youtube.com/watch?v=HXV3zeQKqGY)",
        "[https://www.youtube.com/watch?v=zsjfGDiOcTo](https://www.youtube.com/watch?v=zsjfGDiOcTo)",
        "[https://www.youtube.com/watch?v=ztHopE5Wnpc](https://www.youtube.com/watch?v=ztHopE5Wnpc)"
    ],
    "Week_06": [
        "[https://www.youtube.com/watch?v=9yeOJ0ZMUYw](https://www.youtube.com/watch?v=9yeOJ0ZMUYw)",
        "[https://www.youtube.com/watch?v=0UQJC_FEQ_A](https://www.youtube.com/watch?v=0UQJC_FEQ_A)",
        "[https://www.youtube.com/watch?v=CJzeKzKz_KU](https://www.youtube.com/watch?v=CJzeKzKz_KU)"
    ],
    "Week_07": [
        "[https://www.youtube.com/watch?v=Ww71knvhQ-s](https://www.youtube.com/watch?v=Ww71knvhQ-s)",
        "[https://www.youtube.com/watch?v=cNgMWD2mMWU](https://www.youtube.com/watch?v=cNgMWD2mMWU)",
        "[https://www.youtube.com/watch?v=zAmJTGEGzAM](https://www.youtube.com/watch?v=zAmJTGEGzAM)"
    ],
    "Week_08": [
        "[https://www.youtube.com/watch?v=kqtD5dpn9C8](https://www.youtube.com/watch?v=kqtD5dpn9C8)",
        "[https://www.youtube.com/watch?v=W8KRlNvCQOU](https://www.youtube.com/watch?v=W8KRlNvCQOU)",
        "[https://www.youtube.com/watch?v=ZDa-Z5JzLSg](https://www.youtube.com/watch?v=ZDa-Z5JzLSg)"
    ],
    "Week_09": [
        "[https://www.youtube.com/watch?v=ZyhVh-qRZPA](https://www.youtube.com/watch?v=ZyhVh-qRZPA)",
        "[https://www.youtube.com/watch?v=Lw2qlCEvdnU](https://www.youtube.com/watch?v=Lw2qlCEvdnU)",
        "[https://www.youtube.com/watch?v=txMibs211Yk](https://www.youtube.com/watch?v=txMibs211Yk)"
    ],
    "Week_10": [
        "[https://www.youtube.com/watch?v=eMOA1pPVUc4](https://www.youtube.com/watch?v=eMOA1pPVUc4)",
        "[https://www.youtube.com/watch?v=h4hOPGo4UVU](https://www.youtube.com/watch?v=h4hOPGo4UVU)",
        "[https://www.youtube.com/watch?v=Kk6piJkoIEw](https://www.youtube.com/watch?v=Kk6piJkoIEw)"
    ],
    "Week_11": [
        "[https://www.youtube.com/watch?v=tb8gHvYlCFs](https://www.youtube.com/watch?v=tb8gHvYlCFs)",
        "[https://www.youtube.com/watch?v=9N6a-VLBa2I](https://www.youtube.com/watch?v=9N6a-VLBa2I)",
        "[https://www.youtube.com/watch?v=qriL9QAQVJ8](https://www.youtube.com/watch?v=qriL9QAQVJ8)"
    ],
    "Week_12": [
        "[https://www.youtube.com/watch?v=R67XsEXXGQ8](https://www.youtube.com/watch?v=R67XsEXXGQ8)",
        "[https://www.youtube.com/watch?v=aIQeXN1H_0M](https://www.youtube.com/watch?v=aIQeXN1H_0M)",
        "[https://www.youtube.com/watch?v=x9q8T9tQ4p8](https://www.youtube.com/watch?v=x9q8T9tQ4p8)"
    ]
}
def inject_videos():
    base_dir = "Assignments"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("README.md") or file.endswith(".qmd"):
                file_path = os.path.join(root, file)
                folder_name = os.path.basename(root)

                # Check if the folder matches one of our defined weeks
                week_key = next((key for key in videos.keys() if key in folder_name), None)

                if week_key:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Clean up old video blocks or placeholders if they exist
                    content = re.sub(r"### 🎥 סרטוני הדרכה.*?(?=\n#|\Z)", "", content, flags=re.DOTALL)
                    content = re.sub(r"### 🎥 סרטון.*?(?=\n#|\Z)", "", content, flags=re.DOTALL)

                    # Construct the new tabset block
                    vids = videos[week_key]
                    video_block = f"""
### 🎥 סרטוני הדרכה לפרק זה
כדי לכסות את החומר מכל הזוויות, ריכזנו עבורכם 3 סרטונים ברמות קושי שונות:
::: {{.panel-tabset}}
## 🟢 רמת מתחילים
**מבוא והיכרות עם המושגים הבסיסיים:**
{{{{< video {vids[0]} >}}}}
## 🟡 רמת ביניים
**העמקה ופרקטיקה מעשית:**
{{{{< video {vids[1]} >}}}}
## 🔴 רמת מתקדמים
**מקרי קצה, אופטימיזציה ושימושים מורכבים:**
{{{{< video {vids[2]} >}}}}
:::
"""
                    # Inject right after the first main title
                    content = re.sub(r"(# .*?\n)", r"\1\n" + video_block + "\n", content, count=1)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ Injected {week_key} videos → {file_path}")

if __name__ == "__main__":
    inject_videos()
