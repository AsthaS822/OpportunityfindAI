@echo off
echo Starting OpportunityOS AI...
echo.

if not exist "node_modules" (
  echo Installing dependencies...
  npm install
  echo.
)

echo Launching dev server at http://localhost:5173
echo Press Ctrl+C to stop.
echo.
npm run dev
