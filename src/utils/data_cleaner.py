
import json
from pathlib import Path


INPUT_FILE = Path("data/processed/classified_startups.json")
OUTPUT_FILE = Path("data/processed/cleaned_startups.json")


def clean_records():
    if not INPUT_FILE.exists():
        print("Classified data file not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    cleaned_records = []
    seen_urls = set()

    for record in records:

        title = record.get("title")
        url = record.get("url")

        # Remove records without a title
        if not title or not title.strip():
            continue

        # Remove duplicate URLs
        if url:
            normalized_url = url.strip().rstrip("/").lower()

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

        # Normalize text fields
        record["title"] = title.strip()
        record["category"] = (
            record.get("category") or "other"
        ).lower().strip()

        cleaned_records.append(record)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            cleaned_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("=" * 40)
    print("DATA CLEANING COMPLETED")
    print("=" * 40)
    print(f"Original records: {len(records)}")
    print(f"Cleaned records: {len(cleaned_records)}")
    print(
        f"Removed records: "
        f"{len(records) - len(cleaned_records)}"
    )
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_records()
