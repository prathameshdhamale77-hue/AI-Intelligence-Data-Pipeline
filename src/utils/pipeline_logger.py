
import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_FILE = PROJECT_ROOT / "logs" / "pipeline_logs.json"


def log_pipeline_event(
    stage,
    status,
    records_processed=0,
    message=""
):
    """Record pipeline execution details."""

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    event = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "stage": stage,
        "status": status,
        "records_processed": records_processed,
        "message": message
    }

    logs = []

    if LOG_FILE.exists():
        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            logs = json.load(file)

    logs.append(event)

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            logs,
            file,
            indent=4
        )

    print(
        f"[{status}] {stage}: "
        f"{records_processed} records"
    )


if __name__ == "__main__":

    log_pipeline_event(
        stage="Google Sheets Integration",
        status="SUCCESS",
        records_processed=2170,
        message="Five datasets processed."
    )
