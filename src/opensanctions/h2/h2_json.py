import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from opensanctions.const import input_map_person, country_mapping
from opensanctions.config import PROJECT_ROOT



# def json_categorical_frequency_for_sanctioned_gender_by_year(category='nationality', mapping_dict=None, min_count=50):
#     """
#     Generate a relative frequency table and plot for gender vs. a categorical variable from JSON files,
#     processing each year's data separately.

#     Parameters:
#     - category: str (property to analyze, e.g., 'nationality', 'ethnicity', or 'religion')
#     - mapping_dict: dict (optional mapping for category codes to full names)
#     - min_count: int (minimum total count to include in the plot)

#     Returns:
#     - Dictionary with year as key and relative_frequency_table as value
#     """
#     results = {}

#     # Process each JSON file (each representing a year)
#     for json_input, exact_date in input_map_person.items():
#         json_path = PROJECT_ROOT / json_input
#         year = exact_date[:4]  # Extract year from exact_date

#         # Initialize data structures for this year
#         gender_category_counts = defaultdict(lambda: defaultdict(int))
#         total_counts = defaultdict(int)

#         try:
#             with open(json_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)

#                 # Check if data is a list, if not, make it a list
#                 if not isinstance(data, list):
#                     data = [data]

#                 for entry in data:
#                     if entry.get('schema') == 'Person' and entry.get('target', False):
#                         # Get canonical_id (using 'id' field from JSON)
#                         canonical_id = entry.get('id')

#                         # Get gender
#                         gender_values = entry.get('properties', {}).get('gender', [])
#                         if not gender_values:
#                             continue  # Skip if no gender

#                         gender = gender_values[0]  # Take first gender value

#                         # Get category value
#                         category_values = entry.get('properties', {}).get(category, [])
#                         if not category_values:
#                             continue  # Skip if no category

#                         category_value = category_values[0]  # Take first category value

#                         # Update counts
#                         gender_category_counts[gender][category_value] += 1
#                         total_counts[gender] += 1

#                 # Convert counts to DataFrame for this year
#                 rows = []
#                 for gender, category_dict in gender_category_counts.items():
#                     for category_value, count in category_dict.items():
#                         rows.append({'gender': gender, category: category_value, 'count': count, 'year': year})

#                 if not rows:
#                     print(f"No data found for {year} for the specified category and gender.")
#                     continue

#                 df = pd.DataFrame(rows)

#                 # Map category codes to full names if a mapping dictionary is provided
#                 if mapping_dict is not None:
#                     df[f'{category}_name'] = df[category].map(mapping_dict)
#                     category_name_col = f'{category}_name'
#                 else:
#                     category_name_col = category
#                     df[category_name_col] = df[category]

#                 # Group by gender and category_name, summing the counts
#                 df_grouped = df.groupby(['gender', category_name_col], as_index=False).sum()

#                 # Pivot the grouped DataFrame to create a contingency table
#                 contingency_table = df_grouped.pivot(index='gender', columns=category_name_col, values='count').fillna(0)

#                 # Transpose the contingency table to reverse the axis order
#                 transposed_contingency_table = contingency_table.T

#                 # Calculate relative frequencies (percentages) for the table
#                 relative_frequency_table = transposed_contingency_table.div(transposed_contingency_table.sum(axis=1), axis=0) * 100

#                 # Round values to 2 decimal places
#                 relative_frequency_table = relative_frequency_table.round(2)

#                 # Filter categories with total count >= min_count for the plot
#                 category_counts = df.groupby(category)['count'].sum()
#                 valid_categories = category_counts[category_counts >= min_count].index
#                 filtered_df = df[df[category].isin(valid_categories)].copy()

#                 # Map category names for filtered data if a mapping dictionary is provided
#                 if mapping_dict is not None:
#                     filtered_df.loc[:, category_name_col] = filtered_df[category].map(mapping_dict)

#                 # Group by gender and category_name for filtered data
#                 filtered_df_grouped = filtered_df.groupby(['gender', category_name_col], as_index=False).sum()

#                 # Pivot the filtered DataFrame to create a contingency table for the plot
#                 filtered_contingency_table = filtered_df_grouped.pivot(index='gender', columns=category_name_col, values='count').fillna(0)

