import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from opensanctions.const import input_map_raw, input_map_person, statement_full_csv_path, statement_subset_csv_path, total_sanctioned_individuals, total_individuals
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
        results.append({'year': year, 'sanctioned_individuals': len(sanctioned_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    df['relative_frequency(%)'] = df.apply(lambda row: round((row['sanctioned_individuals'] / total_individuals[row['year']]) * 100, 2), axis=1)

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanctioned_individuals'], color='salmon')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanctioned Individuals')
    plt.title('Total Number of Sanctioned Individuals per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index('year')) 








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
        results.append({'year': year, 'sanctioned_individuals': len(sanctioned_ids)})

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Sort DataFrame by year for better visualization
    df = df.sort_values(by='year')

    # Calculate relative frequency (percentage)
    df['relative_frequency(%)'] = df.apply(lambda row: round((row['sanctioned_individuals'] / total_sanctioned_individuals[row['year']]) * 100, 2), axis=1)

    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df['year'], df['sanctioned_individuals'], color='salmon')
    plt.xlabel('Year')
    plt.ylabel('Number of Sanctioned Individuals having Gender')
    plt.title('Total Number of Sanctioned Individuals with Gender per Year')
    plt.xticks(df['year'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Display the table
    display(df.set_index('year'))




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










































