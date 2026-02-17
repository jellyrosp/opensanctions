import pandas as pd
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt
from IPython.display import display
from opensanctions.const import STATEMENTS_2026_PATH, statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list, statement_subset_csv_path, persons_sub_db_path




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




def filter_persons_by_props_and_values_csv(output_csv_path, conditions):
    """
    Filter a large CSV dataset to create a sub-CSV containing only rows associated with individuals
    who meet the specified logical conditions on their prop and value pairs.

    Parameters:
    - output_csv_path: str, path to save the filtered CSV
    - conditions: list of dicts, each dict specifies a prop, optional value(s), and whether it should be included or excluded.
      Example: [{'prop': 'gender', 'required': True},
                {'prop': 'topics', 'values': ['sanction', 'sanction.counter'], 'required': True}]
      This means: include individuals who have both 'gender' and 'topics' with values 'sanction' or 'sanction.counter'.
    """
    unique_ids = set()
    prop_sets = {i: set() for i in range(len(conditions))}
    chunk_size = 50000
    output_rows = []

    # First pass to collect unique_ids based on conditions
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']

        for i, condition in enumerate(conditions):
            prop = condition['prop']
            required = condition['required']
            values = condition.get('values', None)

            prop_chunk = person_chunk[person_chunk['prop'] == prop]
            if values is not None:
                prop_chunk = prop_chunk[prop_chunk['value'].isin(values)]

            prop_sets[i].update(prop_chunk['canonical_id'].dropna().unique())

    # Determine which canonical_ids meet all conditions
    if conditions:
        if conditions[0]['required']:
            unique_ids = prop_sets[0].copy()
        else:
            unique_ids = set().union(*[s for s in prop_sets.values() if s]) - prop_sets[0]

        for i, condition in enumerate(conditions[1:], start=1):
            if condition['required']:
                unique_ids.intersection_update(prop_sets[i])
            else:
                unique_ids -= prop_sets[i]

    print(f"Total number of unique individuals meeting the conditions: {len(unique_ids)}")

    # Calculate relative frequency if needed (assuming total individuals is 1130872)
    relative_frequency = (len(unique_ids) / 1130872) * 100
    print(f"Relative frequency: {relative_frequency:.2f}%")

    # Second pass to collect all rows associated with unique_ids
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        associated_rows = chunk[chunk['canonical_id'].isin(unique_ids)]
        output_rows.append(associated_rows)

    if output_rows:
        output_df = pd.concat(output_rows, ignore_index=True)
        output_df.to_csv(output_csv_path, index=False)
        print(f"Saved all associated rows to {output_csv_path}")
    else:
        print("No associated rows found.")




