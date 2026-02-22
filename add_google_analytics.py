import os
file_path = "_quarto.yml"
if not os.path.exists(file_path):
    print("Error: _quarto.yml not found.")
    exit(1)
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
if any("google-analytics:" in line for line in lines):
    print("Google Analytics is already configured in _quarto.yml.")
else:
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        # Look for the website key to inject GA right under it
        if line.strip().startswith("website:") and not inserted:
            new_lines.append('  google-analytics: "G-XXXXXXXXXX" # <-- תחליפו את זה במזהה האמיתי שלכם\n')
            inserted = True

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Successfully added Google Analytics placeholder.")
