from pathlib import Path
from typing import Optional, Union
import requests

from opensanctions.config import DELIVERY_TOKEN





def download_dataset_file(
    dataset: str,
    date: str = "latest",
    output_path: Optional[Union[str, Path]] = None,
    delivery_token: Optional[str] = None,
    default_base_dir: Optional[Union[str, Path]] = "datasets",
) -> Path:
    """
    Download an OpenSanctions dataset (latest or historical).

    Parameters
    ----------
    dataset : str
        Dataset name (e.g. "sanctions")
    date : str
        "latest" or a YYYYMMDD date
    output_path : str | Path | None
        File path or directory where the file will be saved
    delivery_token : str | None
        Required for historical datasets
    default_base_dir : str | Path | None
        Base directory for relative paths

    Returns
    -------
    Path
        Path to the downloaded file
    """
    # Base URL and headers
    if date == "latest":
        base_url = "https://data.opensanctions.org"
        headers = {}
    else:
        base_url = "https://delivery.opensanctions.com"
        if not delivery_token:
            raise ValueError("delivery_token is required for historical datasets")
        headers = {"Authorization": f"Token {delivery_token}"}

    url = f"{base_url}/datasets/{date}/{dataset}/entities.ftm.json"

    # Determine output path
    if output_path is None:
        output_path = Path(default_base_dir) / date / f"{dataset}-{date}-entities.ftm.json"
    else:
        output_path = Path(output_path)
        if default_base_dir and not output_path.is_absolute():
            output_path = Path(default_base_dir) / output_path

        if output_path.suffix == "":
            output_path = output_path / f"{dataset}-{date}-entities.ftm.json"

    # Ensure parent directories exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Download the file
    print(f"Downloading from {url}...")
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with output_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output_path

dataset = "sanctions"
date = "20260201"
output_dir = Path("datasets")

path = download_dataset_file(
    dataset=dataset,
    date=date,
    output_path=output_dir / f"{dataset}-{date}-entities.ftm.json",
    delivery_token=DELIVERY_TOKEN,
)

print(f"\nDownloaded to: {path.resolve()}")


