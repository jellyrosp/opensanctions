import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from opensanctions.const import statement_full_csv_path, statement_schema_data_types, valid_dataset_values_list, statement_subset_csv_path, persons_sub_db_path, country_mapping



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





def csv_sanctioned_gender_topics_frequency(mapping_dict=None, min_count=0):
    """
    Generate a relative frequency table and plot for gender vs. topics for sanctioned individuals.

    Parameters:
    - mapping_dict: dict (optional mapping for topics codes to full names)
    - min_count: int (minimum total count to include in the plot)
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    # SQL query to count unique sanctioned individuals with gender and topics
    query = """
        WITH
        -- Individuals with at least one 'sanction' or 'sanction.counter' in topics
        sanctioned_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics' AND value IN ('sanction', 'sanction.counter')
        ),

        -- Individuals with at least one other topics value (not 'sanction' or 'sanction.counter')
        other_topics_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics' AND value NOT IN ('sanction', 'sanction.counter')
        ),

        -- Individuals meeting both criteria
        valid_individuals AS (
            SELECT canonical_id
            FROM sanctioned_individuals
            INTERSECT
            SELECT canonical_id
            FROM other_topics_individuals
        ),

        -- Gender data for valid individuals
        gender_data AS (
            SELECT p.canonical_id, p.value AS gender
            FROM persons_topics p
            JOIN valid_individuals v ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'gender'
        ),

        -- Topics data for valid individuals
        topics_data AS (
            SELECT p.canonical_id, p.value AS topics
            FROM persons_topics p
            JOIN valid_individuals v ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'topics'
        )

        -- Contingency table: gender × topics
        SELECT
            g.gender,
            t.topics,
            COUNT(DISTINCT g.canonical_id) AS count
        FROM
            gender_data g
        JOIN
            topics_data t ON g.canonical_id = t.canonical_id
        GROUP BY
            g.gender, t.topics
        ORDER BY
            g.gender, t.topics;
    """

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert results to a DataFrame
    df = pd.DataFrame(results, columns=['Gender', 'Topics', 'count'])

    # Map topics codes to full names if a mapping dictionary is provided
    if mapping_dict is not None:
        df['topics_name'] = df['topics'].map(mapping_dict)
        topics_name_col = 'topics_name'
    else:
        topics_name_col = 'Topics'
        df[topics_name_col] = df['Topics']

    # Group by gender and topics_name, summing the counts to avoid duplicates
    df_grouped = df.groupby(['Gender', topics_name_col], as_index=False).sum()

    # Pivot the grouped DataFrame to create a contingency table
    contingency_table = df_grouped.pivot(index='Gender', columns=topics_name_col, values='count').fillna(0)

    # Transpose the contingency table to reverse the axis order
    transposed_contingency_table = contingency_table.T

    # Calculate relative frequencies (percentages) for the table
    relative_frequency_table = transposed_contingency_table.div(transposed_contingency_table.sum(axis=1), axis=0) * 100

    # Round values to 2 decimal places
    relative_frequency_table = relative_frequency_table.round(2)

    # Filter topics with total count >= min_count for the plot
    topics_counts = df.groupby('Topics')['count'].sum()
    valid_topics = topics_counts[topics_counts >= min_count].index
    filtered_df = df[df['Topics'].isin(valid_topics)].copy()

    # Map topics names for filtered data if a mapping dictionary is provided
    if mapping_dict is not None:
        filtered_df.loc[:, topics_name_col] = filtered_df['Topics'].map(mapping_dict)

    # Group by gender and topics_name for filtered data
    filtered_df_grouped = filtered_df.groupby(['Gender', topics_name_col], as_index=False).sum()

    # Pivot the filtered DataFrame to create a contingency table for the plot
    filtered_contingency_table = filtered_df_grouped.pivot(index='Gender', columns=topics_name_col, values='count').fillna(0)

    # Transpose the filtered contingency table to swap axes
    transposed_table = filtered_contingency_table.T

    # Normalize the transposed table to get relative frequencies (percentages)
    normalized_table = transposed_table.div(transposed_table.sum(axis=1), axis=0) * 100

    # Create a diverging stacked bar chart with relative frequencies
    
    ax = normalized_table.plot(kind='bar', stacked=True, color=['lightgreen', 'darkred'], figsize=(12, 6))

    # Customize the plot
    plt.title(f'Relative Frequency of Gender by Topics (100% Stacked, Count >= {min_count})')
    plt.xlabel('Topics')
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
    return relative_frequency_table




def csv_sanctioned_gender_specific_topics_frequency(gender, min_count=0):
    """
    Generate a relative frequency table and bar plot for a specific gender vs. topics for sanctioned individuals.

    Parameters:
    - gender: str (specific gender to focus on, e.g., 'female' or 'male')
    - min_count: int (minimum count to include a topic in the plot and table)
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    # SQL query to get the frequency table for the specified gender
    query = f"""
        WITH
        -- Individuals with at least one 'sanction' or 'sanction.counter' in topics
        sanctioned_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics' AND value IN ('sanction', 'sanction.counter')
        ),

        -- Individuals with at least one other topics value (not 'sanction' or 'sanction.counter')
        other_topics_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics' AND value NOT IN ('sanction', 'sanction.counter')
        ),

        -- Individuals meeting both criteria
        valid_individuals AS (
            SELECT canonical_id
            FROM sanctioned_individuals
            INTERSECT
            SELECT canonical_id
            FROM other_topics_individuals
        ),

        -- Gender data for valid individuals
        gender_data AS (
            SELECT p.canonical_id, p.value AS gender
            FROM persons_topics p
            JOIN valid_individuals v ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'gender'
        ),

        -- Topics data for valid individuals
        topics_data AS (
            SELECT p.canonical_id, p.value AS topics
            FROM persons_topics p
            JOIN valid_individuals v ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'topics'
        ),

        -- Contingency table: gender × topics for a specific gender
        specific_gender_topics AS (
            SELECT
                t.topics,
                COUNT(DISTINCT g.canonical_id) AS count
            FROM
                gender_data g
            JOIN
                topics_data t ON g.canonical_id = t.canonical_id
            WHERE
                g.gender = '{gender}'
            GROUP BY
                t.topics
        ),

        -- Total count of individuals for the specific gender
        total_count AS (
            SELECT
                COUNT(DISTINCT canonical_id) AS total
            FROM
                gender_data
            WHERE
                gender = '{gender}'
        )

        -- Frequency table with relative frequency for the specific gender
        SELECT
            s.topics,
            s.count,
            ROUND((s.count * 100.0 / t.total), 2) AS relative_frequency
        FROM
            specific_gender_topics s
        CROSS JOIN
            total_count t
        ORDER BY
            s.count DESC;
    """

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert results to a DataFrame
    df = pd.DataFrame(results, columns=['Topics', 'Frequency', 'Relative Frequency'])

    # Filter topics with count >= min_count
    if min_count > 0:
        df = df[df['Frequency'] >= min_count]

    # Create a bar plot with relative frequencies
    plt.figure(figsize=(12, 6))
    ax = plt.bar(df['Topics'], df['Relative Frequency'], color='darkred')

    # Customize the plot
    plt.title(f'Relative Frequency of Topics for Gender {gender.capitalize()} (Count >= {min_count})')
    plt.xlabel('Topics')
    plt.ylabel('Relative Frequency (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Set pandas display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Return the frequency table
    return df









