import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

def fix_class_string(match):
    quote = match.group(1)
    classes = match.group(2)
    
    # Check if this class string contains the extremely dark text classes we forced (700, 800, 900)
    has_dark_text = re.search(r'\btext-(slate|gray)-(700|800|900)\b', classes)
    if not has_dark_text:
        return match.group(0) # no change
        
    # Check if it ALREADY has a dark mode override
    has_dark_mode_text = re.search(r'\bdark:text-', classes)
    if has_dark_mode_text:
        return match.group(0) # no change
        
    # Inject a dark mode text color for high contrast in dark mode (200)
    if 'slate' in has_dark_text.group(0):
        classes += ' dark:text-slate-200'
    else:
        classes += ' dark:text-gray-200'
        
    return 'class=' + quote + classes + quote

# Match class attribute with double quotes, single quotes, or backticks
class_pattern = re.compile(r'class=(["\'`])(.*?)\1', re.DOTALL)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = class_pattern.sub(fix_class_string, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed {filepath}')
