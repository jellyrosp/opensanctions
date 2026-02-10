import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from opensanctions.const import statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list, statement_subset_csv_path




def csv_total_individual():
    """
    Calculate the total number of unique individuals (canonical_ids) in the statements CSV dataset,
    where schema is 'Person'.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Prints the total count of unique individuals.
    """
    unique_ids = set()
    chunk_size = 50000

    # Read the CSV file in chunks
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={'canonical_id': str, 'schema': str}):
        # Filter rows where schema is 'Person'
        person_chunk = chunk[chunk['schema'] == 'Person']

        # Add unique canonical_ids to the set
        unique_ids.update(person_chunk['canonical_id'].dropna().unique())

    # Display the result
    print(f"Total number of unique individuals (schema == 'Person'): {len(unique_ids)}")









def csv_total_sanctioned_individual():
    """
    Calculate the total number of unique sanctioned individuals (canonical_ids) in the CSV dataset
    where schema is 'Person' and topics include 'sanction' or 'sanction.counter'.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Displays the total count of unique sanctioned individuals and their relative frequency.
    """
    unique_ids = set()
    chunk_size = 50000

    # Read the CSV file in chunks
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        # Filter rows where schema is 'Person'
        person_chunk = chunk[chunk['schema'] == 'Person']

        # Filter rows where prop is 'topics' and value is either 'sanction' or 'sanction.counter'
        sanctioned_chunk = person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'].isin(['sanction', 'sanction.counter']))
        ]

        # Add unique canonical_ids to the set
        unique_ids.update(sanctioned_chunk['canonical_id'].dropna().unique())

    # Display the result
    print(f"Total number of unique sanctioned individuals: {len(unique_ids)}")
    relative_frequency = (len(unique_ids) / 1130872) * 100
    print(f"Relative frequency: {relative_frequency:.2f}%")





def csv_total_sanction_counter_and_not_sanction_individual():
    """
    Calculate the total number of unique individuals (canonical_ids) in the CSV dataset
    where schema is 'Person', prop is 'topics', and value is 'sanction.counter',
    but not 'sanction'.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Displays the total count of unique individuals.
    """
    sanction_counter_ids = set()
    sanction_ids = set()
    chunk_size = 50000

    # First pass to collect all sanction_ids
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanction_ids.update(person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'] == 'sanction')
        ]['canonical_id'].dropna().unique())

    # Second pass to collect sanction_counter_ids that are not in sanction_ids
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanction_counter_chunk = person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'] == 'sanction.counter') &
            (~person_chunk['canonical_id'].isin(sanction_ids))
        ]
        sanction_counter_ids.update(sanction_counter_chunk['canonical_id'].dropna().unique())

    # Display the result
    print(f"Total number of unique sanction counter (and not sanction) individuals: {len(sanction_counter_ids)}")






def csv_total_non_sanctioned_individual():
    """
    Calculate the total number of unique individuals (canonical_ids) in the CSV dataset
    where schema is 'Person' and neither 'sanction' nor 'sanction.counter' appears as a topic value.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Displays the total count of unique individuals.
    """
    sanctioned_ids = set()
    non_sanctioned_ids = set()
    chunk_size = 50000

    # First pass to collect all sanctioned_ids (with 'sanction' or 'sanction.counter')
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanctioned_ids.update(person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'].isin(['sanction', 'sanction.counter']))
        ]['canonical_id'].dropna().unique())

    # Second pass to collect all canonical_ids where schema is 'Person'
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        non_sanctioned_ids.update(person_chunk['canonical_id'].dropna().unique())

    # Subtract sanctioned_ids from non_sanctioned_ids
    non_sanctioned_ids.difference_update(sanctioned_ids)

    # Display the result
    print(f"Total number of unique non-sanctioned individuals: {len(non_sanctioned_ids)}")




