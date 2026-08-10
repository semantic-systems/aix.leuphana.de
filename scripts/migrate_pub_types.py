import os
import json
import glob
import re

import fetch_publications as fp

def main():
    fp.log_header("MIGRATION: Fetching DBLP metadata to update pub types")
    pubs = fp.fetch_dblp_publications()
    
    # Map title to DBLP pub dict
    # DBLP title is often stripped. Let's use the sanitized filename as the key.
    pub_map = {}
    for p in pubs:
        title = p.get("title")
        if not title: continue
        fn = fp.sanitize_filename(title)
        
        # Determine types
        pub_type = p.get("type", "")
        venue = p.get("venue", "")
        is_conference = False
        is_journal = False
        is_archive = False
        conference = ""
        journal = ""
        
        if pub_type == "Conference and Workshop Papers":
            is_conference = True
            if venue: conference = venue
        elif pub_type == "Journal Articles":
            is_journal = True
            if venue: journal = venue
        elif pub_type == "Informal Publications":
            is_archive = True
            
        pub_map[fn] = {
            "is_conference": is_conference,
            "is_journal": is_journal,
            "is_archive": is_archive,
            "conference": conference,
            "journal": journal
        }
        
    state = fp.load_state()
    pubs_state = state.get("publications", {})
    
    # Update all MD files
    md_files = glob.glob(os.path.join(fp.OUTPUT_DIR, "*.md"))
    updated = 0
    
    for filepath in md_files:
        fn = os.path.basename(filepath).replace(".md", "")
        if fn not in pub_map:
            print(f"Skipping {fn} - not found in fresh DBLP fetch.")
            continue
            
        m = pub_map[fn]
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse YAML frontmatter
        parts = content.split("---")
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Remove old fields if present
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
                
        # Update state
        if fn in pubs_state:
            pubs_state[fn]["is_conference"] = m["is_conference"]
            pubs_state[fn]["is_journal"] = m["is_journal"]
            pubs_state[fn]["is_archive"] = m["is_archive"]
            
    fp.log(f"Updated {updated} markdown files.")
    
    # We must patch save_state in memory or write a custom save_state here to update the summary
    state["publications"] = pubs_state
    
    # Recalculate summary locally since fp.save_state might not be patched yet
    total = len(pubs_state)
    with_abstract = sum(1 for v in pubs_state.values() if v.get("has_abstract"))
    without_abstract = total - with_abstract
    total_conference = sum(1 for v in pubs_state.values() if v.get("is_conference"))
    total_journal = sum(1 for v in pubs_state.values() if v.get("is_journal"))
    total_archive = sum(1 for v in pubs_state.values() if v.get("is_archive"))

    from datetime import datetime, timezone
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
