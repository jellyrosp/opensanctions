import os
from opensanctions.config import PROJECT_ROOT

# Define the path to statements_2026.csv
STATEMENT_FULL_CSV_PATH = os.path.join(PROJECT_ROOT, "datasets", "2026", "statements_2026.csv")
statement_full_csv_path = STATEMENT_FULL_CSV_PATH  # Use the same path or define a new one

STATEMENTS_SUBSET_CSV_PATH = os.path.join(PROJECT_ROOT, "datasets", "2026", "persons_sub_statements.csv")
statement_subset_csv_path = STATEMENTS_SUBSET_CSV_PATH

PERSONS_SUB_DB_PATH = os.path.join(PROJECT_ROOT, "datasets", "2026", "persons_sub_statements_db.sql")
persons_sub_db_path = PERSONS_SUB_DB_PATH

SUB_TARGETS_NESTED_REASONS = os.path.join(PROJECT_ROOT, "datasets", "2026", "sub_targets.nested.reasons.json")
sub_targets_nested_reasons_path = SUB_TARGETS_NESTED_REASONS

input_map_raw = {
    "datasets/2021/sanctions-20211231-entities.ftm.json": "20211231",
    "datasets/2022/sanctions-20221231-entities.ftm.json": "20221231",
    "datasets/2023/sanctions-20231231-entities.ftm.json": "20231231",
    "datasets/2024/sanctions-20241231-entities.ftm.json": "20241231",
    "datasets/2025/sanctions-20251231-entities.ftm.json": "20251231",
    "datasets/2026/sanctions-20260201-entities.ftm.json": "20260201"
}

input_map_person = {
    "datasets/2021/sanctions-20211231-persons.ftm.json": "20211231",
    "datasets/2022/sanctions-20221231-persons.ftm.json": "20221231",
    "datasets/2023/sanctions-20231231-persons.ftm.json": "20231231",
    "datasets/2024/sanctions-20241231-persons.ftm.json": "20241231",
    "datasets/2025/sanctions-20251231-persons.ftm.json": "20251231",
    "datasets/2026/sanctions-20260201-persons.ftm.json": "20260201"
}



total_individuals = {
        '2021': 14250,
        '2022': 16619,                
        '2023': 22168,
        '2024': 26233,
        '2025': 40730,
        '2026': 40877
    }


total_sanctioned_individuals = {
        '2021': 10203,
        '2022': 16175,
        '2023': 21100,
        '2024': 24895,
        '2025': 35092,
        '2026': 35241
    }


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