def csv_total_sanctioned_individual_with_gender():
    """
    Calculate the total number of unique sanctioned individuals (canonical_ids) in the CSV dataset
    where schema is 'Person', topics include 'sanction' or 'sanction.counter', and gender is provided.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Displays the total count of unique sanctioned individuals with gender and their relative frequency.
    """
    unique_ids = set()
    chunk_size = 50000

    # Read the CSV file in chunks
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        # Filter rows where schema is 'Person'
        person_chunk = chunk[chunk['schema'] == 'Person']

        # Get canonical_ids with sanction or sanction.counter
        sanctioned_chunk = person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'].isin(['sanction', 'sanction.counter']))
        ]
        sanctioned_ids = set(sanctioned_chunk['canonical_id'].dropna().unique())

        # Get canonical_ids with gender provided
        gender_chunk = person_chunk[
            (person_chunk['prop'] == 'gender') &
            (person_chunk['value'].notna()) &
            (person_chunk['value'] != '')
        ]
        gender_ids = set(gender_chunk['canonical_id'].dropna().unique())

        # Find intersection of sanctioned_ids and gender_ids
        unique_ids.update(sanctioned_ids.intersection(gender_ids))

    # Display the result
    print(f"Total number of unique sanctioned individuals with gender: {len(unique_ids)}")
    relative_frequency = (len(unique_ids) / 40900) * 100
    print(f"Relative frequency: {relative_frequency:.2f}%")    





def csv_total_sanction_counter_and_not_sanction_individual_with_gender():
    """
    Calculate the total number of unique individuals (canonical_ids) in the CSV dataset
    where schema is 'Person', prop is 'topics', and value is 'sanction.counter',
    but not 'sanction', and gender is provided.

    Parameters
    ----------
    statement_full_csv_path : str
        The file path to the statements CSV dataset.

    Returns
    -------
    None
        Displays the total count of unique individuals.
    """
    sanction_counter_ids = set()
    sanction_ids = set()
    gender_ids = set()
    chunk_size = 50000

    # First pass to collect all sanction_ids
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanction_ids.update(person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'] == 'sanction')
        ]['canonical_id'].dropna().unique())

        # Collect canonical_ids with non-empty gender
        gender_chunk = person_chunk[
            (person_chunk['prop'] == 'gender') &
            (person_chunk['value'].notna()) &
            (person_chunk['value'] != '')
        ]
        gender_ids.update(gender_chunk['canonical_id'].dropna().unique())

    # Second pass to collect sanction_counter_ids that are not in sanction_ids and have gender
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanction_counter_chunk = person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'] == 'sanction.counter') &
            (~person_chunk['canonical_id'].isin(sanction_ids))
        ]
        sanction_counter_ids.update(sanction_counter_chunk['canonical_id'].dropna().unique())

    # Intersection with gender_ids to ensure gender is provided
    sanction_counter_ids_with_gender = sanction_counter_ids.intersection(gender_ids)

    # Display the result
    print(f"Total number of unique sanction counter (and not sanction) individuals with gender: {len(sanction_counter_ids_with_gender)}")
    print(f"Relative frequency: {(len(sanction_counter_ids_with_gender) / 9694) * 100:.2f}%")

























def csv_gender_source_frequency():
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

    # Calculate relative frequency and round to 2 decimal places
    frequency_table['relative_frequency(%)'] = round((frequency_table['count'] / 11485) * 100, 2)

    # Bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_table['dataset_category'], frequency_table['count'], color=['green', 'red'])
    plt.title('Frequency of Valid and Non-Valid Datasets')
    plt.xlabel('Dataset Category')
    plt.ylabel('Count')
    plt.show()

    display(frequency_table.set_index(frequency_table.columns[0]))   




def csv_total_sanction_individual():
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
        # Filter rows where schema is 'Person' and topic is 'sanction'
        person_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'topics') & (chunk['value'] == 'sanction')]

        # Add unique canonical_ids to the set
        unique_ids.update(person_chunk['canonical_id'].dropna().unique())

    # Display the result
    print(f"Total number of unique individuals (schema == 'Person', topic == 'sanction'): {len(unique_ids)}")











