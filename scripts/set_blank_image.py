import os
import re

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

for line in raw_list.split('\n'):
    line = line.strip()
    if not line or line in ["Head of the Department", "Office Management", "Technical and Administrative Staff", "Academic Advisor", "Research Assistants", "Scholarship holder", "External PhD Students", "Student Assistants and Research Assistants"]:
        continue
        
    line_clean = re.sub(r'\(.*?\)', '', line).strip()
    
    title_pattern = r'^(Prof\.\s*Dr\.|Dr\.|Dipl\.-Ing\.)\s+'
    title_match = re.search(title_pattern, line_clean)
    if title_match:
        name_part = line_clean[title_match.end():]
    else:
        name_part = line_clean
        
    suffix_pattern = r',\s*(M\.Sc\.|B\.A\.|M\.A\.|Ass\.\s*iur\.)'
    suffix_match = re.search(suffix_pattern, name_part)
    if suffix_match:
        name_part = name_part[:suffix_match.start()]
        
    name_part = name_part.strip()
    
    filename_base = name_part.lower()
    filename_base = filename_base.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    filename_base = re.sub(r'[^a-z0-9\s-]', '', filename_base)
    filename_base = re.sub(r'\s+', '-', filename_base.strip())
    
    md_filename = f"{filename_base}.md"
    file_path = os.path.join(TEAM_DIR, md_filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace image line
        new_content = re.sub(r'image:\s*".*?"', 'image: "blank.png"', content)
        if 'image: "blank.png"' not in new_content:
            # Maybe no quotes
            new_content = re.sub(r'image:\s*[^\s]+', 'image: "blank.png"', content)
            
        if content != new_content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"Updated {md_filename}")
