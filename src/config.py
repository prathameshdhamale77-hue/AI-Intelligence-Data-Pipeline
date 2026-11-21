
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project settings
PROJECT_NAME = "AI Intelligence Data Pipeline"

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Google Sheets configuration
GOOGLE_SHEETS_CREDENTIALS = os.getenv(
    "GOOGLE_SHEETS_CREDENTIALS",
    "credentials.json"
)

# Data collection settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

if not GEMINI_API_KEY:
    print("WARNING: Gemini API key is not configured.")

print(f"{PROJECT_NAME} configuration loaded.")
