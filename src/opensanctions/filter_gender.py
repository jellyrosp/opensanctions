import pandas as pd

# Define the chunk size (optimized for 16GB RAM)
chunk_size = 50000

# Input and output file paths
input_file = '/home/aurora/Desktop/opensanctions/datasets/2026/statements_2026.csv'
output_file = '/home/aurora/Desktop/opensanctions/filtered_gender.csv'

# Define data types for each column (based on your schema and order)
dtype = {
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

# Open a file to save the filtered results
with open(output_file, 'w') as f_out:
    first_chunk = True  # Flag to write the header only once

    # Iterate over the CSV in chunks
    for chunk in pd.read_csv(
        input_file,
        chunksize=chunk_size,
        dtype=dtype,
        parse_dates=['first_seen', 'last_seen']  # Optional: Parse timestamps if needed
    ):
        # Filter rows where 'prop' is "gender"
        filtered_chunk = chunk[(chunk['schema'] == 'Person') & (chunk['prop'] == 'gender')]

        # Skip empty chunks
        if filtered_chunk.empty:
            continue

        # Write to the output file
        if first_chunk:
            filtered_chunk.to_csv(f_out, index=False, mode='w')
            first_chunk = False
        else:
            filtered_chunk.to_csv(f_out, index=False, mode='a', header=False)

print(f"Filtered data saved to '{output_file}'")
