import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from IPython.display import display
from opensanctions.const import input_map_raw, input_map_person, statement_full_csv_path, statement_subset_csv_path, total_sanctioned_individuals, total_individuals, total_sanctioned_by_gender, total_sanctioned_individuals
from opensanctions.config import PROJECT_ROOT
import json




# This function calculates the total number of unique individuals (canonical_ids) in the JSON dataset and visualizes the results in a bar plot. It also displays the results in a table format.
def json_total_individual_per_year():
    results = []

    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)  # Load the entire JSON file as a list of objects
                for obj in data:
                    canonical_id = obj.get("id")
                    if canonical_id:
                        ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'year': year, 'unique_individuals': len(ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['unique_individuals'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Unique Individuals')
    plt.title('Total Number of Unique Individuals per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index(df.columns[0]))   



# Calculates the total number of unique individuals (canonical_ids) in the JSON dataset where the topics include 'sanction' or 'sanction_counter'.
def json_total_sanctioned_individual():
    results = []

    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanctioned_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)  # Load the entire JSON file as a list of objects
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])

                    if "sanction" in topics or "sanction.counter" in topics:
                        canonical_id = obj.get("id")
                        if canonical_id:
                            sanctioned_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'Year': year, 'Sanctioned Individuals': len(sanctioned_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='Year')

    df['Relative Frequency(%)'] = df.apply(lambda row: round((row['Sanctioned Individuals'] / total_individuals[row['Year']]) * 100, 2), axis=1)

# Print the title
    print("\033[1mTable 1.\033[0m Distribution of sanctioned individuals per year.") 

 # Display the table
    display(df.set_index('Year')) 

    # Create bar plot
    # Bar plot
    print("\033[1mFigure 1\033[0m")

    plt.figure(figsize=(10, 6))
    plt.bar(df['Year'], df['Sanctioned Individuals'], color='salmon')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanctioned Individuals')
    plt.title('Distribution of Sanctioned Individuals per Year')
    plt.xticks(df['Year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

   








# This function calculates the total number of unique individuals (canonical_ids) in the JSON dataset where the topics include 'sanction_counter' and not 'sanction'.
def json_total_sanction_counter_and_not_sanction_individual_per_year():
    results = []

    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanction_counter_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)  # Load the entire JSON file as a list of objects
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])

                    if "sanction.counter" in topics and "sanction" not in topics:
                        canonical_id = obj.get("id")
                        if canonical_id:
                            sanction_counter_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'year': year, 'sanction_counter_individuals': len(sanction_counter_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanction_counter_individuals'], color='lightcoral')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanction Counter Individuals')
    plt.title('Total Number of Sanction Counter (and not Sanction) Individuals per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index(df.columns[0]))



def json_total_sanctioned_individual_with_gender_per_year():
    results = []
    
    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanctioned_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])
                    gender = properties.get("gender", [])

                    if gender and ("sanction" in topics or "sanction.counter" in topics):
                        canonical_id = obj.get("id")
                        if canonical_id:
                            sanctioned_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'Year': year, 'Sanctioned Individuals': len(sanctioned_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='Year')

    # Calculate relative frequency (percentage)
    df['Relative Frequency(%)'] = df.apply(lambda row: round((row['Sanctioned Individuals'] / total_sanctioned_individuals[row['Year']]) * 100, 2), axis=1)

