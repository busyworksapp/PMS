# This script runs the Barron Production Management System Frontend
# Execute from: app\frontend directory

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Barron Production Management System - Frontend Server" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
Write-Host "Starting HTTP Server for Frontend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "Frontend running on: http://localhost:3000" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Main Login: http://localhost:3000/templates/login.html" -ForegroundColor Green
Write-Host "👷 Operator Login: http://localhost:3000/templates/operator-login.html" -ForegroundColor Green
Write-Host "📊 Dashboard: http://localhost:3000/templates/dashboard.html" -ForegroundColor Green
Write-Host ""
Write-Host "Make sure the backend is running on http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m http.server 3000
