import sys
import os
from pathlib import Path

# Add parent directory to path so we can import app
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

# Change working directory to parent so relative paths work
os.chdir(parent_dir)

from app import app

# Vercel expects the app to be exposed as 'app' or as a handler function
# This exposes the Flask app for Vercel's serverless runtime
handler = app
