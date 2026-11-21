

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

API_URL = "https://hn.algolia.com/api/v1/search_by_date"
OUTPUT_FILE = Path("data/raw/ai_news.json")

SEARCH_TERMS = [
    "AI",
    "artificial intelligence",
    "machine learning",
    "LLM"
]


def collect_ai_news():

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    timestamp = int(cutoff.timestamp())

    all_news = {}
    
    for term in SEARCH_TERMS:
        print(f"Searching: {term}")

        params = {
            "query": term,
            "tags": "story",
            "numericFilters": f"created_at_i>{timestamp}",
            "hitsPerPage": 30
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            for item in data.get("hits", []):
                all_news[item["objectID"]] = {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "author": item.get("author"),
                    "points": item.get("points"),
                    "created_at": item.get("created_at"),
                    "source": "Hacker News",
                    "collected_at": datetime.now(
                        timezone.utc
                    ).isoformat()
                }

        except requests.RequestException as error:
            print(f"Error searching {term}: {error}")

    return list(all_news.values())


def save_news(news):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(news, file, indent=4, ensure_ascii=False)

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":

    print("AI NEWS COLLECTOR")
    print("=" * 40)

    news = collect_ai_news()

    print("\nTotal news collected:", len(news))

    save_news(news)

    for item in news[:5]:
        print("\nTitle:", item["title"])
        print("URL:", item["url"])

    print("\nCollection completed!")
