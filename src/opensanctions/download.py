from pathlib import Path
from typing import Optional, Union
import requests


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

    # ---- base URL and headers ----
    if date == "latest":
        base_url = "https://data.opensanctions.org"
        headers = {}
    else:
        base_url = "https://delivery.opensanctions.com"
        if not delivery_token:
            raise ValueError("delivery_token is required for historical datasets")
        headers = {"Authorization": f"Token {delivery_token}"}

    url = f"{base_url}/datasets/{date}/{dataset}/entities.ftm.json"

    # ---- determine output path ----
    if output_path is None:
        # default: datasets/YYYY/dataset-date-entities.ftm.json
        output_path = Path(default_base_dir) / date / f"{dataset}-{date}-entities.ftm.json"
    else:
        output_path = Path(output_path)
        # prepend default_base_dir only if provided
        if default_base_dir:
            output_path = Path(default_base_dir) / output_path if not output_path.is_absolute() else output_path

        # if output_path is a directory, append the filename
        if output_path.suffix == "":
            output_path = output_path / f"{dataset}-{date}-entities.ftm.json"

    # ensure parent directories exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ---- download ----
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with output_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output_path
