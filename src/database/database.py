
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "processed" / "classified_startups.json"
DATABASE_FILE = BASE_DIR / "data" / "ai_intelligence.db"


def create_database():
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS startups (
            id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            author TEXT,
            points INTEGER,
            created_at TEXT,
            source TEXT,
            category TEXT,
            summary TEXT,
            relevance TEXT,
            classification_method TEXT
        )
    """)

    connection.commit()
    return connection


def insert_startups(connection, records):
    cursor = connection.cursor()

    for record in records:
        cursor.execute("""
            INSERT OR REPLACE INTO startups (
                id, title, url, author, points,
                created_at, source, category,
                summary, relevance, classification_method
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(record.get("id") or record.get("url") or record.get("title")),
            record.get("title"),
            record.get("url"),
            record.get("author"),
            record.get("points"),
            record.get("created_at"),
            record.get("source"),
            record.get("category"),
            record.get("summary"),
            record.get("relevance"),
            record.get("classification_method")
        ))

    connection.commit()


def verify_database(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM startups")
    total = cursor.fetchone()[0]

    print("\nDatabase verification")
    print("--------------------")
    print("Total stored records:", total)

    cursor.execute("""
        SELECT title, category
        FROM startups
        LIMIT 5
    """)

    print("\nSample records:")

    for row in cursor.fetchall():
        print("Title:", row[0])
        print("Category:", row[1])
        print("-" * 35)


def main():
    print("=" * 45)
    print("AI INTELLIGENCE DATABASE")
    print("=" * 45)

    if not INPUT_FILE.exists():
        print("Classified startup data not found!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    connection = create_database()

    insert_startups(connection, records)

    verify_database(connection)

    connection.close()

    print("\nDatabase saved to:", DATABASE_FILE)
    print("Database operation completed!")


if __name__ == "__main__":
    main()
