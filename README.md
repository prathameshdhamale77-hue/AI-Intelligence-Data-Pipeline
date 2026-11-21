
# AI Intelligence Data Pipeline

An automated Python-based data pipeline that collects, processes, classifies, stores, and exports AI-related intelligence from multiple online sources.

## Overview

The AI Intelligence Data Pipeline automates the collection and organization of startup-related information, AI news, AI job listings, and research papers.

It combines data collection, keyword-based classification, SQLite database storage, CSV export, and Google Sheets integration into one execution workflow.

## Key Features

- **Startup Data Collection:** Collects startup-related stories using the Hacker News Algolia API.
- **AI News Collection:** Collects recent AI-related news using keyword-based searches.
- **AI Job Collection:** Retrieves AI-related remote job listings through the Remotive API.
- **Research Paper Collection:** Collects research papers using the arXiv API.
- **Automated Classification:** Categorizes collected records using Python keyword-based classification.
- **Database Storage:** Stores classified records in an SQLite database.
- **CSV Export:** Exports processed startup records into CSV format.
- **Google Sheets Integration:** Automatically uploads datasets into six Google Sheets tabs.
- **Pipeline Logging:** Tracks execution stages, processing counts, and errors.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Requests | API communication |
| Hacker News Algolia API | Startup and AI news collection |
| Remotive API | Remote job collection |
| arXiv API | Research paper collection |
| SQLite | Database storage |
| Pandas | Data processing and CSV workflows |
| Google Sheets API | Cloud-based data export |
| JSON | Raw and processed data storage |

## Project Architecture

The pipeline follows these stages:

1. Data collection from external APIs.
2. Storage of collected records in JSON files.
3. Keyword-based classification of startup records.
4. Storage of classified records in SQLite.
5. Export of processed records to CSV.
6. Upload of datasets to Google Sheets.
7. Execution logging and monitoring.

## Project Structure

```text
AI_Intelligence_Data_Pipeline/
│
├── src/
│   ├── collectors/
│   │   ├── startup_collector.py
│   │   ├── news_collector.py
│   │   ├── job_collector.py
│   │   └── research_collector.py
│   │
│   ├── ai/
│   │   └── classifier.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── exporters/
│   │   ├── csv_exporter.py
│   │   └── google_sheets.py
│   │
│   ├── utils/
│   │   └── pipeline_logger.py
│   │
│   ├── config.py
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── ai_intelligence.db
│
├── logs/
│
├── docs/
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Intelligence_Data_Pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add the required Google Sheets configuration:

```env
GOOGLE_SHEET_ID=your_google_sheet_id
```

### 5. Configure Google Sheets API

- Create a Google Cloud project.
- Enable the Google Sheets API.
- Create a service account.
- Download its JSON credentials file.
- Save it as `credentials.json` in the project root.
- Share your Google spreadsheet with the service account email as an Editor.

Keep credentials private. Never commit `.env` or `credentials.json` to GitHub.

## Running the Pipeline

From the project root, execute:

```bash
python -m src.main
```

The pipeline automatically executes the collection, classification, database, export, and logging stages.

## Google Sheets Integration

The pipeline exports data into six worksheets:

1. Startups
2. AI_News
3. AI_Jobs
4. Research_Papers
5. Classified_Data
6. Pipeline_Logs

Each worksheet is populated using the corresponding collected or processed JSON dataset.

## Output Files

| Output | Description |
|---|---|
| startups.json | Collected startup-related records |
| ai_news.json | Collected AI news |
| ai_jobs.json | Collected AI job listings |
| research_papers.json | Collected research papers |
| classified_startups.json | Classified startup records |
| startups_export.csv | CSV export |
| ai_intelligence.db | SQLite database |
| pipeline_logs.json | Pipeline execution logs |

## Current Execution Results

A successful integrated execution produced:

| Dataset / Stage | Records |
|---|---:|
| Startup records | 1,000 |
| AI news records | 61 |
| AI job records | 1 |
| Research papers | 100 |
| Classified startup records | 1,000 |
| SQLite stored records | 1,000 |
| CSV exported records | 1,000 |
| Google Sheets uploaded records | 2,179 |

These figures represent one execution and may change when the pipeline runs again.

## Current Limitations

- Startup records are collected from keyword-matched Hacker News stories and are not independently verified companies.
- Classification currently uses Python keyword matching rather than an LLM-based classifier.
- AI job collection may return limited results depending on source availability and filtering.
- SQLite is used for local database storage.
- Data freshness and relevance depend on the external APIs.

## Future Enhancements

- Integrate Gemini or another LLM for intelligent classification.
- Add PostgreSQL database support.
- Expand data collection using additional startup and job APIs.
- Improve data validation and deduplication.
- Implement automated scheduled execution.
- Add a dashboard for data visualization and analytics.
- Introduce comprehensive automated testing.

## Author

Developed as an AI Engineering project focused on automated data collection, processing, classification, and reporting.

---

**Project:** AI Intelligence Data Pipeline
