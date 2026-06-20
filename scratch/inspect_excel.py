import pandas as pd
import json

excel_path = "Aerosol Plant Project Tracker.xlsx"
try:
    xls = pd.ExcelFile(excel_path)
    result = {"sheets": xls.sheet_names, "sheets_data": {}}
    for sheet in xls.sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        # convert column names to string and replace non-ascii chars
        cols = [str(c).encode('ascii', errors='replace').decode('ascii') for c in df.columns]
        head_rows = []
        for idx, row in df.head(5).iterrows():
            row_dict = {}
            for col_idx, val in enumerate(row):
                val_str = str(val).encode('ascii', errors='replace').decode('ascii')
                row_dict[cols[col_idx]] = val_str
            head_rows.append(row_dict)
        result["sheets_data"][sheet] = {
            "columns": cols,
            "head": head_rows
        }
    with open("scratch/excel_structure.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("Success! Structure written to scratch/excel_structure.json")
except Exception as e:
    import traceback
    print("Error:", e)
    traceback.print_exc()
