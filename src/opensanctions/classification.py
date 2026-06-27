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



def gender_type_inference(contingency_table, df):
    """
    Perform inferential analysis of gender × type associations.

    Parameters:
        contingency_table: pd.DataFrame
            With columns ['Type', 'Female', 'Male'] as returned by
            get_gender_type_contingency_table().
        df: pd.DataFrame
            The original prepared DataFrame (columns B=gender, C–G=types),
            used to derive true per-gender individual counts.

    Returns:
        results_df: pd.DataFrame
            Type-level odds ratios, CIs, p-values, BH-adjusted p-values,
            log-odds — sorted by |log-odds| descending.
        chi2_result: dict
            Global Pearson chi-square statistics (note: observations are
            not fully independent across types; treat as descriptive).
        standardized_residuals: pd.DataFrame
            Pearson residuals matrix (Type × gender).
    """
    # True unique individual counts per gender — the correct marginals
    n_female = (df["B"] == "female").sum()
    n_male   = (df["B"] == "male").sum()

    ct = contingency_table.set_index("Type")
    matrix = ct[["Female", "Male"]]

    # Global chi-square (descriptive; independence assumption not fully met
    # because one individual can contribute to multiple type rows)
    chi2, p, dof, expected = chi2_contingency(matrix)
    expected_df = pd.DataFrame(expected, index=matrix.index, columns=matrix.columns)
    standardized_residuals = (matrix - expected_df) / np.sqrt(expected_df)

    results = []
    for type_, row in matrix.iterrows():
        a = row["Female"]          # females WITH this type
        c = row["Male"]            # males   WITH this type
        b = n_female - a           # females WITHOUT this type
        d = n_male   - c           # males   WITHOUT this type

        table = np.array([[a, b], [c, d]], dtype=float)
        if (table == 0).any():
            table += 0.5           # Haldane-Anscombe continuity correction

        oddsratio, pvalue = fisher_exact(table)
        sm_table = sm.stats.Table2x2(table)
        ci_low, ci_high = sm_table.oddsratio_confint()

        results.append({
            "type":         type_,
            "female_count": int(a),
            "male_count":   int(c),
            "odds_ratio":   oddsratio,
            "ci_low":       ci_low,
            "ci_high":      ci_high,
            "p_value":      pvalue,
        })

    results_df = pd.DataFrame(results)
    results_df["p_adj"]    = multipletests(results_df["p_value"], method="fdr_bh")[1]
    results_df["log_odds"] = np.log(results_df["odds_ratio"].replace(0, np.nan))
    results_df = results_df.sort_values(
        by="log_odds", key=lambda s: s.abs(), ascending=False
    )

    chi2_result = {"chi2": chi2, "p_value": p, "dof": dof}
    return results_df, chi2_result, standardized_residuals




def perform_chi_square_tests(df, tests):
    """
    Fisher's exact tests for composite type conditions with BH correction.

    Parameters:
        df: pd.DataFrame
            The original prepared DataFrame (columns B=gender, C–G=types).
        tests: list of dict, each with:
            "name"   : str   — label for this comparison
            "mask_fn": callable(df) -> boolean Series
                       — selects rows satisfying the composite condition

    Returns:
        results_df: pd.DataFrame
            One row per test: counts, OR, 95% CI, raw and BH-adjusted p-values,
            log-odds.

    Example
    -------
    tests = [
        {
            "name":    "activity-based+family-ties",
            "mask_fn": lambda df: (df["C"] == 1) & (df["F"] == 1),
        },
        {
            "name":    "profit-based+family-ties",
            "mask_fn": lambda df: (df["D"] == 1) & (df["F"] == 1),
        },
        {
            "name":    "family-ties",
            "mask_fn": lambda df: df["F"] == 1,
        },
        {
            "name":    "activity-based+other-ties",
            "mask_fn": lambda df: (df["C"] == 1) & (df["G"] == 1),
        },
    ]
    """
    # True marginals derived from data, not hard-coded
    n_female = (df["B"] == "female").sum()
    n_male   = (df["B"] == "male").sum()

    results = []
    for test in tests:
        mask       = test["mask_fn"](df)
        sub        = df[mask]
        a          = (sub["B"] == "female").sum()   # females satisfying condition
        c          = (sub["B"] == "male").sum()     # males   satisfying condition
        b          = n_female - a                   # females NOT satisfying condition
        d          = n_male   - c                   # males   NOT satisfying condition

        table = np.array([[a, b], [c, d]], dtype=float)
        if (table == 0).any():
            table += 0.5

        oddsratio, pvalue = fisher_exact(table)
        sm_table          = sm.stats.Table2x2(table)
        ci_low, ci_high   = sm_table.oddsratio_confint()
        log_odds          = np.log(oddsratio)

        results.append({
            "type":         test["name"],
            "female_count": int(a),
            "male_count":   int(c),
            "n_female":     int(n_female),
            "n_male":       int(n_male),
            "odds_ratio":   oddsratio,
            "ci_low":       ci_low,
            "ci_high":      ci_high,
            "p_value":      pvalue,
            "log_odds":     log_odds,
        })

    results_df         = pd.DataFrame(results)
    results_df["p_adj"] = multipletests(results_df["p_value"], method="fdr_bh")[1]

    # print("\nResults:")
    # print(
    #     tabulate(
    #         results_df[
    #             ["type", "female_count", "male_count",
    #              "odds_ratio", "ci_low", "ci_high",
    #              "p_value", "p_adj", "log_odds"]
    #         ].values,
    #         headers=["type", "f_count", "m_count",
    #                  "odds_ratio", "ci_low", "ci_high",
    #                  "p_value", "p_adj", "log_odds"],
    #         tablefmt="grid",
    #         floatfmt=(".0f", ".0f", ".0f",
    #                   ".6f", ".6f", ".6f",
    #                   ".4e", ".4e", ".6f"),
    #     )
    # )
    return results_df
# Call the function to perform the tests and print results





# data_prepared = load_and_prepare_data(classification_csv_path)
# conting_table = get_gender_type_contingency_table(data_prepared)
# print(conting_table)

# results_df, chi2_result, standardized_residuals = gender_type_inference(
#     conting_table, data_prepared          # <-- pass df here
# )
# print(results_df)
# print(chi2_result)
# print(standardized_residuals)

# tests = [
#     {
#         "name":    "activity-based+family-ties",
#         "mask_fn": lambda df: (df["C"] == 1) & (df["F"] == 1),
#     },
#     {
#         "name":    "profit-based+family-ties",
#         "mask_fn": lambda df: (df["D"] == 1) & (df["F"] == 1),
#     },
#     {
#         "name":    "family-ties",
#         "mask_fn": lambda df: df["F"] == 1,
#     },
#     {
#         "name":    "activity-based+other-ties",
#         "mask_fn": lambda df: (df["C"] == 1) & (df["G"] == 1),
#     },
# ]
# perform_chi_square_tests(data_prepared, tests)




