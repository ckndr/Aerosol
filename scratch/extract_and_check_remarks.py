import pandas as pd
import json

excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]
df = df[df['Machine'].notna() | df['Task Description'].notna()]

remarks_data = []
for idx, row in df.iterrows():
    rem = str(row['Remarks']).strip() if pd.notna(row['Remarks']) else ""
    remarks_data.append({
        "row": idx + 1,
        "machine": str(row['Machine']).strip(),
        "desc": str(row['Task Description']).strip(),
        "remarks": rem
    })

with open("scratch/remarks_list.json", "w", encoding="utf-8") as f:
    json.dump(remarks_data, f, indent=2)

print("Saved scratch/remarks_list.json")
