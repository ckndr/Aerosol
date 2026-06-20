import json
import pandas as pd

# Load tasks.json
with open("tasks.json", "r", encoding="utf-8") as f:
    tasks_data = json.load(f)

tasks = tasks_data.get("tasks", [])
print(f"Total tasks in tasks.json: {len(tasks)}")

# Load Excel
excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]

excel_tasks = []
for idx, row in df.iterrows():
    if pd.isna(row['Machine']) and pd.isna(row['Task Description']):
        continue
    excel_tasks.append({
        "machine": str(row['Machine']).strip() if pd.notna(row['Machine']) else "",
        "category": str(row['Category']).strip() if pd.notna(row['Category']) else "",
        "desc": str(row['Task Description']).strip() if pd.notna(row['Task Description']) else "",
        "remarks": str(row['Remarks']).strip() if pd.notna(row['Remarks']) else ""
    })

print(f"Total tasks in Excel TRACKER sheet: {len(excel_tasks)}")

# Let's see how many match exactly
matched = 0
unmatched = []
for et in excel_tasks:
    # try to find in tasks.json
    found = False
    for t in tasks:
        # compare case-insensitive and stripped
        if (t['machine'].lower() == et['machine'].lower() and 
            t['category'].lower() == et['category'].lower() and 
            t['desc'].lower() == et['desc'].lower()):
            found = True
            matched += 1
            break
    if not found:
        unmatched.append(et)

print(f"Exactly matched by (machine, category, desc): {matched}")
print(f"Unmatched: {len(unmatched)}")
if unmatched:
    print("Some unmatched tasks from Excel:")
    for ut in unmatched[:5]:
        print(ut)
