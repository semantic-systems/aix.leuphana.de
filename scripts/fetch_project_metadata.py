import os
import re
import json
import yaml
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_project_urls():
    url = "https://fis.leuphana.de/de/persons/ricardo-usbeck/projects/"
    print(f"Fetching projects list from {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("Failed to fetch projects list.")
        return []
        
    soup = BeautifulSoup(res.text, "html.parser")
    projects = []
    for h3 in soup.find_all("h3", class_="title"):
        a_tag = h3.find("a")
        if a_tag and "href" in a_tag.attrs:
            proj_title = a_tag.text.strip()
            proj_url = a_tag["href"]
            if proj_url.startswith("/"):
                proj_url = "https://fis.leuphana.de" + proj_url
            projects.append({"title": proj_title, "url": proj_url})
            
    print(f"Found {len(projects)} projects on FIS.")
    return projects

def extract_project_details(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {}
        
    soup = BeautifulSoup(res.text, "html.parser")
    data = {}
    
    web_span = soup.find(lambda tag: tag.name == "span" and "Projekt Webseite" in tag.text)
    if web_span and web_span.parent.name == "a":
        data["website"] = web_span.parent.get("href")
        
    funder_span = soup.find("span", class_="funder-name")
    if funder_span:
        data["funding_organization"] = funder_span.text.strip()
        
    part_h3 = soup.find(lambda tag: tag.name == "h3" and "Projektbeteiligte" in tag.text)
    participants = []
    if part_h3:
        ul = part_h3.find_next_sibling("ul")
        if ul:
            for li in ul.find_all("li"):
                org_tag = li.find("span", class_="organisation")
                if not org_tag:
                    a_tag = li.find("a", rel="Organisation")
                    if a_tag:
                        org_tag = a_tag.find("span")
                
                if org_tag:
                    participants.append(org_tag.text.strip())
    
    if participants:
        data["participants"] = participants
        
    return data

def process_markdown_files():
    fis_projects = get_project_urls()
    for fp in fis_projects:
        details = extract_project_details(fp["url"])
        fp.update(details)
        print(f"Scraped {fp['title']}: {details}")

    proj_dir = "_projects"
    for filename in os.listdir(proj_dir):
        if not filename.endswith(".md") or filename == "TEMPLATE-PROJECT.md":
            continue
            
        filepath = os.path.join(proj_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if not content.startswith("---"):
            continue
            
        end_idx = content.find("---", 3)
        if end_idx == -1:
            continue
            
        frontmatter = content[3:end_idx]
        body = content[end_idx:]
        
        try:
            parsed = yaml.safe_load(frontmatter)
        except Exception as e:
            print(f"Error parsing YAML for {filename}: {e}")
            continue
            
        local_title = parsed.get("title", "").strip()
        if not local_title:
            continue
            
        best_match = None
        best_score = 0
        for fp in fis_projects:
            score = similar(local_title, fp["title"])
            if score > best_score:
                best_score = score
                best_match = fp
                
        if best_match and best_score > 0.6:
            print(f"\nMatched local '{local_title}' -> FIS '{best_match['title']}' (Score: {best_score:.2f})")
            
            changes_made = False
            
            if "website" in best_match and not parsed.get("website"):
                changes_made = True
                print(f"  + Added website: {best_match['website']}")
                
            if "funding_organization" in best_match and not parsed.get("funding_organization"):
                changes_made = True
                print(f"  + Added funding_organization: {best_match['funding_organization']}")
                
            if "participants" in best_match and not parsed.get("participants"):
                if isinstance(best_match["participants"], list) and len(best_match["participants"]) > 0:
                    changes_made = True
                    print(f"  + Added participants: {best_match['participants']}")
                    
            if changes_made:
                new_frontmatter_lines = []
                
                if "website" in best_match and "website:" not in frontmatter:
                    new_frontmatter_lines.append(f"website: \"{best_match['website']}\"")
                
                if "funding_organization" in best_match and "funding_organization:" not in frontmatter:
                    new_frontmatter_lines.append(f"funding_organization: \"{best_match['funding_organization']}\"")
                    
                if "participants" in best_match and "participants:" not in frontmatter:
                    new_frontmatter_lines.append("participants:")
                    for p in best_match['participants']:
                        new_frontmatter_lines.append(f"  - \"{p}\"")
                
                if new_frontmatter_lines:
                    new_frontmatter_block = frontmatter.rstrip() + "\n" + "\n".join(new_frontmatter_lines) + "\n"
                    new_content = "---\n" + new_frontmatter_block.lstrip() + body
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"  -> Saved changes to {filename}")

if __name__ == "__main__":
    process_markdown_files()
