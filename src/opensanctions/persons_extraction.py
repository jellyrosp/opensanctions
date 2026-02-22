import json
import sqlite3
import pandas as pd
from pathlib import Path
from opensanctions.const import input_map_raw
from opensanctions.const import statement_csv_db_path
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



# for json_input, exact_date in input_map_raw.items():
#     json_path = PROJECT_ROOT / json_input

#     output_file = persons_extract(
#         json_path=json_path,
#         exact_date=exact_date,
#     )

#     print(f"\nExtracted persons to: {output_file.resolve()}")





def get_sanctioned_persons_csv(output_csv):
    """
    Extract sanctioned persons with gender and sanction reasons to CSV.
    Columns: person_id, gender, sanction_reason
    """
    
    query = """
    SELECT DISTINCT
        p.canonical_id AS person_id,
        pg.value AS gender,
        s2.value AS sanction_reason
    FROM statements_csv p
    -- Person has sanction topics
    INNER JOIN statements_csv pt ON p.canonical_id = pt.canonical_id
        AND pt.schema = 'Person' AND pt.prop = 'topics'
        AND (pt.value = 'sanction' OR pt.value = 'sanction.counter')
    -- Person has gender male/female
    INNER JOIN statements_csv pg ON p.canonical_id = pg.canonical_id
        AND pg.schema = 'Person' AND pg.prop = 'gender'
        AND (pg.value = 'male' OR pg.value = 'female')
    -- Person referenced by Sanction (via value field)
    INNER JOIN statements_csv s ON s.schema = 'Sanction'
        AND s.prop_type = 'entity'
        AND s.value = p.canonical_id
    -- Sanction has reason property
    INNER JOIN statements_csv s2 ON s.canonical_id = s2.canonical_id
        AND s2.schema = 'Sanction' AND s2.prop = 'reason'
    """
    
    # Connect to database and execute query
    conn = sqlite3.connect(statement_csv_db_path)
    
    try:
        # Load results into pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Save to CSV
        df.to_csv(output_csv, index=False)
        
        # Count UNIQUE canonical_ids
        unique_persons = df['person_id'].nunique()
        
        print(f"Exported {len(df)} rows to {output_csv}")
        print(f"Unique canonical_ids: {unique_persons}")
        print("\nFirst 100 rows:")
        print(df.head(100))
        
        return df
        
    finally:
        conn.close()
        



get_sanctioned_persons_csv(output_csv='/home/aurora/Desktop/opensanctions/datasets/2026/statement_reasons.csv')        