import sqlite3
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
from scipy.stats import chi2_contingency
from opensanctions.const import persons_sub_db_path



def get_gender_topic_contingency_table():
    """
    Returns Gender × Topic contingency table for sanctioned individuals.

    Output:
        pandas.DataFrame with columns:
            Topics | female | male
    """

    conn = sqlite3.connect(persons_sub_db_path)
    cursor = conn.cursor()

    query = """
        WITH
        sanctioned_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics'
              AND value IN ('sanction', 'sanction.counter')
        ),

        other_topics_individuals AS (
            SELECT DISTINCT canonical_id
            FROM persons_topics
            WHERE prop = 'topics'
              AND value NOT IN ('sanction', 'sanction.counter')
        ),

        valid_individuals AS (
            SELECT canonical_id FROM sanctioned_individuals
            INTERSECT
            SELECT canonical_id FROM other_topics_individuals
        ),

        gender_data AS (
            SELECT p.canonical_id, p.value AS gender
            FROM persons_topics p
            JOIN valid_individuals v
              ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'gender'
        ),

        topics_data AS (
            SELECT p.canonical_id, p.value AS topics
            FROM persons_topics p
            JOIN valid_individuals v
              ON p.canonical_id = v.canonical_id
            WHERE p.prop = 'topics'
        )

        SELECT
            t.topics,
            g.gender,
            COUNT(DISTINCT g.canonical_id) AS count
        FROM gender_data g
        JOIN topics_data t
          ON g.canonical_id = t.canonical_id
        GROUP BY t.topics, g.gender
        ORDER BY t.topics;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(results, columns=["Topics", "Gender", "Count"])

    # Pivot → contingency table
    contingency = (
        df.pivot(index="Topics", columns="Gender", values="Count")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    # Ensure consistent column naming
    contingency = contingency.rename(
        columns={
            "female": "female_count",
            "male": "male_count"
        }
    )

    #return contingency
    return contingency


def gender_topic_inference(contingency_table):
    """
    Perform inferential analysis of gender × topic associations.

    Parameters:
        contingency_table: pd.DataFrame
            Index = Topics, columns = ['female_count', 'male_count']

    Returns:
        results_df: pd.DataFrame
            Topic-level odds ratios, confidence intervals, p-values, adjusted p-values, log-odds
        chi2_result: dict
            Global chi-square statistics
        standardized_residuals: pd.DataFrame
            Matrix of standardized residuals
    """
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm
    from scipy.stats import chi2_contingency, fisher_exact
    from statsmodels.stats.multitest import multipletests

    ct = contingency_table.set_index("Topics")
    matrix = ct[["female_count", "male_count"]]

    chi2, p, dof, expected = chi2_contingency(matrix)
    expected_df = pd.DataFrame(expected, index=matrix.index, columns=matrix.columns)
    standardized_residuals = (matrix - expected_df) / np.sqrt(expected_df)

    total_female = matrix["female_count"].sum()
    total_male = matrix["male_count"].sum()

    results = []
    for topic, row in matrix.iterrows():
        a = row["female_count"]
        c = row["male_count"]
        b = total_female - a
        d = total_male - c

        table = np.array([[a, b], [c, d]], dtype=float)
        if (table == 0).any():
            table += 0.5

        oddsratio, pvalue = fisher_exact(table)
        sm_table = sm.stats.Table2x2(table)
        ci_low, ci_high = sm_table.oddsratio_confint()

        results.append({
            "topic": topic,
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






# Given sanctioned individuals, is the probability of being associated with a specific topic different between females and males?

# odds(topic | female)vs odds(topic | male)


# role.rca
# female_count = 115
# male_count   = 202
# odds_ratio   = 3.86
# CI = [3.06, 4.86]
# p_adj ≈ 1.18e-24

# Interpretation:

# Females have 3.86× higher odds than males of appearing in role.rca.

# Confidence interval excludes 1 → effect is statistically reliable.

# Extremely small adjusted p-value → survives multiple testing.

# ✅ Strong female overrepresentation.