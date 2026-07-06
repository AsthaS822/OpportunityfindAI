# OpportunityOS AI Backend

This is the production-ready FastAPI backend for OpportunityOS AI. It integrates a rule-based fuzzy search engine over local datasets and pairs it with real-time verification using the Jina Search and Reader APIs. Final analysis, summaries, and application roadmaps are generated using Google Gemini.

## Architecture Highlights
- **No Database Needed**: Datasets in `../Dataset/` are loaded into memory on startup.
- **Strict Verification**: AI does not hallucinate deadlines or active status. Opportunities are live-verified using Jina, and differences in ranking or deadlines are explicitly surfaced.
- **Language Support**: Seamlessly translates explanations into Hindi (if requested) without translating official names.
- **Highly Modular**: Each step of the query pipeline is isolated in its own service (Parser -> Search -> Deduplicate -> Live Verify -> Gemini Analysis).

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Environment Variables:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   JINA_API_KEY=your_jina_api_key
   ```

## Running the Server

Start the FastAPI application via uvicorn:
```bash
uvicorn main:app --reload
```
The server will start at `http://127.0.0.0:8000`. On startup, it will recursively scan `../Dataset/` and load all `.csv`, `.json`, and `.xlsx` files into memory.

## Connecting the React Frontend

The React frontend should point its API calls to `http://localhost:8000/discover`.

Example payload to fetch opportunities in Hindi:
```javascript
const fetchOpportunities = async (userQuery, language = 'en') => {
  try {
    const response = await fetch('http://localhost:8000/discover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userQuery, language: language })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching opportunities:", error);
  }
};
```

The React UI should expect the response to match the `DiscoverResponse` schema (refer to `schemas/response.py`).

## Features
- **Rate Limiting**: 30 requests per minute per IP via `slowapi`.
- **Concurrency**: Jina queries run concurrently using `asyncio.gather`.
- **Fault Tolerance**: If Gemini APIs fail or hit a quota, the system falls back gracefully to returning raw Jina-verified dataset results.
