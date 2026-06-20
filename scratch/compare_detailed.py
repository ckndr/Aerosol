import json
import pandas as pd
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Load tasks.json
with open("tasks.json", "r", encoding="utf-8") as f:
    tasks_data = json.load(f)
tasks = tasks_data.get("tasks", [])

# Load Excel
excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]
df = df[df['Machine'].notna() | df['Task Description'].notna()]

excel_tasks = []
for idx, row in df.iterrows():
    excel_tasks.append({
        "excel_row_num": idx + 1,  # 1-indexed Excel row
        "machine": str(row['Machine']).strip() if pd.notna(row['Machine']) else "",
        "category": str(row['Category']).strip() if pd.notna(row['Category']) else "",
        "desc": str(row['Task Description']).strip() if pd.notna(row['Task Description']) else "",
        "priority": str(row['Priority']).strip() if pd.notna(row['Priority']) else "",
        "progress": float(row['Progress']) if pd.notna(row['Progress']) else 0.0,
        "status": str(row['Status']).strip() if pd.notna(row['Status']) else "",
        "responsible": str(row['Responsible']).strip() if pd.notna(row['Responsible']) else "",
        "remarks": str(row['Remarks']).strip() if pd.notna(row['Remarks']) else "",
        "updated": str(row['Updated']).strip() if pd.notna(row['Updated']) else ""
    })

print(f"Loaded {len(tasks)} tasks from json and {len(excel_tasks)} tasks from Excel.")

# We want to match each Excel task with a JSON task.
# Let's find best match based on machine, category, desc.
matches = []
unmatched_excel = []
unmatched_json = list(tasks)

for et in excel_tasks:
    best_t = None
    best_score = 0
    # first try exact match
    for t in unmatched_json:
        if (t['machine'].strip().lower() == et['machine'].lower() and 
            t['category'].strip().lower() == et['category'].lower() and 
            t['desc'].strip().lower() == et['desc'].lower()):
            best_t = t
            best_score = 1.0
            break
            
    if best_score < 1.0:
        # try exact desc + machine match
        for t in unmatched_json:
            if (t['machine'].strip().lower() == et['machine'].lower() and 
                t['desc'].strip().lower() == et['desc'].lower()):
                best_t = t
                best_score = 0.95
                break
                
    if best_score < 0.95:
        # try fuzzy match
        for t in unmatched_json:
            # check description similarity
            score = similarity(t['desc'], et['desc'])
            if t['machine'].strip().lower() == et['machine'].lower():
                score += 0.2
            if t['category'].strip().lower() == et['category'].lower():
                score += 0.1
            if score > best_score:
                best_score = score
                best_t = t
                
    if best_t and best_score >= 0.7:
        unmatched_json.remove(best_t)
        matches.append((et, best_t, best_score))
    else:
        unmatched_excel.append(et)

print(f"Matched {len(matches)} tasks.")
print(f"Unmatched Excel: {len(unmatched_excel)}")
print(f"Unmatched JSON: {len(unmatched_json)}")

# Show matches with lower confidence or unmatched
low_conf = [m for m in matches if m[2] < 1.0]
print(f"\nLow confidence matches (< 1.0): {len(low_conf)}")
for et, jt, score in low_conf[:10]:
    print(f"Score: {score:.2f}")
    print(f"  Excel: row={et['excel_row_num']} | Machine={et['machine']} | Desc={et['desc']}")
    print(f"  JSON:  id={jt['id']} | Machine={jt['machine']} | Desc={jt['desc']}")

if unmatched_excel:
    print("\nUnmatched Excel tasks:")
    for et in unmatched_excel[:10]:
        print(f"  Row {et['excel_row_num']}: Machine={et['machine']} | Desc={et['desc']}")

if unmatched_json:
    print("\nUnmatched JSON tasks:")
    for jt in unmatched_json[:10]:
        print(f"  ID {jt['id']}: Machine={jt['machine']} | Desc={jt['desc']}")
