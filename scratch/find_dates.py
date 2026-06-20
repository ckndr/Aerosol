import pandas as pd
import re

excel_path = "Aerosol Plant Project Tracker.xlsx"
df = pd.read_excel(excel_path, sheet_name="TRACKER")
# Row 0 was headers, so the columns actually are:
df.columns = df.iloc[0]
df = df[1:]  # skip the header row in data

# Look at non-null remarks
df_remarks = df[df['Remarks'].notna()]
print(f"Total rows with Remarks: {len(df_remarks)}")

# Let's inspect some of them
for idx, row in df_remarks.head(30).iterrows():
    # print machine, category, task description, and remarks
    print(f"Machine: {row['Machine']} | Desc: {row['Task Description']} | Remarks: {row['Remarks']}")
