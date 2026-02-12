import pandas as pd
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt
from IPython.display import display
from opensanctions.const import statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list, statement_subset_csv_path, persons_sub_db_path




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




def persons_sub_statement_csv(output_csv_path):
    unique_ids = set()
    chunk_size = 50000
    output_rows = []

    # First pass to collect unique_ids
    for chunk in pd.read_csv(statement_full_csv_path, chunksize=chunk_size, dtype={
        'canonical_id': str,
        'prop': str,
        'value': str,
        'schema': str
    }):
        person_chunk = chunk[chunk['schema'] == 'Person']
        sanctioned_chunk = person_chunk[
            (person_chunk['prop'] == 'topics') &
            (person_chunk['value'].isin(['sanction', 'sanction.counter']))
        ]
        unique_ids.update(sanctioned_chunk['canonical_id'].dropna().unique())

    print(f"Total number of unique sanctioned individuals: {len(unique_ids)}")
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

    
#persons_sub_statement_csv("/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/persons_sub_statements.csv")




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








# This function measures the frequency of valid datasets providing gender information.


import pandas as pd
from collections import defaultdict

def csv_dataset_frequency_for_sanctioned_gender(persons_sub_statements_csv_path, valid_dataset_values_list, statement_schema_data_types):
    """
    Count the frequency of datasets that provide gender information for sanctioned individuals.
    This version counts unique sanctioned individuals per dataset.

    Parameters
    ----------
    persons_sub_statements_csv_path : str
        Path to the statements CSV file.
    valid_dataset_values_list : list
        List of valid dataset values.
    statement_schema_data_types : dict
        Data types for the CSV schema.

    Returns
    -------
    pd.DataFrame
        Frequency table of datasets.
    """
    chunk_size = 50000
    dataset_unique_individuals = defaultdict(set)

    # Step 1: Collect all sanctioned canonical_ids
    sanctioned_ids = set()

    for chunk in pd.read_csv(
        persons_sub_statements_csv_path,
        chunksize=chunk_size,
        dtype=statement_schema_data_types,
        parse_dates=['first_seen', 'last_seen']
    ):
        topics_chunk = chunk[
            (chunk['schema'] == 'Person') &
            (chunk['prop'] == 'topics') &
            (chunk['value'].isin(['sanction', 'sanction.counter']))
        ]
        sanctioned_ids.update(topics_chunk['canonical_id'].dropna().unique())

    # Step 2: For each valid dataset, track unique sanctioned individuals it provides gender for
    for chunk in pd.read_csv(
        persons_sub_statements_csv_path,
        chunksize=chunk_size,
        dtype=statement_schema_data_types,
        parse_dates=['first_seen', 'last_seen']
    ):
        gender_chunk = chunk[
            (chunk['schema'] == 'Person') &
            (chunk['prop'] == 'gender') &
            (chunk['canonical_id'].isin(sanctioned_ids)) &
            (chunk['dataset'].isin(valid_dataset_values_list))
        ]

        for _, row in gender_chunk.iterrows():
            dataset = row['dataset']
            canonical_id = row['canonical_id']
            if dataset in valid_dataset_values_list:
                dataset_unique_individuals[dataset].add(canonical_id)

    # Convert to DataFrame
    frequency_table = pd.DataFrame(
        [(dataset, len(unique_ids)) for dataset, unique_ids in dataset_unique_individuals.items()],
        columns=['dataset', 'count']
    ).sort_values(by='count', ascending=False)

    # Calculate relative frequency
    frequency_table['relative_frequency(%)'] = round((frequency_table['count'] / 8666) * 100, 2)

    return frequency_table