#                 # Transpose the filtered contingency table to swap axes
#                 transposed_table = filtered_contingency_table.T

#                 # Normalize the transposed table to get relative frequencies (percentages)
#                 normalized_table = transposed_table.div(transposed_table.sum(axis=1), axis=0) * 100

#                 # Create a diverging stacked bar chart with relative frequencies
#                 plt.figure(figsize=(12, 6))
#                 ax = normalized_table.plot(kind='bar', stacked=True, color=['lightgreen', 'darkred'])

#                 # Customize the plot
#                 plt.title(f'Relative Frequency of Gender by {category.capitalize()} ({year}, Count >= {min_count})')
#                 plt.xlabel(category.capitalize())
#                 plt.ylabel('Relative Frequency (%)')
#                 plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
#                 plt.tight_layout()

#                 # Show the plot
#                 plt.show()

#                 # Store results for this year
#                 results[year] = relative_frequency_table

#         except Exception as e:
#             print(f"Error processing {json_path}: {e}")
#             continue

#     return results






def json_categorical_frequency_for_sanctioned_gender_by_year(category='nationality', mapping_dict=None, min_count=50):
    """
    Generate a relative frequency table and plot for gender vs. a categorical variable from JSON files,
    processing each year's data separately.

    Parameters:
    - category: str (property to analyze, e.g., 'nationality', 'ethnicity', or 'religion')
    - mapping_dict: dict (optional mapping for category codes to full names)
    - min_count: int (minimum total count to include in the plot and table)

    Returns:
    - Dictionary with year as key and relative_frequency_table as value
    """
    results = {}

    # Process each JSON file (each representing a year)
    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        year = exact_date[:4]  # Extract year from exact_date

        # Initialize data structures for this year
        gender_category_counts = defaultdict(lambda: defaultdict(int))
        total_counts = defaultdict(int)

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Check if data is a list, if not, make it a list
                if not isinstance(data, list):
                    data = [data]

                for entry in data:
                    if entry.get('schema') == 'Person' and entry.get('target', False):
                        # Get canonical_id (using 'id' field from JSON)
                        canonical_id = entry.get('id')

                        # Get gender
                        gender_values = entry.get('properties', {}).get('gender', [])
                        if not gender_values:
                            continue  # Skip if no gender

                        gender = gender_values[0]  # Take first gender value

                        # Get category value
                        category_values = entry.get('properties', {}).get(category, [])
                        if not category_values:
                            continue  # Skip if no category

                        category_value = category_values[0]  # Take first category value

                        # Update counts
                        gender_category_counts[gender][category_value] += 1
                        total_counts[gender] += 1

                # Convert counts to DataFrame for this year
                rows = []
                for gender, category_dict in gender_category_counts.items():
                    for category_value, count in category_dict.items():
                        rows.append({'gender': gender, category: category_value, 'count': count, 'year': year})

                if not rows:
                    print(f"No data found for {year} for the specified category and gender.")
                    continue

                df = pd.DataFrame(rows)

                # Filter categories with total count >= min_count for the entire dataset
                category_counts = df.groupby(category)['count'].sum()
                valid_categories = category_counts[category_counts >= min_count].index
                df = df[df[category].isin(valid_categories)].copy()

                if df.empty:
                    print(f"No categories meet the minimum count of {min_count} for {year}.")
                    continue

                # Map category codes to full names if a mapping dictionary is provided
                if mapping_dict is not None:
                    df[f'{category}_name'] = df[category].map(mapping_dict)
                    category_name_col = f'{category}_name'
                else:
                    category_name_col = category
                    df[category_name_col] = df[category]

                # Group by gender and category_name, summing the counts
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
                filtered_df = df.copy()

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
                ax = normalized_table.plot(kind='bar', stacked=True, color=['lightgreen', 'darkred'])

                # Customize the plot
                plt.title(f'Relative Frequency of Gender by {category.capitalize()} ({year}, Count >= {min_count})')
                plt.xlabel(category.capitalize())
                plt.ylabel('Relative Frequency (%)')
                plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()

                # Show the plot
                plt.show()

                # Store results for this year
                results[year] = relative_frequency_table

        except Exception as e:
            print(f"Error processing {json_path}: {e}")
            continue

    return results




