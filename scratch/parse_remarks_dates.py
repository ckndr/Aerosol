import pandas as pd
import re

def is_date(val):
    val_str = str(val).strip()
    # Check YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}', val_str):
        return val_str[:10]
    # Check DMY format e.g. 15/05/2026 or 15-05-2026
    dmy = re.match(r'^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', val_str)
    if dmy:
        return f"{dmy.group(3)}-{dmy.group(2).zfill(2)}-{dmy.group(1).zfill(2)}"
    # Check Excel serial number (typically 5 digits starting with 4, e.g. 46159)
    if re.match(r'^\d{5}$', val_str):
        try:
            # Excel epoch is 1899-12-30 due to leap year bug
            dt = pd.to_datetime(int(val_str), unit='D', origin='1899-12-30')
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    return None

excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
df.columns = df.iloc[0]
df = df[1:]
df = df[df['Machine'].notna() | df['Task Description'].notna()]

date_count = 0
text_count = 0
empty_count = 0

for idx, row in df.iterrows():
    val = row['Remarks']
    if pd.isna(val) or str(val).strip() == "" or str(val).strip().lower() == "nan":
        empty_count += 1
        continue
    parsed = is_date(val)
    if parsed:
        date_count += 1
        print(f"Row {idx+1} | Date: {parsed} | Original: {val} | Task: {row['Task Description']}")
    else:
        text_count += 1
        print(f"Row {idx+1} | Text: {val} | Task: {row['Task Description']}")

print(f"\nSummary:\n  Dates: {date_count}\n  Texts: {text_count}\n  Empty: {empty_count}\n  Total: {len(df)}")
