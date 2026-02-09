import pandas as pd
import matplotlib.pyplot as plt
from opensanctions.const import statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list



def gender_source_frequency():
    """
    Analyze the frequency of gender sources in the statements dataset,
    filtered for rows where 'prop' is 'gender' and 'topics' is 'sanction'.

    Parameters
    ----------
    input_file : str
        Path to the statements CSV file.

    Returns
    -------
    pd.DataFrame
        Frequency table of valid and non-valid datasets.
    """
    # Define the chunk size (optimized for 16GB RAM)
    chunk_size = 50000

    # List to store merged and deduplicated chunks
    merged_chunks = []

    # Iterate over the CSV in chunks to find canonical_ids with gender and sanction topics
    for chunk in pd.read_csv(
        statement_full_csv_path,
        chunksize=chunk_size,
        dtype=statement_schema_data_types,
        parse_dates=['first_seen', 'last_seen']
    ):
        gender_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'gender')]
        topics_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'topics') & (chunk['value'] == 'sanction')]

        # Merge the two DataFrames on 'canonical_id' using inner join
        merged_df = pd.merge(
            gender_chunk,
            topics_chunk,
            on='canonical_id',
            how='inner'
        )

        # Drop duplicate 'canonical_id' values, keeping only the first occurrence
        final_df = merged_df.drop_duplicates(subset=['canonical_id'])

        # Append to the list if not empty
        if not final_df.empty:
            merged_chunks.append(final_df)

    # Concatenate all merged and deduplicated chunks
    if not merged_chunks:
        print("No matching rows found.")
        return pd.DataFrame(columns=['canonical_id'])

    result = pd.concat(merged_chunks, ignore_index=True)
    canonical_ids = result['canonical_id'].unique()

    # List to store gender rows with the canonical_ids
    gender_rows = []

    # Iterate over the CSV in chunks to get gender rows for the canonical_ids
    for chunk in pd.read_csv(
        statement_full_csv_path,
        chunksize=chunk_size,
        dtype=statement_schema_data_types,
        parse_dates=['first_seen', 'last_seen']
    ):
        gender_rows_chunk = chunk[
            (chunk['schema'] == 'Person') &
            (chunk['prop'] == 'gender') &
            (chunk['canonical_id'].isin(canonical_ids))
        ]
        if not gender_rows_chunk.empty:
            gender_rows.append(gender_rows_chunk)

    if not gender_rows:
        print("No gender rows found for the canonical_ids.")
        return pd.DataFrame(columns=['canonical_id'])

    gender_rows_df = pd.concat(gender_rows, ignore_index=True)

    # Create a set of canonical_ids that have at least one valid dataset
    valid_canonical_ids = set()

    # Iterate over each canonical_id to check if any dataset is valid
    for canonical_id in canonical_ids:
        canonical_id_rows = gender_rows_df[gender_rows_df['canonical_id'] == canonical_id]
        datasets = canonical_id_rows['dataset'].dropna().unique()

        # Check if any dataset is in valid_dataset_values_list
        for dataset in datasets:
            if dataset in valid_dataset_values_list:
                valid_canonical_ids.add(canonical_id)
                break  # No need to check further for this canonical_id

    # Get unique canonical_ids for each category
    valid_canonical_ids_list = list(valid_canonical_ids)
    non_valid_canonical_ids_list = [id for id in canonical_ids if id not in valid_canonical_ids]

    # Frequency table based on unique canonical_ids
    frequency_data = {
        'dataset_category': ['valid_dataset', 'non_valid_dataset'],
        'count': [len(valid_canonical_ids_list), len(non_valid_canonical_ids_list)]
    }
    frequency_table = pd.DataFrame(frequency_data)

    # Bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_table['dataset_category'], frequency_table['count'], color=['green', 'red'])
    plt.title('Frequency of Valid and Non-Valid Datasets')
    plt.xlabel('Dataset Category')
    plt.ylabel('Count')
    plt.show()

    display(frequency_table.set_index(frequency_table.columns[0]))   



















