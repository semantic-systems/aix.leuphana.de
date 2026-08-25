import os
import re
import urllib.request
import ssl

# To avoid SSL certificate issues
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Mapping categories from user text to Jekyll template job_categories
category_mapping = {
    "Head of the Department": "head",
    "Office Management": "office_management",
    "Technical and Administrative Staff": "technical_staff",
    "Academic Advisor": "academic_advisor",
    "Research Assistants": "research_assistant",
    "Jann Pfeifer, M.Sc. (Research Associate)": "research_associate",
    "Scholarship holder": "scholarship_holder",
    "External PhD Students": "external_phd",
    "Student Assistants and Research Assistants": "student_assistant"
}

raw_list = """Head of the Department
Prof. Dr. Ricardo Usbeck
Office Management
Sabrina Bergmann
Diana Kästner
Madlen Schmaltz
Technical and Administrative Staff
Dipl.-Ing. Martin Kohler
Jan Henrik Last, B.A.
Academic Advisor
Dr. Debayan Banerjee
Research Assistants
Christian Borck, M.A.
Julian Burmester, M.Sc.
Anna Ehrenberg, M.Sc.
Dr. Panagiotis Ioannidis
Kai Moltzen, M.Sc.
Najebullah Shams, M.Sc.
Armin Szauer, M.Sc.
Tilahun Abedissa Taffa, M.Sc.
Dr. Patrick Westphal

Jann Pfeifer, M.Sc. (Research Associate)

Scholarship holder
Jannis Gries, Ass. iur.
Longquan Jiang, M.Sc.
H. Marlene Schulz, M.A.
Aida Usmanova, M.Sc.

External PhD Students
Junbo Huang (Universität Hamburg)
Dr. Cedric Möller (Universität Hamburg)
Jan Reinecke (HITec e.V)
Daniel Speck (HITec e.V)
Elena Williams (Lufthansa Technik AG)
Zeinab Aliakbari Mamaghani, M.Sc. (Ostfalia Hochschule)

Student Assistants and Research Assistants
Victor Caplan (Leuphana Universität Lüneburg)
Nina Marlis Dürfeldt (Leuphana Universität Lüneburg)
Muratbek Nurmatov (Leuphana Universität Lüneburg)
David Rath (Leuphana Universität Lüneburg)
Ghaith Abdullah Ali Al-Dailami (Leuphana Universität Lüneburg)
Hannah Louisa Heyne (Leuphana Universität Lüneburg)"""

TEAM_DIR = "_team"
IMG_DIR = "assets/images/team"

os.makedirs(TEAM_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

existing_files = set(os.listdir(TEAM_DIR))

current_category = "research_assistant"

for line in raw_list.split('\n'):
    line = line.strip()
    if not line:
        continue
    
    if line in category_mapping:
        current_category = category_mapping[line]
        continue
        
    # Handle the special Jann Pfeifer line
    if "Jann Pfeifer" in line and "(Research Associate)" in line:
        current_category = "research_associate"
        line = "Jann Pfeifer, M.Sc."
        
    # Remove affiliations in parentheses
    line_clean = re.sub(r'\(.*?\)', '', line).strip()
    
    # Extract title and name
    # Common titles
    title_pattern = r'^(Prof\.\s*Dr\.|Dr\.|Dipl\.-Ing\.)\s+'
    title_match = re.search(title_pattern, line_clean)
    academic_title = ""
    if title_match:
        academic_title = title_match.group(0).strip()
        name_part = line_clean[title_match.end():]
    else:
        name_part = line_clean
        
    # Extract suffix (M.Sc., B.A., M.A., Ass. iur.)
    suffix_pattern = r',\s*(M\.Sc\.|B\.A\.|M\.A\.|Ass\.\s*iur\.)'
    suffix_match = re.search(suffix_pattern, name_part)
    if suffix_match:
        if academic_title:
            academic_title += " " + suffix_match.group(1).strip()
        else:
            academic_title = suffix_match.group(1).strip()
        name_part = name_part[:suffix_match.start()]
        
    name_part = name_part.strip()
    
    # Generate filename
    # Remove special chars and accents for filename
    filename_base = name_part.lower()
    filename_base = filename_base.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    filename_base = re.sub(r'[^a-z0-9\s-]', '', filename_base)
    filename_base = re.sub(r'\s+', '-', filename_base.strip())
    
    md_filename = f"{filename_base}.md"
    
    if md_filename in existing_files:
        print(f"Skipping {md_filename} (already exists)")
        continue
        
    print(f"Processing {name_part} ({md_filename})...")
    
    # Try to fetch their image from Leuphana person page
    image_filename = f"{filename_base}.jpg"
    image_path = os.path.join(IMG_DIR, image_filename)
    
    profile_url = f"https://www.leuphana.de/en/institutes/iis/persons/{filename_base}.html"
    image_found = False
    
    try:
        req = urllib.request.Request(profile_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        # Find image src
        img_match = re.search(r'<img[^>]*class="[^"]*person[^"]*"[^>]*src="([^"]+)"', html)
        if not img_match:
            img_match = re.search(r'<img[^>]*src="([^"]+fileadmin/user_upload/PERSONALPAGES/[^"]+)"', html)
            
        if img_match:
            img_url = img_match.group(1)
            if img_url.startswith('/'):
                img_url = "https://www.leuphana.de" + img_url
            
            # Download image
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(img_req, context=ctx).read()
            with open(image_path, "wb") as f:
                f.write(img_data)
            image_found = True
            print(f"  Downloaded image from {img_url}")
    except Exception as e:
        print(f"  Profile page not found or error: {e}")
        
    if not image_found:
        image_filename = "placeholder.jpg"
        
    # Write markdown file
    md_content = f"""---
name: "{name_part}"
title: "{academic_title}"
image: "{image_filename}"
job_category: "{current_category}"

layout: team_member
permalink: /team/{filename_base}/
---

## About Me

Profile details coming soon.

## Contact

"""
    with open(os.path.join(TEAM_DIR, md_filename), "w") as f:
        f.write(md_content)
    print(f"  Created {md_filename}")
