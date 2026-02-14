import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from opensanctions.const import statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list, statement_subset_csv_path, persons_sub_db_path, country_mapping




# def csv_nationality_frequency_for_sanctioned_gender():
#     # Connect to the SQLite database
#     conn = sqlite3.connect(persons_sub_db_path)
#     cursor = conn.cursor()

#     # SQL query to count unique sanctioned individuals with gender and nationality
#     query = """
#         WITH gender_data AS (
#             SELECT canonical_id, value AS gender
#             FROM persons
#             WHERE prop = 'gender'
#         ),
#         nationality_data AS (
#             SELECT canonical_id, value AS nationality
#             FROM persons
#             WHERE prop = 'nationality'
#         )
#         SELECT
#             g.gender,
#             n.nationality,
#             COUNT(DISTINCT g.canonical_id) AS count
#         FROM
#             gender_data g
#         JOIN
#             nationality_data n ON g.canonical_id = n.canonical_id
#         GROUP BY
#             g.gender, n.nationality
#         ORDER BY
#             g.gender, n.nationality;
#     """

#     # Execute the query
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()

#     # Convert results to a DataFrame
#     df = pd.DataFrame(results, columns=['gender', 'nationality', 'count'])

#     # Map country codes to full names
#     df['country_name'] = df['nationality'].map(country_mapping)

#     # Group by gender and country_name, summing the counts to avoid duplicates
#     df_grouped = df.groupby(['gender', 'country_name'], as_index=False).sum()

#     # Pivot the grouped DataFrame to create a contingency table with full country names
#     contingency_table = df_grouped.pivot(index='gender', columns='country_name', values='count').fillna(0)

#     # Transpose the contingency table to reverse the axis order
#     transposed_contingency_table = contingency_table.T

#     # Calculate relative frequencies (percentages) for the table
#     relative_frequency_table = transposed_contingency_table.div(transposed_contingency_table.sum(axis=1), axis=0) * 100

#     # Round values to 2 decimal places
#     relative_frequency_table = relative_frequency_table.round(2)

#     # Set pandas display options to show all rows and columns
#     # pd.set_option('display.max_rows', None)
#     # pd.set_option('display.max_columns', None)
#     # pd.set_option('display.width', None)
#     # pd.set_option('display.max_colwidth', None)

#     # # Display the relative frequency table
#     # display(relative_frequency_table)

#     # Reset display options to default
#     pd.reset_option('all')

#     # Filter nationalities with total count >= 50 for the plot
#     nationality_counts = df.groupby('nationality')['count'].sum()
#     valid_nationalities = nationality_counts[nationality_counts >= 50].index
#     filtered_df = df[df['nationality'].isin(valid_nationalities)].copy()

#     # Map country names for filtered data
#     filtered_df.loc[:, 'country_name'] = filtered_df['nationality'].map(country_mapping)

#     # Group by gender and country_name for filtered data
#     filtered_df_grouped = filtered_df.groupby(['gender', 'country_name'], as_index=False).sum()

#     # Pivot the filtered DataFrame to create a contingency table for the plot
#     filtered_contingency_table = filtered_df_grouped.pivot(index='gender', columns='country_name', values='count').fillna(0)

#     # Transpose the filtered contingency table to swap axes
#     transposed_table = filtered_contingency_table.T

#     # Normalize the transposed table to get relative frequencies (percentages)
#     normalized_table = transposed_table.div(transposed_table.sum(axis=1), axis=0) * 100

#     # Create a diverging stacked bar chart with relative frequencies
#     plt.figure(figsize=(12, 6))
#     ax = normalized_table.plot(kind='bar', stacked=True, color=['lightgreen', 'darkred'], figsize=(12, 6))

#     # Customize the plot
#     plt.title('Relative Frequency of Gender by Nationality (100% Stacked, Count >= 50)')
#     plt.xlabel('Country')
#     plt.ylabel('Relative Frequency (%)')
#     plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.tight_layout()

#     # Show the plot
#     plt.show()

#     pd.set_option('display.max_rows', None)
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.width', None)
#     pd.set_option('display.max_colwidth', None)

#     # Display the relative frequency table
#     display(relative_frequency_table)