# Print the title
    print("\033[1mTable 2.\033[0m Distribution of sanctioned individuals with gender per year.")

 # Display the table
    display(df.set_index('Year'))

    # Create bar plot
    # Bar plot
    print("\033[1mFigure 2\033[0m")

    plt.figure(figsize=(10, 6))
    plt.bar(df['Year'], df['Sanctioned Individuals'], color='salmon')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanctioned Individuals with Gender')
    plt.title('Distribution of Sanctioned Individuals with Gender per Year')
    plt.xticks(df['Year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

   




def json_total_sanctioned_individual_without_gender_per_year():
    results = []
    
    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanctioned_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])
                    gender = properties.get("gender", [])

                    if "gender" not in properties:
                        topics = properties.get("topics", [])
                        if "sanction" in topics or "sanction.counter" in topics:
                            canonical_id = obj.get("id")
                            if canonical_id:
                                sanctioned_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'year': year, 'sanctioned_individuals': len(sanctioned_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')
    

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanctioned_individuals'], color='salmon')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanctioned Individuals not having Gender')
    plt.title('Total Number of Sanctioned Individuals without Gender per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index('year'))




def json_total_sanction_counter_and_not_sanction_individual_with_gender_per_year():
    results = []

    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanction_counter_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])
                    gender = properties.get("gender", [])

                    if gender and "sanction.counter" in topics and "sanction" not in topics:
                        canonical_id = obj.get("id")
                        if canonical_id:
                            sanction_counter_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'year': year, 'sanction_counter_individuals': len(sanction_counter_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    if df.empty:
        print("No valid data found.")
        return

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    # Calculate relative frequency (percentage)
    df['relative_frequency(%)'] = df.apply(lambda row: round((row['sanction_counter_individuals'] / total_sanctioned_individuals.get(row['year'], 1)) * 100, 2), axis=1)

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanction_counter_individuals'], color='lightcoral')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanction Counter Individuals with Gender')
    plt.title('Total Number of Sanction Counter (and not Sanction) Individuals with Gender per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index('year'))



def json_total_sanction_counter_and_not_sanction_individual_without_gender_per_year():
    results = []

    for json_input, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_input
        sanction_counter_ids = set()

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for obj in data:
                    properties = obj.get("properties", {})
                    topics = properties.get("topics", [])

                    # Check if 'gender' key is not present in properties
                    if "gender" not in properties and "sanction.counter" in topics and "sanction" not in topics:
                        canonical_id = obj.get("id")
                        if canonical_id:
                            sanction_counter_ids.add(canonical_id)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

        year = exact_date[:4]
        results.append({'year': year, 'sanction_counter_individuals': len(sanction_counter_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    if df.empty:
        print("No valid data found.")
        return

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanction_counter_individuals'], color='lightcoral')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanction Counter Individuals without Gender')
    plt.title('Total Number of Sanction Counter (and not Sanction) Individuals without Gender per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index('year'))





def count_gender_categories_for_sanctioned_individuals_json():
    results = []

    for json_path_str, exact_date in input_map_person.items():
        json_path = PROJECT_ROOT / json_path_str
        gender_categories = defaultdict(int)

        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)  # data is a list of entities

            # Identify sanctioned individuals
            sanctioned_ids = set()
            for entity in data:
                if entity.get('schema') == 'Person':
                    topics = entity.get('properties', {}).get('topics', [])
                    if any(t in ['sanction', 'sanction.counter'] for t in topics):
                        sanctioned_ids.add(entity['id'])

            # Extract gender information (FIRST value only)
            gender_categories = {'male': 0, 'female': 0}
            for entity in data:
                if entity['id'] in sanctioned_ids and 'gender' in entity.get('properties', {}):
                    first_gender = entity['properties']['gender'][0].lower().strip()
                    if first_gender in ['male', 'female']:
                        gender_categories[first_gender] += 1

            # # Categorize individuals
            # for canonical_id, genders in gender_map.items():
            #     if len(genders) > 1:
            #         gender_categories['mixed'] += 1
            #     else:
            #         gender = next(iter(genders))
            #         gender_categories[gender] += 1

            # Append results
            year = exact_date[:4]
            results.append({
                'Year': year,
                'Male': gender_categories.get('male', 0),
                'Female': gender_categories.get('female', 0)
            })

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_path}: {e}")
            continue

    if not results:
        print("No valid data found.")
        return

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='Year')

    # Set the year as the index
    df.set_index('Year', inplace=True)

    # Calculate relative frequency for each gender category
    for gender in ['Male', 'Female']:
        df[f'{gender}_rel_freq(%)'] = round(
            (df[gender] / df.index.map(total_sanctioned_by_gender)) * 100, 2
        )

    # Create a frequency table with both absolute and relative frequencies
    frequency_table = pd.DataFrame()
    for gender in ['Male', 'Female']:
        frequency_table[f'{gender}'] = df[gender]
        frequency_table[f'{gender}_rel_freq(%)'] = df[f'{gender}_rel_freq(%)']

# Print the title
    print("\033[1mTable 3.\033[0m Gender distribution among sanctioned individuals per year.")

# Display the frequency table
    display(frequency_table)

    # Create bar plot
    print("\033[1mFigure 3\033[0m")

    ax = df[['Male', 'Female']].plot(kind='bar', figsize=(12, 6), color=['darkred', 'lightgreen', 'orange'], width=0.8)
    plt.xlabel('Year')
    plt.ylabel('Number of Individuals')
    plt.title('Gender Distribution Among Sanctioned Individuals per Year')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.show()


































