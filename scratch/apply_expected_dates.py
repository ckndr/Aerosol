import json
import pandas as pd
import re
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower().strip()
    text = re.sub(r'[\u2013\u2014\u2015\u2212]', '-', text)
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_date(val):
    val_str = str(val).strip()
    if pd.isna(val) or val_str == "" or val_str.lower() == "nan":
        return None
    # YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}', val_str):
        return val_str[:10]
    # DD/MM/YYYY or DD-MM-YYYY
    dmy = re.match(r'^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', val_str)
    if dmy:
        return f"{dmy.group(3)}-{dmy.group(2).zfill(2)}-{dmy.group(1).zfill(2)}"
    # Excel serial number
    if re.match(r'^\d{5}$', val_str):
        try:
            dt = pd.to_datetime(int(val_str), unit='D', origin='1899-12-30')
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    return None

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
        "row_num": idx + 1,
        "machine": str(row['Machine']).strip() if pd.notna(row['Machine']) else "",
        "category": str(row['Category']).strip() if pd.notna(row['Category']) else "",
        "desc": str(row['Task Description']).strip() if pd.notna(row['Task Description']) else "",
        "remarks": str(row['Remarks']).strip() if pd.notna(row['Remarks']) else ""
    })

# We'll match tasks.
# Keep track of which JSON tasks have been matched
matched_json_ids = set()
updates = []

for et in excel_tasks:
    date_val = parse_date(et['remarks'])
    if not date_val:
        continue # only care if there is a date in the remarks column
        
    et_machine_norm = normalize_text(et['machine'])
    et_desc_norm = normalize_text(et['desc'])
    
    # 1. Exact match (excluding already matched)
    found = None
    for t in tasks:
        if t['id'] in matched_json_ids:
            continue
        t_machine_norm = normalize_text(t['machine'])
        t_desc_norm = normalize_text(t['desc'])
        if et_machine_norm == t_machine_norm and et_desc_norm == t_desc_norm:
            found = t
            break
            
    # 2. Fuzzy match if exact match not found
    if not found:
        best_score = 0
        best_t = None
        for t in tasks:
            if t['id'] in matched_json_ids:
                continue
            if normalize_text(t['machine']) == et_machine_norm:
                # calculate similarity of description
                score = similarity(t['desc'], et['desc'])
                if score > best_score and score >= 0.7:
                    best_score = score
                    best_t = t
        if best_t:
            found = best_t
            print(f"Fuzzy Matched: Excel '{et['desc']}' -> JSON '{found['desc']}' (Score: {best_score:.2f})")
            
    if found:
        matched_json_ids.add(found['id'])
        # set expectedDate
        old_expected = found.get('expectedDate', '')
        found['expectedDate'] = date_val
        updates.append({
            "id": found['id'],
            "machine": found['machine'],
            "desc": found['desc'],
            "expectedDate": date_val
        })
    else:
        print(f"WARNING: Could not match Excel row {et['row_num']} having date {date_val}: {et['machine']} | {et['desc']}")

# Show summary of updates
print(f"\nTotal tasks in json: {len(tasks)}")
print(f"Total tasks updated with expectedDate: {len(updates)}")

# Write back to tasks.json
with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks_data, f, indent=2)
print("Updated tasks.json saved successfully.")
