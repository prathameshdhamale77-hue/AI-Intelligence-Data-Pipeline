
import json
import csv
from pathlib import Path

INPUT_FILE = Path("data/processed/classified_startups.json")
OUTPUT_FILE = Path("data/processed/startups_export.csv")


def export_to_csv():

    if not INPUT_FILE.exists():
        print("Classified JSON file not found!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not records:
        print("No records available to export.")
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(dict.fromkeys(
        key for record in records for key in record.keys()
    ))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print("CSV export completed!")
    print("Total records exported:", len(records))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    export_to_csv()
