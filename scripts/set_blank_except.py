import os
import glob
import re

TEAM_DIR = "_team"
EXCLUDE = [
    "debayan-banerjee.md",
    "anna-ehrenberg.md",
    "h-marlene-schulz.md",
    "ricardo-usbeck.md",
    "template.md"
]

for filepath in glob.glob(os.path.join(TEAM_DIR, "*.md")):
    filename = os.path.basename(filepath)
    if filename in EXCLUDE:
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    new_content = re.sub(r'image:\s*".*?"', 'image: "blank.png"', content)
    if 'image: "blank.png"' not in new_content:
        new_content = re.sub(r'image:\s*[^\s]+', 'image: "blank.png"', content)
        
    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filename}")
