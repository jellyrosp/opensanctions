import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from opensanctions.const import input_map, statement_full_csv_path, statement_subset_csv_path
from opensanctions.config import PROJECT_ROOT
import json

def jsn_total_individual_per_year():
    """
    Calculate the total number of unique individuals (ids) in the dataset for each year,
    plot a bar chart, and display a table of the exact values for each year.

    Returns
    -------
    None
        Displays a bar plot and a table of the total count of unique individuals for each year.
    """
    results = []

    for json_input, exact_date in input_map.items():
        json_path = PROJECT_ROOT / json_input

        with json_path.open("r", encoding="utf-8") as f:
            ids = set()
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("schema") == "Person":
                    canonical_id = obj.get("id")
                    if canonical_id:
                        ids.add(canonical_id)

        year = exact_date[:4]
        results.append({'year': year, 'unique_individuals': len(ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['unique_individuals'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Unique Individuals')
    plt.title('Total Number of Unique Individuals per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index(df.columns[0]))




def csv_total_individual():
    """
    Calculate the total number of unique individuals (canonical_ids) in the statements CSV dataset,
    where schema is 'Person', using chunk processing for large files.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.
    chunk_size : int, optional
        The number of rows to process at a time (default is 50000).

    Returns
    -------
    None
        Prints the total count of unique individuals.
    """
    unique_ids = set()

    chunk_size=50000

    # Read the CSV file in chunks
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={'canonical_id': str}):
        # Filter rows where schema is 'Person'
        person_chunk = chunk[chunk['schema'] == 'Person']

        # Add unique canonical_ids to the set
        unique_ids.update(person_chunk['canonical_id'].dropna().unique())

    # Display the result
    print(f"Total number of unique individuals (schema == 'Person'): {len(unique_ids)}")

# Example usage
csv_total_individual()


