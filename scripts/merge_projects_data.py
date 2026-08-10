import os
import json
import yaml

def process_markdown_files():
    with open("projects_data.json", "r") as f:
        fis_projects = json.load(f)

    proj_dir = "_projects"
    for filename in os.listdir(proj_dir):
        if not filename.endswith(".md") or filename == "TEMPLATE-PROJECT.md":
            continue
            
        filepath = os.path.join(proj_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        end_idx = content.find("---", 3)
        if end_idx == -1:
            continue
            
        frontmatter = content[3:end_idx]
        body = content[end_idx:]
        
        try:
            parsed = yaml.safe_load(frontmatter)
        except Exception as e:
            continue
            
        if not isinstance(parsed, dict):
            continue
            
        local_title = parsed.get("title", "").strip()
        if not local_title:
            continue
            
        # Hardcode matching logic to be 100% reliable
        best_match = None
        for fp in fis_projects:
            fis_title = fp["title"]
            local_lower = local_title.lower()
            fis_lower = fis_title.lower()
            
            match = False
            if local_lower in fis_lower:
                match = True
            # Special cases
            if "creative space" in local_lower and "creative space" in fis_lower: match = True
            if "nfdi" in local_lower and "nfdi" in fis_lower: match = True
            if "provider" == local_lower and "provider:" in fis_lower: match = True
            if "hdn" in local_lower and "hdn" in fis_lower: match = True
            if "mobile ai workstations" in local_lower and "mobile ki-workstations" in fis_lower: match = True
            if "lstartuplab" in local_lower and "lstartuplab" in fis_lower: match = True
            if "student ai server" in local_lower and "studentischen ki-servers" in fis_lower: match = True
            if "llms for clinical-research" in local_lower and "datenextraktion für klinische forschung" in fis_lower: match = True
            
            if match:
                best_match = fp
                break
                
        if best_match:
            print(f"\nMatched local '{local_title}' -> FIS '{best_match['title']}'")
            
            changes_made = False
            
            if best_match.get("website") and not parsed.get("website"):
                changes_made = True
                print(f"  + Added website: {best_match['website']}")
                
            if best_match.get("funding_organization") and not parsed.get("funding_organization"):
                changes_made = True
                print(f"  + Added funding_organization: {best_match['funding_organization']}")
                
            if best_match.get("participants") and not parsed.get("participants"):
                if isinstance(best_match["participants"], list) and len(best_match["participants"]) > 0:
                    changes_made = True
                    print(f"  + Added participants: {best_match['participants']}")
                    
            if changes_made:
                new_frontmatter_lines = []
                
                if best_match.get("website") and "website:" not in frontmatter:
                    new_frontmatter_lines.append(f"website: \"{best_match['website']}\"")
                
                if best_match.get("funding_organization") and "funding_organization:" not in frontmatter:
                    new_frontmatter_lines.append(f"funding_organization: \"{best_match['funding_organization']}\"")
                    
                if best_match.get("participants") and "participants:" not in frontmatter and len(best_match['participants']) > 0:
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
