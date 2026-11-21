

import json
from pathlib import Path

INPUT_FILE = Path("data/raw/startups.json")
OUTPUT_FILE = Path("data/processed/classified_startups.json")


def classify_record(record):
    title = (record.get("title") or "").lower()

    startup_keywords = [
        "startup", "founded", "founder", "funding",
        "raised", "company"
    ]

    product_keywords = [
        "launch", "introducing", "new product",
        "app", "tool", "platform", "product"
    ]

    discussion_keywords = [
        "ask hn", "tell hn", "show hn",
        "discussion", "opinion"
    ]

    if any(word in title for word in discussion_keywords):
        category = "discussion"

    elif any(word in title for word in startup_keywords):
        category = "startup"

    elif any(word in title for word in product_keywords):
        category = "product"

    else:
        category = "article"

    return {
        **record,
        "category": category,
        "summary": title,
        "relevance": "unknown",
        "reason": "Classified using Python keyword matching.",
        "classification_status": "success",
        "classification_method": "offline_keyword"
    }


def process_records():
    if not INPUT_FILE.exists():
        print("Startup data file not found!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    results = []

    for index, record in enumerate(records, start=1):
        result = classify_record(record)
        results.append(result)

        print(
            f"{index}/{len(records)} - "
            f"{result['category']}: {record.get('title')}"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nClassification completed!")
    print("Total records:", len(results))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    process_records()