country_mapping = {
    'al': 'Albania',
    'ao': 'Angola',
    'az': 'Azerbaijan',
    'ba': 'Bosnia and Herzegovina',
    'be': 'Belgium',
    'bg': 'Bulgaria',
    'bj': 'Benin',
    'by': 'Belarus',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cm': 'Cameroon',
    'cn': 'China',
    'co': 'Colombia',
    'cr': 'Costa Rica',
    'cu': 'Cuba',
    'cy': 'Cyprus',
    'de': 'Germany',
    'dj': 'Djibouti',
    'dz': 'Algeria',
    'ee': 'Estonia',
    'eg': 'Egypt',
    'fi': 'Finland',
    'fj': 'Fiji',
    'fr': 'France',
    'gb': 'United Kingdom',
    'ge': 'Georgia',
    'gm': 'Gambia',
    'gq': 'Equatorial Guinea',
    'gt': 'Guatemala',
    'gy': 'Guyana',
    'hk': 'Hong Kong',
    'hn': 'Honduras',
    'hr': 'Croatia',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'in': 'India',
    'iq': 'Iraq',
    'ir': 'Iran',
    'it': 'Italy',
    'ke': 'Kenya',
    'kg': 'Kyrgyzstan',
    'kn': 'Saint Kitts and Nevis',
    'kp': 'North Korea',
    'kr': 'South Korea',
    'lb': 'Lebanon',
    'lt': 'Lithuania',
    'lv': 'Latvia',
    'ly': 'Libya',
    'ma': 'Morocco',
    'md': 'Moldova',
    'me': 'Montenegro',
    'mk': 'North Macedonia',
    'mm': 'Myanmar',
    'mt': 'Malta',
    'mx': 'Mexico',
    'ni': 'Nicaragua',
    'nl': 'Netherlands',
    'om': 'Oman',
    'pe': 'Peru',
    'ph': 'Philippines',
    'pk': 'Pakistan',
    'pl': 'Poland',
    'py': 'Paraguay',
    'rs': 'Serbia',
    'ru': 'Russia',
    'sa': 'Saudi Arabia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'si': 'Slovenia',
    'sk': 'Slovakia',
    'so': 'Somalia',
    'sv': 'El Salvador',
    'sy': 'Syria',
    'tn': 'Tunisia',
    'tr': 'Turkey',
    'tw': 'Taiwan',
    'ua': 'Ukraine',
    'ug': 'Uganda',
    'us': 'United States',
    'uz': 'Uzbekistan',
    've': 'Venezuela',
    'xk': 'Kosovo',
    'zw': 'Zimbabwe',
    'ae': 'United Arab Emirates',
    'af': 'Afghanistan',
    'am': 'Armenia',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'bf': 'Burkina Faso',
    'bh': 'Bahrain',
    'br': 'Brazil',
    'bt': 'Bhutan',
    'cd': 'Congo',
    'cf': 'Central African Republic',
    'cg': 'Republic of the Congo',
    'cl': 'Chile',
    'csxx': 'Czechoslovakia',
    'dm': 'Dominica',
    'do': 'Dominican Republic',
    'ec': 'Ecuador',
    'er': 'Eritrea',
    'es': 'Spain',
    'et': 'Ethiopia',
    'gh': 'Ghana',
    'gn': 'Guinea',
    'gw': 'Guinea-Bissau',
    'ht': 'Haiti',
    'hu': 'Hungary',
    'jo': 'Jordan',
    'kh': 'Cambodia',
    'ki': 'Kiribati',
    'kw': 'Kuwait',
    'kz': 'Kazakhstan',
    'li': 'Liechtenstein',
    'lk': 'Sri Lanka',
    'lr': 'Liberia',
    'mv': 'Maldives',
    'mn': 'Mongolia',
    'mr': 'Mauritania',
    'mz': 'Mozambique',
    'na': 'Namibia',
    'ne': 'Niger',
    'ng': 'Nigeria',
    'no': 'Norway',
    'nz': 'New Zealand',
    'pa': 'Panama',
    'ps': 'Palestine',
    'pt': 'Portugal',
    'qa': 'Qatar',
    'rw': 'Rwanda',
    'sd': 'Sudan',
    'sl': 'Sierra Leone',
    'sn': 'Senegal',
    'ss': 'South Sudan',
    'suhh': 'Soviet Union',
    'td': 'Chad',
    'tg': 'Togo',
    'tj': 'Tajikistan',
    'tm': 'Turkmenistan',
    'tt': 'Trinidad and Tobago',
    'tz': 'Tanzania',
    'vu': 'Vanuatu',
    'ye': 'Yemen',
    'za': 'South Africa',
}




sanctions_taxonomy = {
    "AS": {
        "label": "Activity-based sanctions",
        "definition": (
            "Imposed on individuals for their direct involvement in sanctionable activities. "
            "The individual has actively participated in or facilitated the sanctionable conduct."
        )
    },
    "SS": {
        "label": "Status-based sanctions",
        "definition": (
            "Imposed on the basis of an individual’s membership in and/or association with a "
            "target group, regardless of any direct involvement in sanctionable conduct."
        )
    },
    "PS": {
        "label": "Profit-based sanctions",
        "definition": (
            "Imposed on individuals who have derived, directly or indirectly, a benefit from "
            "the sanctionable conduct of a sanctioned person or entity, regardless of any "
            "direct involvement in sanctionable conduct."
        )
    },
    "FS": {
        "label": "Family-member sanctions",
        "definition": (
            "Imposed on individuals who are related by family ties to a sanctioned individual, "
            "regardless of any direct involvement in sanctionable conduct."
        )
    }
}
