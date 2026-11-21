
import os
import json
import gspread
from pathlib import Path
from dotenv import load_dotenv

# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")


def connect_to_google_sheets():
    """Connect to Google Sheets."""

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            "credentials.json not found."
        )

    if not SPREADSHEET_ID:
        raise ValueError(
            "GOOGLE_SHEET_ID missing from .env."
        )

    client = gspread.service_account(
        filename=str(CREDENTIALS_FILE)
    )

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    print(
        f"Connected to: {spreadsheet.title}"
    )

    return spreadsheet


def upload_json_to_sheet(
    spreadsheet,
    file_path,
    worksheet_name
):
    """Upload JSON records into a worksheet."""

    if not file_path.exists():
        print(
            f"Skipping {worksheet_name}: "
            "file not found."
        )
        return

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        print(
            f"Skipping {worksheet_name}: "
            "no valid records."
        )
        return

    headers = list(dict.fromkeys(
        key
        for record in records
        if isinstance(record, dict)
        for key in record.keys()
    ))

    if not headers:
        print(
            f"Skipping {worksheet_name}: "
            "no columns found."
        )
        return

    rows = [headers]

    for record in records:

        if not isinstance(record, dict):
            continue

        row = []

        for header in headers:

            value = record.get(header, "")

            if isinstance(value, (dict, list)):
                value = json.dumps(
                    value,
                    ensure_ascii=False
                )

            row.append(value)

        rows.append(row)

    worksheet = spreadsheet.worksheet(
        worksheet_name
    )

    worksheet.clear()

    worksheet.update(
        rows,
        value_input_option="RAW"
    )

    print(
        f"Uploaded {len(rows) - 1} records "
        f"to {worksheet_name}."
    )


def main():

    print("Starting Google Sheets export...")

    spreadsheet = connect_to_google_sheets()

    # All six datasets
    datasets = [
        (
            "data/raw/startups.json",
            "Startups"
        ),
        (
            "data/raw/ai_news.json",
            "AI_News"
        ),
        (
            "data/raw/ai_jobs.json",
            "AI_Jobs"
        ),
        (
            "data/processed/classified_startups.json",
            "Classified_Data"
        ),
        (
            "data/raw/research_papers.json",
            "Research_Papers"
        ),
        (
            "logs/pipeline_logs.json",
            "Pipeline_Logs"
        )
    ]

    for file_path, worksheet_name in datasets:

        upload_json_to_sheet(
            spreadsheet,
            PROJECT_ROOT / file_path,
            worksheet_name
        )

    print(
        "Google Sheets export completed!"
    )


if __name__ == "__main__":
    main()



