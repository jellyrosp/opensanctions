import requests
from pathlib import Path
from typing import Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env from current working directory
DELIVERY_TOKEN = os.getenv("DELIVERY_TOKEN")




def download_dataset_file(
    dataset: str,
    date: str = "latest",
    output_path: Optional[Union[str, Path]] = None,
    delivery_token: Optional[str] = None,
) -> Path:

    if date == "latest":
        base_url = "https://data.opensanctions.org"
        headers = {}
    else:
        base_url = "https://delivery.opensanctions.com"
        if not delivery_token:
            raise ValueError("delivery_token is required for historical datasets")
        headers = {"Authorization": f"Token {delivery_token}"}

    url = f"{base_url}/datasets/{date}/{dataset}/entities.ftm.json"

    if output_path is None:
        output_path = Path(f"{dataset}-{date}-entities.ftm.json")
    else:
        output_path = Path(output_path)

        # 👇 THIS is the missing logic
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / f"{dataset}-{date}-entities.ftm.json"

    # Ensure parent directories exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, headers=headers, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with output_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output_path




path = download_dataset_file(
    dataset="sanctions",
    date="20211231",
    delivery_token=DELIVERY_TOKEN,
    output_path="datasets/2021"
)

print(f"Downloaded to: {path.resolve()}")
