
import requests
import json
import time
from pathlib import Path
from datetime import datetime, timezone

API_URL = "https://hn.algolia.com/api/v1/search"

OUTPUT_FILE = Path("data/raw/startups.json")

SEARCH_TERMS = [
    "startup",
    "product launch",
    "startup funding",
    "founded company",
    "Show HN",
    "YC startup",
    "new product",
    "technology company",
    "SaaS",
    "AI startup"
]

RECORDS_PER_PAGE = 100
MAX_PAGES_PER_TERM = 10
TARGET_RECORDS = 1000


def collect_startups():
    print("Starting startup and product data collection...")

    all_records = {}

    session = requests.Session()

    for term in SEARCH_TERMS:
        print(f"\nSearching for: {term}")

        for page in range(MAX_PAGES_PER_TERM):

            params = {
                "query": term,
                "tags": "story",
                "hitsPerPage": RECORDS_PER_PAGE,
                "page": page
            }

            try:
                response = session.get(
                    API_URL,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()
                data = response.json()

                hits = data.get("hits", [])

                if not hits:
                    break

                for item in hits:
                    record_id = item.get("objectID")

                    if not record_id:
                        continue

                    all_records[record_id] = {
                        "id": record_id,
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "author": item.get("author"),
                        "points": item.get("points"),
                        "created_at": item.get("created_at"),
                        "source": "Hacker News",
                        "search_term": term,
                        "collected_at": datetime.now(
                            timezone.utc
                        ).isoformat()
                    }

                print(
                    f"Page {page + 1}: "
                    f"{len(hits)} records received | "
                    f"Unique total: {len(all_records)}"
                )

                if len(all_records) >= TARGET_RECORDS:
                    break

                time.sleep(0.2)

            except requests.RequestException as error:
                print(f"Error searching {term}: {error}")
                break

        if len(all_records) >= TARGET_RECORDS:
            break

    return list(all_records.values())


def save_to_json(records):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nData saved to:", OUTPUT_FILE)


if __name__ == "__main__":

    print("=" * 50)
    print("STARTUP DATA COLLECTOR")
    print("=" * 50)

    records = collect_startups()

    print("\nCollection completed!")
    print("Total unique records:", len(records))

    save_to_json(records)

    print("\nFirst 5 records:")

    for record in records[:5]:
        print("\nTitle:", record["title"])
        print("Source:", record["source"])
        print("URL:", record["url"])

    print("\nFinal record count:", len(records))


