import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
from opensanctions.const import classification_csv_path
from tabulate import tabulate



def load_and_prepare_data(csv_path):
    """
    Load and prepare data from the CSV file.

    Parameters:
        csv_path: str
            Path to the CSV file.

    Returns:
        pd.DataFrame
            DataFrame with columns: B (gender), C (activity), D (profit), E (status), F (family), G (other)
    """
    df = pd.read_csv(csv_path)

    # Rename columns for clarity
    df.columns = ['B', 'C', 'D', 'E', 'F', 'G']

    # Replace 'x' with 1 and empty cells with 0
    for col in ['C', 'D', 'E', 'F', 'G']:
        df[col] = df[col].apply(lambda x: 1 if x == 'x' else 0)

    return df

def get_gender_type_contingency_table(df):
    """
    Returns Gender × Type contingency table for individuals with at least one 'x' in columns 'C','D', E, F, G.

    Parameters:
        df: pd.DataFrame
            DataFrame with columns: B (gender), C (activity), D (profit), E (status), F (family), G (other)

    Returns:
        pd.DataFrame
            Contingency table with columns: Type, Female, Male
    """
    # Filter rows where at least one of D, E, F, G, H is 1
    df_filtered = df[df[['C', 'D', 'E', 'F', 'G']].sum(axis=1) > 0]

    # Melt the DataFrame to long format for easier aggregation
    df_melted = df_filtered.melt(id_vars=['B'], value_vars=['C', 'D', 'E', 'F', 'G'],
                                  var_name='Type', value_name='Value')

    # Filter for rows where Value is 1
    df_melted = df_melted[df_melted['Value'] == 1]

    # Create contingency table
    contingency = df_melted.groupby(['Type', 'B']).size().unstack(fill_value=0).reset_index()
    contingency.columns = ['Type', 'Female', 'Male']

    return contingency



def gender_type_inference(contingency_table):
    """
    Perform inferential analysis of gender × type associations.

    Parameters:
        contingency_table: pd.DataFrame
            Index = Type, columns = ['Female', 'Male']

    Returns:
        results_df: pd.DataFrame
            Type-level odds ratios, confidence intervals, p-values, adjusted p-values, log-odds
        chi2_result: dict
            Global chi-square statistics
        standardized_residuals: pd.DataFrame
            Matrix of standardized residuals
    """
    ct = contingency_table.set_index("Type")
    matrix = ct[["Female", "Male"]]

    chi2, p, dof, expected = chi2_contingency(matrix)
    expected_df = pd.DataFrame(expected, index=matrix.index, columns=matrix.columns)
    standardized_residuals = (matrix - expected_df) / np.sqrt(expected_df)

    total_female = matrix["Female"].sum()
    total_male = matrix["Male"].sum()

    results = []
    for type_, row in matrix.iterrows():
        a = row["Female"]
        c = row["Male"]
        b = total_female - a
        d = total_male - c

        table = np.array([[a, b], [c, d]], dtype=float)
        if (table == 0).any():
            table += 0.5

        oddsratio, pvalue = fisher_exact(table)
        sm_table = sm.stats.Table2x2(table)
        ci_low, ci_high = sm_table.oddsratio_confint()

        results.append({
            "type": type_,
            "female_count": a,
            "male_count": c,
            "odds_ratio": oddsratio,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "p_value": pvalue
        })

    results_df = pd.DataFrame(results)
    results_df["p_adj"] = multipletests(results_df["p_value"], method="fdr_bh")[1]
    results_df["log_odds"] = np.log(results_df["odds_ratio"].replace(0, np.nan))
    results_df = results_df.sort_values(by="log_odds", key=lambda s: s.abs(), ascending=False)

    chi2_result = {"chi2": chi2, "p_value": p, "dof": dof}

    return results_df, chi2_result, standardized_residuals




def perform_chi_square_tests():
    # Total number of females and males
    total_females = 85
    total_males = 172

    # Define the tests and their observed counts for individuals satisfying the condition
    tests = [
        {
            "name": "activity-based+family-ties",
            "female_count": 9,
            "male_count": 21
        },
        {
            "name": "profit-based+family-ties",
            "female_count": 14,
            "male_count": 7
        },
        {
            "name": "family-ties",
            "female_count": 29,
            "male_count": 7
        },
        {
            "name": "activity-based+other-ties",
            "female_count": 35,
            "male_count": 144
        }
    ]

    results = []

    for test in tests:
        a = test["female_count"]
        b = test["male_count"]
        c = total_females - a
        d = total_males - b

        # Create the contingency table
        observed = np.array([[a, b], [c, d]])

        chi2, p, dof, expected = chi2_contingency(observed)

        table = observed.astype(float)
        if (table == 0).any():
            table += 0.5

        odds_ratio, p_value_fisher = fisher_exact(table)
        sm_table = sm.stats.Table2x2(table)
        ci_low, ci_high = sm_table.oddsratio_confint()

        log_odds = np.log(odds_ratio)

        results.append({
            "type": test["name"],
            "female_count": a,
            "male_count": b,
            "odds_ratio": f"{odds_ratio:.6f}",
            "ci_low": f"{ci_low:.6f}",
            "ci_high": f"{ci_high:.6f}",
            "p_value": f"{p:.10e}",
            "p_adj": "",  # Placeholder for adjusted p-value
            "log_odds": f"{log_odds:.6f}"
        })

    # Adjust p-values for multiple comparisons
    p_values = [float(result["p_value"]) for result in results]
    reject, pvals_corrected, _, _ = multipletests(p_values, method='fdr_bh')

    for idx, result in enumerate(results):
        result["p_adj"] = f"{pvals_corrected[idx]:.10e}"

    # Print the results in a table format
    results_table = []
    for result in results:
        results_table.append([
            result["type"],
            result["female_count"],
            result["male_count"],
            result["odds_ratio"],
            result["ci_low"],
            result["ci_high"],
            result["p_value"],
            result["p_adj"],
            result["log_odds"]
        ])

    print("\nResults:")
    print(tabulate(results_table, headers=["type", "female_count", "male_count", "odds_ratio", "ci_low", "ci_high", "p_value", "p_adj", "log_odds"], tablefmt="grid"))

# Call the function to perform the tests and print results





data_prepared = load_and_prepare_data(classification_csv_path)
conting_table = get_gender_type_contingency_table(data_prepared)
print(conting_table)
results_df, chi2_result, standardized_residuals = gender_type_inference(conting_table)
print(results_df)
print(chi2_result)
print(standardized_residuals)

perform_chi_square_tests()




