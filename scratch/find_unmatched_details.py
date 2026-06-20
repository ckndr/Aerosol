import pandas as pd
import json

excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]
df = df[df['Machine'].notna() | df['Task Description'].notna()]

print("Searching Excel for 'Pneumatic':")
for idx, row in df.iterrows():
    desc = str(row['Task Description'])
    if 'pneumatic' in desc.lower():
        print(f"Row {idx+1} | Machine: {row['Machine']} | Desc: {desc} | Remarks: {row['Remarks']}")

print("\nSearching Excel for 'tray':")
for idx, row in df.iterrows():
    desc = str(row['Task Description'])
    if 'tray' in desc.lower():
        print(f"Row {idx+1} | Machine: {row['Machine']} | Desc: {desc} | Remarks: {row['Remarks']}")

print("\nSearching Excel for 'cutter' or 'sharp':")
for idx, row in df.iterrows():
    desc = str(row['Task Description'])
    if 'cutter' in desc.lower() or 'sharp' in desc.lower():
        print(f"Row {idx+1} | Machine: {row['Machine']} | Desc: {desc} | Remarks: {row['Remarks']}")
