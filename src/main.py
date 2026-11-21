
import os
import json
from pathlib import Path

from src.config import PROJECT_NAME

from src.collectors.startup_collector import (
    collect_startups,
    save_to_json
)

from src.collectors.news_collector import (
    collect_ai_news,
    save_news
)

from src.collectors.job_collector import (
    collect_ai_jobs,
    save_jobs
)

from src.collectors.research_collector import (
    collect_research_papers
)

from src.ai.classifier import process_records

from src.database.database import (
    create_database,
    insert_startups,
    verify_database
)

from src.exporters.csv_exporter import export_to_csv

from src.exporters.google_sheets import (
    main as export_to_google_sheets,
    connect_to_google_sheets,
    upload_json_to_sheet
)

from src.utils.pipeline_logger import log_pipeline_event


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# -----------------------------------------
# PROJECT INITIALIZATION
# -----------------------------------------

def initialize_project():

    print("=" * 50)
    print(PROJECT_NAME)
    print("=" * 50)

    directories = [
        PROJECT_ROOT / "data" / "raw",
        PROJECT_ROOT / "data" / "processed",
        PROJECT_ROOT / "logs"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory ready: {directory.name}")

    print("\nProject initialized successfully!")


# -----------------------------------------
# PIPELINE STAGE EXECUTION
# -----------------------------------------

def execute_stage(stage_name, function):

    print("\n" + "=" * 50)
    print(f"STAGE: {stage_name}")
    print("=" * 50)

    try:

        result = function()

        records_count = (
            len(result)
            if isinstance(result, list)
            else result if isinstance(result, int)
            else 0
        )

        log_pipeline_event(
            stage=stage_name,
            status="SUCCESS",
            records_processed=records_count,
            message="Stage completed successfully."
        )

        print(
            f"[SUCCESS] {stage_name}: "
            f"{records_count} records"
        )

        return result

    except Exception as error:

        log_pipeline_event(
            stage=stage_name,
            status="FAILED",
            records_processed=0,
            message=str(error)
        )

        print(f"[FAILED] {stage_name}: {error}")

        raise


# -----------------------------------------
# DATA COLLECTION
# -----------------------------------------

def collect_startup_data():

    records = collect_startups()
    save_to_json(records)

    return records


def collect_news_data():

    records = collect_ai_news()
    save_news(records)

    return records


def collect_job_data():

    records = collect_ai_jobs()
    save_jobs(records)

    return records


def collect_research_data():

    return collect_research_papers()


# -----------------------------------------
# AI CLASSIFICATION
# -----------------------------------------

def classify_startup_data():

    process_records()

    output_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "classified_startups.json"
    )

    if not output_file.exists():
        raise FileNotFoundError(
            "Classified startup file was not created."
        )

    with open(output_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    return len(records)


# -----------------------------------------
# DATABASE STORAGE
# -----------------------------------------

def store_database():

    classified_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "classified_startups.json"
    )

    with open(classified_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    connection = create_database()

    try:
        insert_startups(connection, records)
        verify_database(connection)

    finally:
        connection.close()

    return len(records)


# -----------------------------------------
# CSV EXPORT
# -----------------------------------------

def export_csv_stage():

    export_to_csv()

    classified_file = (
        PROJECT_ROOT /
        "data" /
        "processed" /
        "classified_startups.json"
    )

    with open(classified_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    return len(records)


# -----------------------------------------
# GOOGLE SHEETS EXPORT
# -----------------------------------------

def export_google_sheets_stage():

    export_to_google_sheets()

    dataset_files = [
        "data/raw/startups.json",
        "data/raw/ai_news.json",
        "data/raw/ai_jobs.json",
        "data/processed/classified_startups.json",
        "data/raw/research_papers.json",
        "logs/pipeline_logs.json"
    ]

    total_records = 0

    for filename in dataset_files:

        file_path = PROJECT_ROOT / filename

        if file_path.exists():

            with open(file_path, "r", encoding="utf-8") as file:
                records = json.load(file)

            if isinstance(records, list):
                total_records += len(records)

    return total_records


# -----------------------------------------
# PIPELINE LOG SYNCHRONIZATION
# -----------------------------------------

def sync_pipeline_logs():

    log_file = (
        PROJECT_ROOT /
        "logs" /
        "pipeline_logs.json"
    )

    with open(log_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    spreadsheet = connect_to_google_sheets()

    upload_json_to_sheet(
        spreadsheet,
        log_file,
        "Pipeline_Logs"
    )

    return len(records)


# -----------------------------------------
# MAIN PIPELINE
# -----------------------------------------

def main():

    os.chdir(PROJECT_ROOT)

    print("\n" + "#" * 55)
    print("STARTING AI INTELLIGENCE DATA PIPELINE")
    print("#" * 55)

    initialize_project()

    try:

        execute_stage(
            "Startup Collection",
            collect_startup_data
        )

        execute_stage(
            "AI News Collection",
            collect_news_data
        )

        execute_stage(
            "AI Job Collection",
            collect_job_data
        )

        execute_stage(
            "Research Paper Collection",
            collect_research_data
        )

        execute_stage(
            "Startup Classification",
            classify_startup_data
        )

        execute_stage(
            "SQLite Database Storage",
            store_database
        )

        execute_stage(
            "CSV Export",
            export_csv_stage
        )

        execute_stage(
            "Google Sheets Export",
            export_google_sheets_stage
        )

        execute_stage(
            "Pipeline Logs Synchronization",
            sync_pipeline_logs
        )

        print("\n" + "#" * 55)
        print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
        print("#" * 55)

    except Exception as error:

        print("\n" + "#" * 55)
        print("PIPELINE EXECUTION FAILED!")
        print("Reason:", error)
        print("#" * 55)


if __name__ == "__main__":
    main()
