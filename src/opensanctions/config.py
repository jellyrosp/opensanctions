from pathlib import Path
import os

from dotenv import load_dotenv

# Resolve project root: src/opensanctions/config.py → project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load .env explicitly
load_dotenv(PROJECT_ROOT / ".env")

# Required configuration
DELIVERY_TOKEN = os.getenv("DELIVERY_TOKEN")

if DELIVERY_TOKEN is None:
    raise RuntimeError("DELIVERY_TOKEN is not set in .env")
