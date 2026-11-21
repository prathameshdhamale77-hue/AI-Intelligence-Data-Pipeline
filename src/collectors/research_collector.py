
import requests
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_URL = "https://export.arxiv.org/api/query"

SEARCH_QUERY = (
    'all:"artificial intelligence" OR '
    'all:"machine learning" OR '
    'all:"large language model"'
)


def collect_research_papers(max_results=100):

    print("Collecting AI research papers from arXiv...")

    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    papers = []

    for entry in root.findall("atom:entry", namespace):

        title = entry.findtext(
            "atom:title",
            default="",
            namespaces=namespace
        ).strip()

        summary = entry.findtext(
            "atom:summary",
            default="",
            namespaces=namespace
        ).strip()

        published = entry.findtext(
            "atom:published",
            default="",
            namespaces=namespace
        )

        paper_id = entry.findtext(
            "atom:id",
            default="",
            namespaces=namespace
        )

        authors = [
            author.findtext(
                "atom:name",
                default="",
                namespaces=namespace
            )
            for author in entry.findall(
                "atom:author",
                namespace
            )
        ]

        papers.append({
            "title": title,
            "authors": authors,
            "summary": summary,
            "published": published,
            "url": paper_id,
            "source": "arXiv",
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat()
        })

    output_dir = PROJECT_ROOT / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "research_papers.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            papers,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Collected {len(papers)} research papers.")
    print(f"Saved to: {output_file}")

    return papers


if __name__ == "__main__":
    collect_research_papers()
