from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DELIVERY_TOKEN = os.getenv("DELIVERY_TOKEN")
if DELIVERY_TOKEN is None:
    raise RuntimeError("DELIVERY_TOKEN is not set")