# filter_persons_by_props_and_values_csv(
#     output_csv_path='/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/persons_topic_sub_statements.csv',
#     conditions=[
#         {'prop': 'gender', 'required': True},
#         {'prop': 'topics', 'required': True}
#     ]
# )



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
    Calculate the total number of unique sanctioned individuals (canonical_ids) in the SQLite database
    where topics include 'sanction' or 'sanction.counter', and gender is provided.

    Returns
    -------
    None
        Displays the total count of unique sanctioned individuals with gender and their relative frequency.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    # SQL query to count unique sanctioned individuals with gender
    sql_query = """
    WITH
    -- Individuals with 'sanction' or 'sanction.counter' in 'topics'
    has_sanction_topics AS (
        SELECT DISTINCT canonical_id
        FROM persons
        WHERE prop = 'topics' AND (value = 'sanction' OR value = 'sanction.counter')
    ),

    -- Individuals with 'gender' property
    has_gender AS (
        SELECT DISTINCT canonical_id
        FROM persons
        WHERE prop = 'gender'
    )

    -- Count individuals who have both 'sanction'/'sanction.counter' in 'topics' and 'gender'
    SELECT COUNT(DISTINCT hst.canonical_id)
    FROM has_sanction_topics hst
    INNER JOIN has_gender hg ON hst.canonical_id = hg.canonical_id;
    """

    # Execute the query
    cursor.execute(sql_query)
    total_individuals = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    # Display the result
    print(f"Total number of unique sanctioned individuals with gender: {total_individuals}")
    relative_frequency = (total_individuals / 40900) * 100
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
    for chunk in pd.read_csv(STATEMENTS_2026_PATH, chunksize=chunk_size, dtype={
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



def count_gender_categories_for_sanctioned_individuals():
    """
    Count the total number of sanctioned individuals per gender category.
    Individuals with multiple gender values are categorized as 'mixed'.
    Also plots a bar chart and displays a frequency table.

    Parameters
    ----------
    csv_path : str
        The file path to the CSV dataset.
    total_individuals : int
        Total number of sanctioned individuals for percentage calculation.

    Returns
    -------
    pd.DataFrame
        A frequency table with gender categories, counts, and percentages.
    """
    # Read the CSV file
    df = pd.read_csv(statement_subset_csv_path, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    })

    # Filter for sanctioned individuals
    sanctioned_df = df[
        (df['prop'] == 'topics') &
        (df['value'].isin(['sanction', 'sanction.counter']))
    ]
    sanctioned_ids = set(sanctioned_df['canonical_id'].dropna().unique())

    # Filter for gender information of sanctioned individuals
    gender_df = df[
        (df['prop'] == 'gender') &
        (df['value'].isin(['male', 'female', 'other'])) &
        (df['canonical_id'].isin(sanctioned_ids))
    ]

    # Map canonical_id to set of gender values
    gender_map = defaultdict(set)
    for _, row in gender_df.iterrows():
        canonical_id = row['canonical_id']
        gender = row['value'].lower().strip()
        gender_map[canonical_id].add(gender)

    # Categorize individuals
    gender_categories = defaultdict(int)
    for canonical_id, genders in gender_map.items():
        if len(genders) > 1:
            gender_categories['mixed'] += 1
        else:
            gender = next(iter(genders))
            gender_categories[gender] += 1

    # Create a DataFrame for the frequency table
    frequency_table = pd.DataFrame({
        'gender_category': list(gender_categories.keys()),
        'count': list(gender_categories.values())
    })

    # Calculate relative frequency and round to 2 decimal places
    frequency_table['relative_frequency(%)'] = round(
        (frequency_table['count'] / 12046) * 100, 2
    )

    # Bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_table['gender_category'], frequency_table['count'],
            color=['blue', 'pink', 'green', 'orange'])
    plt.title('Gender Distribution Among Sanctioned Individuals')
    plt.xlabel('Gender Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

    # Display the frequency table
    display(frequency_table.set_index('gender_category'))




def csv_dataset_frequency_for_sanctioned_gender():
    # Connect to the SQLite database
    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    # Create placeholders for the IN clause (e.g., ?, ?, ?)
    placeholders = ', '.join(['?'] * len(valid_dataset_values_list))

    # SQL query to count unique sanctioned individuals with gender
    query = f"""
    SELECT dataset,
    COUNT(*) AS occurrence_count
    FROM persons
    WHERE dataset IN ({placeholders})
    AND prop = 'gender'
    GROUP BY dataset
    ORDER BY occurrence_count DESC;
    """
    # Execute the query with the list of values
    cursor.execute(query, valid_dataset_values_list)

    # Fetch the results
    results = cursor.fetchall()
    conn.close()

    # Convert results to a pandas DataFrame
    frequency_table = pd.DataFrame(results, columns=['dataset_category', 'count'])

    # Calculate relative frequency and round to 2 decimal places
    frequency_table['relative_frequency(%)'] = round((frequency_table['count'] / 45241) * 100, 2)

    # Bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(frequency_table['dataset_category'], frequency_table['count'], color='skyblue')
    plt.title('Frequency of Individual Valid Datasets (Gender)')
    plt.xlabel('Dataset Category')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    # Display frequency table
    display(frequency_table.set_index('dataset_category'))









