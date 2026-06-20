import json
import pandas as pd
import re

def normalize_text(text):
    if not text:
        return ""
    text = str(text).lower().strip()
    # Replace smart dashes, en dashes, em dashes with hyphen
    text = re.sub(r'[\u2013\u2014\u2015\u2212]', '-', text)
    # Replace non-alphanumeric characters with space (except letters, digits, and basic punctuation)
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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

matched_count = 0
unmatched_excel = []
unmatched_json = list(tasks)

for et in excel_tasks:
    # Match criteria:
    # 1. Normalize machine
    # 2. Normalize desc
    et_machine_norm = normalize_text(et['machine'])
    et_desc_norm = normalize_text(et['desc'])
    
    found = None
    for t in unmatched_json:
        t_machine_norm = normalize_text(t['machine'])
        t_desc_norm = normalize_text(t['desc'])
        
        if et_machine_norm == t_machine_norm and et_desc_norm == t_desc_norm:
            found = t
            break
            
    if found:
        unmatched_json.remove(found)
        matched_count += 1
    else:
        unmatched_excel.append(et)

print(f"Total Excel: {len(excel_tasks)}")
print(f"Total JSON: {len(tasks)}")
print(f"Matched after normalization: {matched_count}")
print(f"Unmatched Excel count: {len(unmatched_excel)}")
print(f"Unmatched JSON count: {len(unmatched_json)}")

if unmatched_excel:
    print("\nUnmatched Excel tasks:")
    for et in unmatched_excel[:10]:
        print(f"  Row {et['row_num']}: {et['machine']} | {et['desc']}")

if unmatched_json:
    print("\nUnmatched JSON tasks:")
    for jt in unmatched_json[:10]:
        print(f"  ID {jt['id']}: {jt['machine']} | {jt['desc']}")
