import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables from opportunityos-ai/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Core Paths
DATASET_PATH = BASE_DIR / "Dataset"

# External APIs
JINA_SEARCH_URL = "https://s.jina.ai/"
JINA_READER_URL = "https://r.jina.ai/"
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Limits & Thresholds
RATE_LIMIT = "30/minute"
MAX_SEARCH_RESULTS = 10
MAX_VERIFY = 5
REQUEST_TIMEOUT = 20.0

# Cache TTLs (Seconds)
CACHE_SEARCH_TTL = 1800      # 30 mins
CACHE_GEMINI_TTL = 1800      # 30 mins
CACHE_JINA_TTL = 21600       # 6 hours

# App Information
BACKEND_VERSION = "1.0.0"