# Example usage:
persons_sub_statements_csv_path = '/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/persons_sub_statements.csv'
valid_dataset_values_list = [
    'ar_repet', 'au_listed_terrorist_orgs', 'AU-TERROR', 'au_dfat_sanctions', 'AU-AFGHANISTAN', 'AU-UNSC1373',
    'AU-DPRK', 'AU-YUGO', 'AU-IRAN', 'AU-LIBYA', 'AU-MYANMAR', 'AU-RUSSIA', 'AU-VESSELS', 'AU-CRP',
    'AU-HUMAN', 'AU-CYB', 'AU-SYRIA', 'AU-UKRAINE', 'AU-ZIM', 'at_nbter_sanctions', 'az_fiu_sanctions',
    'be_fod_sanctions', 'BE-FOD-NAT', 'bg_omnio_poi', 'ca_dfatd_sema_sanctions', 'CA-SEMA',
    'ca_facfoa', 'CA-FACFOA-TUN', 'CA-FACFOA-UKR', 'ca_listed_terrorists', 'CA-UNSC1373',
    'ca_named_research_orgs', 'CA-NRO', 'cn_sanctions', 'CN-AFSL', 'CN-CML', 'CN-UEL', 'cz_terrorists',
    'CZ-TERR', 'cz_national_sanctions', 'CZ-A1-2023COLL', 'ee_international_sanctions', 'eu_travel_bans',
    'eu_journal_sanctions', 'eu_esma_saris', 'EU-ESMA', 'eu_fsf', 'EU-US-LEG', 'EU-TUN', 'EU-CYB',
    'EU-HR', 'EU-HAM', 'EU-SYR', 'EU-CHEM', 'EU-AFG', 'EU-PRK', 'EU-MDA', 'EU-SDNZ', 'EU-RUSDA',
    'EU-BLR', 'EU-BOSNIA', 'EU-BDI', 'EU-GTM', 'EU-GIN', 'EU-GNB', 'EU-HTI', 'EU-LEBANON', 'EU-LBY',
    'EU-MLI', 'EU-MMR', 'EU-NIC', 'EU-NIGER', 'EU-SOM', 'EU-SSD', 'EU-SDN', 'EU-COD', 'EU-VEN',
    'EU-YEM', 'EU-ZWE', 'EU-TUR', 'EU-IRQ', 'EU-TAQA-EUAQ', 'EU-IRN', 'EU-RUS', 'EU-UKR', 'EU-TERR',
    'EU-UNLI', 'EU-CAF', 'eu_sanctions_map', 'fr_tresor_gels_avoir', 'FR-CMF-562', 'ge_ot_list',
    'in_mha_banned', 'IN-UAPA', 'id_dttot', 'ir_sanctions', 'IR-MFA-SANC', 'iq_aml_list',
    'ie_unlawful_organizations', 'il_wmd_sanctions', 'il_mod_crypto', 'il_mod_terrorists',
    'jp_mof_sanctions', 'jp_meti_eul', 'jp_meti_ru', 'kz_afmrk_sanctions', 'KZ-PTA', 'KZ-TFL',
    'kg_fiu_national', 'lv_fiu_sanctions', 'lv_magnitsky_list', 'lt_magnitsky_amendments',
    'lt_fiu_freezes', 'LT-SL', 'my_moha_sanctions', 'md_terror_sanctions', 'mc_fund_freezes',
    'np_mha_sanctions', 'nl_terrorism_list', 'NL-UNSC1373', 'nz_designated_terrorists', 'NZ-UNSC1373',
    'nz_russia_sanctions', 'NZ-RSA2022', 'ng_nigsac_sanctions', 'pk_proscribed_persons', 'PK-ATA1997',
    'ps_local_freezing', 'ph_amlc_sanctions', 'PH-...SECO-ZIM', 'SECO-HAITI', 'SECO-MOLDOVA',
    'SECO-UKRAINE', 'tw_shtc', 'th_designated_person', 'TH-SEC-7', 'tr_fcib', 'gb_fcdo_sanctions',
    'GB-SAMLA', 'gb_hmt_sanctions', 'GB-FO', 'GB-CH', 'GB-AFG', 'GB-AA', 'GB-BH', 'GB-CW', 'GB-CYB',
    'GB-CT', 'GB-AC', 'GB-HR', 'GB-GU', 'GB-HT', 'GB-ICT', 'GB-IRAN', 'GB-IRAN-NW', 'GB-IRQ',
    'GB-ISIL', 'GB-LEB', 'GB-LEB-RH', 'GB-LBY', 'GB-MLI', 'GB-MMR', 'GB-NIC', 'GB-RUS', 'GB-SOM',
    'GB-SSD', 'GB-SDN', 'GB-SYR', 'GB-SYR-CP', 'GB-CAR', 'GB-DPRK', 'GB-DRC', 'GB-BLR', 'GB-GNB',
    'GB-DRILL', 'GB-VEN', 'GB-YEM', 'GB-ZIM', 'gb_hmt_invbans', 'ua_nsdc_sanctions', 'UA-SA1644',
    'ua_sfms_blacklist', 'un_1718_vessels', 'un_sc_sanctions', 'UN-SC2127', 'UN-SC1533', 'UN-SC2048',
    'UN-SC1518', 'UN-SCISIL', 'UN-SC1970', 'UN-SC1718', 'UN-SC1636', 'UN-SC1591', 'UN-SC1988',
    'UN-SC2140', 'ae_local_terrorists', 'AE-UNSC1373', 'us_nk_jointventures', 'us_klepto_hr_visa',
    'us_bis_denied', 'us_cbp_forced_labor', 'us_state_terrorist_orgs', 'US-FTO219', 'us_state_terrorist_exclusion',
    'us_ddtc_debarred', 'US-DDTC-SD', 'us_dod_chinese_milcorps', 'US-DOD-1260H', 'us_fincen_special_measures',
    'us_ofac_cons', 'US-BURMA', 'US-CAPTA', 'US-FSE', 'US-NS-CMIC', 'US-NS-MBS', 'US-NS-PLC', 'US-SSI',
    'us_ofac_sdn', 'US-AFGH', 'US-BALKANS', 'US-BRUS', 'US-NARCO', 'US-TERR', 'US-CYB', 'US-DRC',
    'US-FORINT', 'US-GLOMAG', 'US-HONGKONG', 'US-HOSTAGE', 'US-ICC', 'US-IRAQ', 'US-LEBANON', 'US-MAGNITSKY',
    'US-MALI', 'US-NICARAGUA', 'US-NON-PROLIF', 'US-RUSHAR', 'US-SOMALIA', 'US-SOUTH-SUDAN', 'US-DARFUR',
    'US-SYR-REL', 'US-SYR', 'US-TCO', 'US-UKRRUS-REL', 'US-VEN', 'US-YEMEN', 'us_special_leg', 'US-5949LIST',
    'US-MCCAIN-889', 'US-MCCAIN-1286', 'US-NDAA-154', 'US-CORRUPT-353', 'us_cuba_sanctions', 'US-DOS-CU-PAL',
    'US-DOS-CU-REA', 'us_trade_csl', 'US-AECA-DEBARRED', 'US-BIS-DPL', 'US-BIS-EL', 'US-BIS-MEU', 'US-BIS-UVL',
    'US-DOS-ISN', 'us_dhs_uflpa', 'US-UFLPA',
    # Add all other valid datasets here
]

statement_schema_data_types = {
    'canonical_id': str,
    'prop': str,
    'value': str,
    'dataset': str,
    'schema': str
}

# result = csv_dataset_frequency_for_sanctioned_gender(persons_sub_statements_csv_path, valid_dataset_values_list, statement_schema_data_types)
# print(result)




