import os
import json
import glob
import re
from datetime import datetime, timezone

import fetch_publications as fp

def main():
    fp.log_header("MIGRATION: Deduplicating and enforcing priority")
    pubs = fp.fetch_dblp_publications()
    
    # Group by filename
    groups = {}
    for p in pubs:
        title = p.get("title")
        if not title: continue
        fn = fp.sanitize_filename(title)
        
        # Populate boolean fields
        pub_type = p.get("type", "")
        venue = p.get("venue", "")
        p["is_conference"] = (pub_type == "Conference and Workshop Papers")
        p["is_journal"] = (pub_type == "Journal Articles")
        p["is_archive"] = (pub_type == "Informal Publications")
        p["conference"] = venue if p["is_conference"] else ""
        p["journal"] = venue if p["is_journal"] else ""
        
        # Add year to conference if missing
        year = str(p.get("year", ""))
        if p["is_conference"] and p["conference"] and year and year not in p["conference"]:
            p["conference"] = f"{p['conference']} {year}"
            
        groups.setdefault(fn, []).append(p)
        
    # Select best per group
    pub_map = {}
    for fn, group in groups.items():
        best = None
        for p in group:
            if p["is_conference"]:
                best = p
                break
        if not best:
            for p in group:
                if p["is_journal"]:
                    best = p
                    break
        if not best:
            for p in group:
                if p["is_archive"]:
                    best = p
                    break
        if not best:
            best = group[0]
            
        pub_map[fn] = best
        
    state = fp.load_state()
    pubs_state = state.get("publications", {})
    
    md_files = glob.glob(os.path.join(fp.OUTPUT_DIR, "*.md"))
    updated = 0
    
    for filepath in md_files:
        fn = os.path.basename(filepath).replace(".md", "")
        if fn not in pub_map:
            continue
            
        m = pub_map[fn]
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        parts = content.split("---")
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Replace old fields
            frontmatter = re.sub(r'is_conference:.*\n', '', frontmatter)
            frontmatter = re.sub(r'is_journal:.*\n', '', frontmatter)
            frontmatter = re.sub(r'is_archive:.*\n', '', frontmatter)
            frontmatter = re.sub(r'conference:.*\n', '', frontmatter)
            frontmatter = re.sub(r'journal:.*\n', '', frontmatter)
            
            # Add new fields
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
                
        if fn in pubs_state:
            pubs_state[fn]["is_conference"] = m["is_conference"]
            pubs_state[fn]["is_journal"] = m["is_journal"]
            pubs_state[fn]["is_archive"] = m["is_archive"]
            
    fp.log(f"Updated {updated} markdown files.")
    
    total = len(pubs_state)
    with_abstract = sum(1 for v in pubs_state.values() if v.get("has_abstract"))
    without_abstract = total - with_abstract
    total_conference = sum(1 for v in pubs_state.values() if v.get("is_conference"))
    total_journal = sum(1 for v in pubs_state.values() if v.get("is_journal"))
    total_archive = sum(1 for v in pubs_state.values() if v.get("is_archive"))

    state["summary"] = {
        "total_publications": total,
        "with_abstract": with_abstract,
        "without_abstract": without_abstract,
        "total_conference": total_conference,
        "total_journal": total_journal,
        "total_archive": total_archive,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    with open(fp.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        
    fp.log("Migration complete!")

if __name__ == "__main__":
    main()
