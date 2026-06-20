import json
import pandas as pd

with open("tasks.json", "r", encoding="utf-8") as f:
    tasks_data = json.load(f)
tasks = tasks_data.get("tasks", [])

excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]
df = df[df['Machine'].notna() | df['Task Description'].notna()]

excel_tasks = df.to_dict('records')

print(f"tasks.json count: {len(tasks)}")
print(f"Excel count: {len(excel_tasks)}")

mismatches = 0
for idx, (t, et) in enumerate(zip(tasks, excel_tasks)):
    et_machine = str(et['Machine']).strip()
    et_desc = str(et['Task Description']).strip()
    
    match_machine = t['machine'].strip().lower() == et_machine.lower()
    match_desc = t['desc'].strip().lower() == et_desc.lower()
    
    if not (match_machine and match_desc):
        print(f"Mismatch at index {idx}:")
        print(f"  tasks.json: Machine={t['machine']} | Desc={t['desc']}")
        print(f"  Excel:      Machine={et_machine} | Desc={et_desc}")
        mismatches += 1
        if mismatches > 10:
            break
if mismatches == 0:
    print("Perfect match in order!")
