import os

filepath = r"c:\Users\ruant\OneDrive\Documents\Omnibot\6.4.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False

for i, line in enumerate(lines):
    # Remove Advanced Block (roughly from line 432 to 454)
    if "<!-- ═══ Advanced ═══ -->" in line:
        skip = True
    
    if skip and '<!-- OK Button -->' in line:
        skip = False
    
    if not skip:
        # Fix text-white for Personality Options
        if '<h4 class="text-xs font-bold text-white">Alpha Engine</h4>' in line:
            line = line.replace('text-white', 'text-slate-800 dark:text-white')
        elif '<h4 class="text-xs font-bold text-white">Nova Engine</h4>' in line:
            line = line.replace('text-white', 'text-slate-800 dark:text-white')
        elif '<h4 class="text-xs font-bold text-white">Luna Engine</h4>' in line:
            line = line.replace('text-white', 'text-slate-800 dark:text-white')
            
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
