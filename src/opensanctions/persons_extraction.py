import json
from pathlib import Path
from opensanctions.const import input_map

from opensanctions.config import PROJECT_ROOT






def persons_extract(json_path: Path, exact_date: str) -> Path:
    """
    Extract Person entities from an OpenSanctions dataset and save to JSON-LD.

    Parameters
    ----------
    json_path : Path
        Path to entities.ftm.json
    exact_date : str
        Date of the dataset (YYYYMMDD)

    Returns
    -------
    Path
        Path to the output JSON-LD file
    """
    output_list = []
    year = exact_date[:4]

    with json_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("schema") == "Person":
                output_list.append(obj)

    # Prepare output path
    output_dir = PROJECT_ROOT / "datasets" / year
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"sanctions-{exact_date}-persons.ftm.json"
    with output_file.open("w", encoding="utf-8") as f_out:
        json.dump(output_list, f_out, ensure_ascii=False, indent=2)

    return output_file



for json_input, exact_date in input_map.items():
    json_path = PROJECT_ROOT / json_input

    output_file = persons_extract(
        json_path=json_path,
        exact_date=exact_date,
    )

    print(f"\nExtracted persons to: {output_file.resolve()}")
