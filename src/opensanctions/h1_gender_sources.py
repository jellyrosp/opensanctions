import pandas as pd



statement_schema_data_types = {
        'canonical_id': 'str',
        'entity_id': 'str',
        'prop': 'str',
        'prop_type': 'str',
        'schema': 'str',
        'value': 'str',
        'dataset': 'str',
        'origin': 'str',
        'lang': 'str',
        'original_value': 'str',
        'external': 'str',
        'first_seen': 'str',
        'last_seen': 'str',
        'id': 'str'
    }



def gender_source_frequency(input_file: str, output_file: str) -> pd.DataFrame:
    """
    Analyze the frequency of gender sources in the statements dataset,
    filtered for rows where 'prop' is 'gender' and 'topics' is 'sanction'.

    Parameters
    ----------
    input_file : str
        Path to the statements CSV file.
    output_file : str
        Path to save the filtered and merged results.

    Returns
    -------
    pd.DataFrame
        DataFrame with merged and deduplicated rows.
    """
    # Define the chunk size (optimized for 16GB RAM)
    chunk_size = 50000

    # Initialize counters for total rows
    total_gender_rows = 0
    total_topics_rows = 0

    # Set to store unique canonical_id values from topics_chunk
    unique_canonical_ids = set()

    # List to store merged and deduplicated chunks
    merged_chunks = []

    # Iterate over the CSV in chunks
    for chunk in pd.read_csv(
        input_file,
        chunksize=chunk_size,
        dtype=statement_schema_data_types,
        parse_dates=['first_seen', 'last_seen']  # Optional: Parse timestamps if needed
    ):
        # Filter rows where 'prop' is "gender" and 'prop' is "topics" with 'value' as "sanction"
        gender_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'gender')]
        topics_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'topics') & (chunk['value'] == 'sanction')]

        # Update total row counts
        total_gender_rows += len(gender_chunk)
        total_topics_rows += len(topics_chunk)

        # Add unique canonical_id values from topics_chunk to the set
        unique_canonical_ids.update(topics_chunk['canonical_id'].unique())

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

    # Print total unique canonical_id count in topics_chunk with value 'sanction'
    print(f"Total unique canonical_id count in topics_chunk with value 'sanction': {len(unique_canonical_ids)}")

    # Print total row counts
    print(f"Total number of rows in gender_chunk: {total_gender_rows}")
    print(f"Total number of rows in topics_chunk: {total_topics_rows}")

    # Concatenate all merged and deduplicated chunks
    if merged_chunks:
        result = pd.concat(merged_chunks, ignore_index=True)
        # Print the number of rows in the final result
        print(f"Number of rows in the final stacked DataFrame: {len(result)}")
        # Save to output file
        result.to_csv(output_file, index=False)
        print(f"Merged and deduplicated data saved to '{output_file}'")
        return result
    else:
        print("No matching rows found.")
        return pd.DataFrame(columns=['canonical_id'])

input_file = '/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/statements_2026.csv'
output_file = '/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/filtered_data.csv'

print(gender_source_frequency(input_file, output_file))




# import json

# # Path to your JSON file
# json_file_path = '/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/sanctions-20260201-persons.ftm.json'

# # Open and read the JSON file
# with open(json_file_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Count the objects
# if isinstance(data, list):
#     # If the JSON is a list of objects
#     num_objects = len(data)
#     print(f"The JSON file contains {num_objects} objects (list items).")
# elif isinstance(data, dict):
#     # If the JSON is a dictionary of objects
#     num_objects = len(data)
#     print(f"The JSON file contains {num_objects} objects (dictionary keys).")
# else:
#     print("The JSON file does not contain a list or dictionary at the top level.")
