from pathlib import Path
from typing import Optional, Union

import requests


def download_dataset_file(
    dataset: str,
    date: str = "latest",
    output_path: Optional[Union[str, Path]] = None,
    delivery_token: Optional[str] = None,
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

    Returns
    -------
    Path
        Path to the downloaded file
    """

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
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / f"{dataset}-{date}-entities.ftm.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with output_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output_path
