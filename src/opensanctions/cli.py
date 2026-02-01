#!/usr/bin/env python3
import sys
from pathlib import Path

from opensanctions.download import download_dataset_file
from opensanctions.config import DELIVERY_TOKEN

# project root = directory containing pyproject.toml
PROJECT_ROOT = next(
    p for p in Path(__file__).resolve().parents
    if (p / "pyproject.toml").exists()
)

FUNCTIONS = {
    "download_dataset": download_dataset_file,
}

def list_functions() -> None:
    for name in FUNCTIONS:
        print(name)

def main():
    # ---- bash completion hook (MUST be first) ----
    if len(sys.argv) == 2 and sys.argv[1] == "list_functions":
        list_functions()
        return

    if len(sys.argv) < 2:
        print("Usage: opensanctions FUNCTION")
        print("Available functions:", ", ".join(FUNCTIONS))
        sys.exit(1)

    func_name = sys.argv[1]

    if func_name not in FUNCTIONS:
        print(f"Unknown function: {func_name}")
        print("Available functions:", ", ".join(FUNCTIONS))
        sys.exit(1)

    if func_name == "download_dataset":
        dataset = input("\n--dataset name (e.g. sanctions): ").strip()
        if not dataset:
            raise ValueError("ALERT: Dataset name is required")

        date = input("--date (YYYYMMDD or 'latest') [latest]: ").strip() or "latest"

        out = input("--output directory [datasets/]: ").strip()
        if out:
            output_dir = PROJECT_ROOT / "datasets" / out
        else:
            output_dir = PROJECT_ROOT / "datasets" / date

        path = download_dataset_file(
            dataset=dataset,
            date=date,
            output_path=output_dir / f"{dataset}-{date}-entities.ftm.json",
            delivery_token=DELIVERY_TOKEN,
        )

        print(f"\nDownloaded to: {path.resolve()}")

if __name__ == "__main__":
    main()
