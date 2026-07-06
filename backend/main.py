from pathlib import Path
from contextlib import asynccontextmanager
import time
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.config import DATASET_PATH, BACKEND_VERSION
from backend.limiter import limiter
from backend.routes import discover, health
from backend.services.dataset_loader import dataset_loader
from backend.middleware.exception_handler import global_exception_handler
from backend.utils.logger import get_logger

# --------------------------------------------------
# Load .env from project root
# OpportunityAI/
# ├── .env
# └── backend/
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

logger = get_logger(__name__)

APP_START_TIME = time.time()

# --------------------------------------------------
# Rate Limiter (shared instance)
# --------------------------------------------------
# limiter imported from backend.limiter

# --------------------------------------------------
# Startup Validation
# --------------------------------------------------

def validate_startup():

    logger.info("Running startup validation...")

    if not DATASET_PATH.exists():
        logger.error(f"Dataset folder not found:\n{DATASET_PATH}")
        sys.exit(1)

    groq = os.getenv("GROQ_API_KEY")
    jina = os.getenv("JINA_API_KEY")

    if not groq:
        logger.error("Missing GROQ_API_KEY inside .env")
        sys.exit(1)

    if not jina:
        logger.error("Missing JINA_API_KEY inside .env")
        sys.exit(1)

    logger.info("Dataset Path : %s", DATASET_PATH)
    logger.info("Groq Key     : Loaded")
    logger.info("Jina Key     : Loaded")
    logger.info("Startup validation completed successfully.")

# --------------------------------------------------
# Lifespan
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    validate_startup()

    logger.info("Loading datasets...")

    dataset_loader.load_all()
    
    # Initialize dataset analyzer
    logger.info("Initializing dataset analyzer...")
    try:
        from backend.services.dataset_analyzer import dataset_analyzer
        dataset_analyzer.analyze_and_index()
        logger.info("Dataset analyzer ready")
    except Exception as e:
        logger.error(f"Failed to initialize dataset analyzer: {e}")

    app.state.start_time = APP_START_TIME

    logger.info("Backend Ready.")

    yield

    logger.info("Backend shutting down...")

# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="FutureOS Backend",
    description="AI Decision Intelligence Platform",
    version=BACKEND_VERSION,
    lifespan=lifespan,
)

# --------------------------------------------------
# Rate Limit
# --------------------------------------------------

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------

app.add_exception_handler(
    Exception,
    global_exception_handler,
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # change to frontend URL when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(health.router)
app.include_router(discover.router)

# --------------------------------------------------
# Local Run
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )