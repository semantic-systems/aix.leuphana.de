import os, json, re
import fetch_publications as fp

def main():
    fp.log("Fetching fresh DBLP data for fix...")
    pubs = fp.fetch_dblp_publications()
    
    # Map by lowercase title instead of filename
    pub_map = {}
    for p in pubs:
        title = p.get("title")
        if not title: continue
        
        # Priority parsing
        pub_type = p.get("type", "")
        venue = p.get("venue", "")
        is_conference = (pub_type == "Conference and Workshop Papers")
        is_journal = (pub_type == "Journal Articles")
        is_archive = ("Informal" in pub_type)
        conference = venue if is_conference else ""
        journal = venue if is_journal else ""
        
        year = str(p.get("year", ""))
        if is_conference and conference and year and year not in conference:
            conference = f"{conference} {year}"
            
        t_key = title.lower()
        if t_key not in pub_map:
            pub_map[t_key] = {
                "is_conference": is_conference, "is_journal": is_journal, "is_archive": is_archive,
                "conference": conference, "journal": journal, "priority": 1 if is_conference else 2 if is_journal else 3 if is_archive else 4
            }
        else:
            # Enforce priority
            curr_pri = pub_map[t_key]["priority"]
            new_pri = 1 if is_conference else 2 if is_journal else 3 if is_archive else 4
            if new_pri < curr_pri:
                pub_map[t_key] = {
                    "is_conference": is_conference, "is_journal": is_journal, "is_archive": is_archive,
                    "conference": conference, "journal": journal, "priority": new_pri
                }
                
    state = fp.load_state()
    pubs_state = state.get("publications", {})
    
    updated = 0
    for fn, info in pubs_state.items():
        title = info.get("title", "").lower()
        if title in pub_map:
            m = pub_map[title]
            filepath = info["file"]
            
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                parts = content.split("---")
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    frontmatter = re.sub(r'is_conference:.*\n', '', frontmatter)
                    frontmatter = re.sub(r'is_journal:.*\n', '', frontmatter)
                    frontmatter = re.sub(r'is_archive:.*\n', '', frontmatter)
                    frontmatter = re.sub(r'conference:.*\n', '', frontmatter)
                    frontmatter = re.sub(r'journal:.*\n', '', frontmatter)
                    
                    new_fields = f"is_conference: {str(m['is_conference']).lower()}\n"
                    new_fields += f"is_journal: {str(m['is_journal']).lower()}\n"
                    new_fields += f"is_archive: {str(m['is_archive']).lower()}\n"
                    if m['is_conference'] and m['conference']:
                        c = m['conference'].replace('"', '\\"')
                        new_fields += f'conference: "{c}"\n'
                    elif m['is_journal'] and m['journal']:
                        j = m['journal'].replace('"', '\\"')
                        new_fields += f'journal: "{j}"\n'
                        
                    parts[1] = frontmatter.rstrip() + "\n" + new_fields
                    new_content = "---".join(parts)
                    
                    if content != new_content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        updated += 1
                        
            # Update state
            pubs_state[fn]["is_conference"] = m["is_conference"]
            pubs_state[fn]["is_journal"] = m["is_journal"]
            pubs_state[fn]["is_archive"] = m["is_archive"]
            
    fp.log(f"Fixed {updated} files.")
    
    state["publications"] = pubs_state
    total = len(pubs_state)
    with_abstract = sum(1 for v in pubs_state.values() if v.get("has_abstract"))
    without_abstract = total - with_abstract
    total_conference = sum(1 for v in pubs_state.values() if v.get("is_conference"))
    total_journal = sum(1 for v in pubs_state.values() if v.get("is_journal"))
    total_archive = sum(1 for v in pubs_state.values() if v.get("is_archive"))

    from datetime import datetime, timezone
    state["summary"] = {
        "total_publications": total, "with_abstract": with_abstract, "without_abstract": without_abstract,
        "total_conference": total_conference, "total_journal": total_journal, "total_archive": total_archive,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    with open(fp.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
