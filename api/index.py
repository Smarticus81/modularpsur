import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Vercel expects the app to be exposed for serverless functions
# The app variable will be used by Vercel to handle requests
