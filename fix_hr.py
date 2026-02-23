import os
import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.rstrip() == '---':
            # Check if it's a Setext heading (previous non-empty line exists)
            prev = lines[i-1].rstrip() if i > 0 else ''
            if prev != '':
                # This is a Setext h2 heading underline — keep it
                new_lines.append(line)
            else:
                # Plain horizontal rule — replace with *** to avoid YAML confusion
                new_lines.append('***\n')
                changed += 1
        else:
            new_lines.append(line)
        i += 1

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Fixed {changed} occurrences in {filepath}")
    return changed

total = 0
for f in sorted(glob.glob('/home/user/econlabppe/Assignments/**/README.md', recursive=True)):
    total += fix_file(f)

print(f"\nTotal replacements: {total}")
