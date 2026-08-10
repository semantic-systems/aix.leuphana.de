import json
import os

state_file = "_publications/.state.json"
with open(state_file, "r") as f:
    state = json.load(f)

pubs = state["publications"]

# Group by title
title_map = {}
for k, v in pubs.items():
    t = v.get("title", "").strip().lower()
    title_map.setdefault(t, []).append(k)

to_delete = []
for t, keys in title_map.items():
    if len(keys) > 1:
        # Sort by key length. Keep the shortest key (the 100-character one)
        keys.sort(key=len)
        keep = keys[0]
        remove_keys = keys[1:]
        
        for rk in remove_keys:
            # Transfer abstract if needed
            if pubs[rk].get("has_abstract") and not pubs[keep].get("has_abstract"):
                pubs[keep]["has_abstract"] = True
                
                # Copy abstract from the file we are deleting
                fpath_r = pubs[rk]["file"]
                fpath_k = pubs[keep]["file"]
                if os.path.exists(fpath_r) and os.path.exists(fpath_k):
                    with open(fpath_r, "r") as f1:
                        content_r = f1.read()
                    if "> **Abstract:**" in content_r:
                        ab_block = content_r[content_r.find("> **Abstract:**"):]
                        with open(fpath_k, "r") as f2:
                            content_k = f2.read()
                        if "*Abstract not available.*" in content_k:
                            content_k = content_k.replace("*Abstract not available.*", ab_block)
                            with open(fpath_k, "w") as f2:
                                f2.write(content_k)
                                
            # Delete file
            fpath = pubs[rk]["file"]
            if os.path.exists(fpath):
                os.remove(fpath)
                print(f"Deleted duplicate file: {fpath}")
            
            to_delete.append(rk)

for k in to_delete:
    del pubs[k]

if to_delete:
    print(f"Removed {len(to_delete)} duplicate entries from state.")
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
else:
    print("No duplicates found.")