def csv_categorical_frequency_for_sanctioned_gender(category='nationality', mapping_dict=None, min_count=50):
    """
    Generate a relative frequency table and plot for gender vs. a categorical variable.

    Parameters:
    - category: str ('nationality', 'ethnicity', or 'religion')
    - mapping_dict: dict (optional mapping for category codes to full names)
    - min_count: int (minimum total count to include in the plot)
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    # SQL query to count unique sanctioned individuals with gender and the specified category
    query = f"""
        WITH gender_data AS (
            SELECT canonical_id, value AS gender
            FROM persons
            WHERE prop = 'gender'
        ),
        {category}_data AS (
            SELECT canonical_id, value AS {category}
            FROM persons
            WHERE prop = '{category}'
        )
        SELECT
            g.gender,
            c.{category},
            COUNT(DISTINCT g.canonical_id) AS count
        FROM
            gender_data g
        JOIN
            {category}_data c ON g.canonical_id = c.canonical_id
        GROUP BY
            g.gender, c.{category}
        ORDER BY
            g.gender, c.{category};
    """

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert results to a DataFrame
    df = pd.DataFrame(results, columns=['gender', category, 'count'])

    # Map category codes to full names if a mapping dictionary is provided
    if mapping_dict is not None:
        df[f'{category}_name'] = df[category].map(mapping_dict)
        category_name_col = f'{category}_name'
    else:
        category_name_col = category
        df[category_name_col] = df[category]

    # Group by gender and category_name, summing the counts to avoid duplicates
    df_grouped = df.groupby(['gender', category_name_col], as_index=False).sum()

    # Pivot the grouped DataFrame to create a contingency table
    contingency_table = df_grouped.pivot(index='gender', columns=category_name_col, values='count').fillna(0)

    # Transpose the contingency table to reverse the axis order
    transposed_contingency_table = contingency_table.T

    # Calculate relative frequencies (percentages) for the table
    relative_frequency_table = transposed_contingency_table.div(transposed_contingency_table.sum(axis=1), axis=0) * 100

    # Round values to 2 decimal places
    relative_frequency_table = relative_frequency_table.round(2)

    # Filter categories with total count >= min_count for the plot
    category_counts = df.groupby(category)['count'].sum()
    valid_categories = category_counts[category_counts >= min_count].index
    filtered_df = df[df[category].isin(valid_categories)].copy()

    # Map category names for filtered data if a mapping dictionary is provided
    if mapping_dict is not None:
        filtered_df.loc[:, category_name_col] = filtered_df[category].map(mapping_dict)

    # Group by gender and category_name for filtered data
    filtered_df_grouped = filtered_df.groupby(['gender', category_name_col], as_index=False).sum()

    # Pivot the filtered DataFrame to create a contingency table for the plot
    filtered_contingency_table = filtered_df_grouped.pivot(index='gender', columns=category_name_col, values='count').fillna(0)

    # Transpose the filtered contingency table to swap axes
    transposed_table = filtered_contingency_table.T

    # Normalize the transposed table to get relative frequencies (percentages)
    normalized_table = transposed_table.div(transposed_table.sum(axis=1), axis=0) * 100

    # Create a diverging stacked bar chart with relative frequencies
    plt.figure(figsize=(12, 6))
    ax = normalized_table.plot(kind='bar', stacked=True, color=['lightgreen', 'darkred'], figsize=(12, 6))

    # Customize the plot
    plt.title(f'Relative Frequency of Gender by {category.capitalize()} (100% Stacked, Count >= {min_count})')
    plt.xlabel(category.capitalize())
    plt.ylabel('Relative Frequency (%)')
    plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Set pandas display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Display the relative frequency table
    display(relative_frequency_table)























# def csv_nationality_frequency_for_sanctioned_gender():
#     # Connect to the SQLite database
#     conn = sqlite3.connect(persons_sub_db_path)
#     cursor = conn.cursor()

#     # SQL query to count unique sanctioned individuals with gender and nationality
#     query = """
#         WITH gender_data AS (
#             SELECT canonical_id, value AS gender
#             FROM persons
#             WHERE prop = 'gender'
#         ),
#         nationality_data AS (
#             SELECT canonical_id, value AS nationality
#             FROM persons
#             WHERE prop = 'nationality'
#         )
#         SELECT
#             g.gender,
#             n.nationality,
#             COUNT(DISTINCT g.canonical_id) AS count
#         FROM
#             gender_data g
#         JOIN
#             nationality_data n ON g.canonical_id = n.canonical_id
#         GROUP BY
#             g.gender, n.nationality
#         ORDER BY
#             g.gender, n.nationality;
#     """

#     # Execute the query
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()

#     # Convert results to a DataFrame
#     df = pd.DataFrame(results, columns=['gender', 'nationality', 'count'])

#     # Pivot the DataFrame to create a contingency table
#     contingency_table = df.pivot(index='gender', columns='nationality', values='count').fillna(0)

#     # Display the contingency table
#     display(contingency_table)

#     # Transpose the contingency table to swap axes
#     transposed_table = contingency_table.T

#     # Normalize the transposed table to get relative frequencies (percentages)
#     normalized_table = transposed_table.div(transposed_table.sum(axis=1), axis=0) * 100

#     # Create a horizontal diverging stacked bar chart with relative frequencies
#     plt.figure(figsize=(12, 8))
#     ax = normalized_table.plot(kind='barh', stacked=True, colormap='RdBu_r', figsize=(12, 8))

#     # Customize the plot
#     plt.title('Relative Frequency of Gender by Nationality (100% Stacked)')
#     plt.xlabel('Relative Frequency (%)')
#     plt.ylabel('Nationality')
#     plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.tight_layout()

#     # Show the plot
#     plt.show()

#     return normalized_table
    