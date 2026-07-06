$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "C:\Users\Admin\Desktop\OpportunityAI\opportunityos-ai\venv\Scripts\python.exe"
$pinfo.Arguments = "-m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
$pinfo.WorkingDirectory = "C:\Users\Admin\Desktop\OpportunityAI\opportunityos-ai"
$pinfo.UseShellExecute = $false
[System.Diagnostics.Process]::Start($pinfo)
Write-Host "Backend started"
