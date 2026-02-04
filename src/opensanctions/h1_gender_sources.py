import pandas as pd
import matplotlib.pyplot as plt




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
    'US-DOS-ISN', 'us_dhs_uflpa', 'US-UFLPA'
]





def gender_source_frequency(input_file: str) -> pd.DataFrame:
    """
    Analyze the frequency of gender sources in the statements dataset,
    filtered for rows where 'prop' is 'gender' and 'topics' is 'sanction'.

    Parameters
    ----------
    input_file : str
        Path to the statements CSV file.
    valid_dataset_values_list : list
        List of valid dataset values.

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
        input_file,
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
        input_file,
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

    # Classify datasets into valid and non_valid
    gender_rows_df['dataset_category'] = gender_rows_df['dataset'].apply(
        lambda x: 'valid_dataset' if x in valid_dataset_values_list else 'non_valid_dataset'
    )

    # Frequency table
    frequency_table = gender_rows_df['dataset_category'].value_counts().reset_index()
    frequency_table.columns = ['dataset_category', 'count']

    # Bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_table['dataset_category'], frequency_table['count'], color=['green', 'red'])
    plt.title('Frequency of Valid and Non-Valid Datasets')
    plt.xlabel('Dataset Category')
    plt.ylabel('Count')
    plt.show()

    return frequency_table


input_file = '/home/ljutach/Documents/auri_projects/opensanctions/datasets/2026/statements_2026.csv'

frequency_table = gender_source_frequency(input_file)
print(frequency_table)
















