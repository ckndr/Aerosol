import json
import re

with open("tasks.json", "r", encoding="utf-8") as f:
    data = json.load(f)
tasks = data.get("tasks", [])

count_with_dates = 0
for t in tasks:
    rem = t.get("remarks", "")
    if re.search(r'\d{4}-\d{2}-\d{2}', str(rem)) or re.search(r'\d{1,2}\s+[JFMASOND][a-z]+\s+\d{4}', str(rem)):
        count_with_dates += 1
        print(f"ID: {t['id']} | Machine: {t['machine']} | Desc: {t['desc']} | Remarks: {t['remarks']}")

print(f"Total tasks with dates in tasks.json remarks: {count_with_dates}")
