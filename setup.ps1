PowerShell.exe -NoProfile -ExecutionPolicy Bypass -Command "
# Create and activate virtual environment
python -m venv social
.\social\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
$directories = @(
    'static\images\generated',
    'src\content_creation\config',
    'src\content_creation\utils',
    'src\content_creation\routers',
    'src\content_creation\middleware',
    'templates'
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
}

# Setup frontend
cd frontend
npm install
cd ..

Write-Host 'Project setup complete!'
"
