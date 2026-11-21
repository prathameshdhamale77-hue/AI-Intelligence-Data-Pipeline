
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

API_URL = "https://remotive.com/api/remote-jobs"
OUTPUT_FILE = Path("data/raw/ai_jobs.json")

AI_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data scientist",
    "data science",
    "llm",
    "generative ai",
    "ai engineer",
    "ml engineer",
    "nlp",
    "computer vision",
    "data engineer",
    "ai developer",
    "research scientist",
    "machine learning engineer"
]

DAYS_TO_COLLECT = 30


def collect_ai_jobs():
    print("Fetching jobs from Remotive...")

    try:
        response = requests.get(
            API_URL,
            params={"limit": 500},
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        all_jobs = data.get("jobs", [])

        print("Total jobs received from API:", len(all_jobs))

        cutoff = datetime.now(timezone.utc) - timedelta(
            days=DAYS_TO_COLLECT
        )

        collected_jobs = []

        for job in all_jobs:
            title = job.get("title") or ""
            title_text = title.lower()

            # Match AI-related job titles only
            if not any(
                keyword in title_text
                for keyword in AI_KEYWORDS
            ):
                continue

            posted_at = job.get("publication_date")

            if not posted_at:
                continue

            try:
                posted_date = datetime.fromisoformat(
                    posted_at.replace("Z", "+00:00")
                )

                if posted_date.tzinfo is None:
                    posted_date = posted_date.replace(
                        tzinfo=timezone.utc
                    )

            except ValueError:
                continue

            if posted_date < cutoff:
                continue

            collected_jobs.append({
                "job_id": job.get("id"),
                "title": title,
                "company": job.get("company_name"),
                "category": job.get("category"),
                "job_type": job.get("job_type"),
                "location": job.get("candidate_required_location"),
                "salary": job.get("salary"),
                "description": job.get("description"),
                "publication_date": posted_at,
                "url": job.get("url"),
                "source": "Remotive",
                "collected_at": datetime.now(
                    timezone.utc
                ).isoformat()
            })

        return collected_jobs

    except requests.RequestException as error:
        print("Job collection error:", error)
        return []


def save_jobs(jobs):
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
            jobs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":

    print("=" * 45)
    print("AI JOB LISTINGS COLLECTOR")
    print("=" * 45)

    jobs = collect_ai_jobs()

    print(
        f"\nAI-related jobs collected from the last "
        f"{DAYS_TO_COLLECT} days:",
        len(jobs)
    )

    save_jobs(jobs)

    print("\nFirst 5 matching jobs:")

    for job in jobs[:5]:
        print("\nTitle:", job["title"])
        print("Company:", job["company"])
        print("Posted:", job["publication_date"])
        print("URL:", job["url"])

    print("\nJob collection completed!")

