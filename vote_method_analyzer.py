"""
Vote-Method Analyzer
====================
Tests whether candidate vote shares differ statistically across voting methods
(mail-in, early in-person, election day, etc.) in a given jurisdiction.

USAGE
-----
1. Fill in the `votes` dict below with raw vote counts per candidate per method.
2. Optionally adjust `two_way_candidates` to specify which two candidates to
   focus pairwise comparisons on (defaults to the two highest vote-getters).
3. Run: python3 vote_method_analyzer.py

Outputs:
  - Raw counts table
  - Percentage breakdown by method
  - Two-way (R vs D) margin table
  - Chi-square test of independence (full table)
  - Chi-square test on two-way subset
  - Pairwise 2x2 chi-square between every method pair (Bonferroni-corrected)
  - Optional: comparison vs. a previous analysis

WHERE TO GET DATA (Kentucky)
----------------------------
- Statewide / per-county totals: KY State Board of Elections live results
    https://vrsws.sos.ky.gov/liveresults/
  Note: only shows combined "Absentee" + "Total" — no method breakdown.

- For full method-level breakdowns, use county clerk cumulative/summary PDFs.
  These typically have columns: Mail-in, Walk-in (excused absentee),
  Early voting (no-excuse), Election Day. Format varies by county.
  Examples:
    Campbell:  https://campbellcountyclerk.ky.gov/wp-content/uploads/2024/11/
               Campbell-County-Cumulative-Results-11-5-2024-10-55-46-PM.pdf
    Kenton:    https://kentoncountykyclerk.com/wp-content/uploads/2024/11/
               24-General-Summary-Report.pdf

- The KY SBE precinct-level "Recap Sheets" have the breakdown but are
  precinct-by-precinct — you'd need to sum across precincts to get county totals.
    https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx

CAVEATS
-------
- Differences across methods reflect SELECTION (who chooses each method),
  not the method causing partisan choice.
- With large n (10K+), trivial differences become "statistically significant."
  Always report effect size (Cramer's V) alongside p-values.
- Drop "Provisional" columns if all-zero or near-zero (sample too small).
- For partial-county congressional districts, county totals overcount slightly.

STATISTICAL APPROACH
--------------------
- Chi-square test of independence: tests H0 that candidate choice is
  independent of method. Robust to large n; assumes expected cell counts >= 5
  (always satisfied here for the major-party candidates).
- Cramer's V: effect size, scale-invariant. 0.1=small, 0.3=medium, 0.5=large.
- Bonferroni correction for pairwise: alpha/k where k = number of pairs.
"""

import numpy as np
import pandas as pd
from scipy import stats
from itertools import combinations


# =============================================================================
# 1. INPUT DATA
# =============================================================================
# Edit these for your analysis. Order of methods is preserved in the output.

JURISDICTION = "Campbell County, KY"
ELECTION = "2024 General — President & VP"
SOURCE = ("Campbell County Clerk Cumulative Results, 11/5/2024 10:55 PM. "
          "https://campbellcountyclerk.ky.gov/wp-content/uploads/2024/11/"
          "Campbell-County-Cumulative-Results-11-5-2024-10-55-46-PM.pdf")

# Methods (column labels) — in the order they should appear
methods = ["Mail-in Absentee", "Walk-in Absentee", "Early Voting", "Election Day"]

# Vote counts: dict mapping candidate name to a list of counts in `methods` order
votes = {
    "Trump (R)":       [1106, 458, 7281, 19605],
    "Harris (D)":      [1343, 311, 5111, 12187],
    "Kennedy (Ind)":   [16,   2,   49,   364],
    "Stein (KY)":      [14,   2,   31,   165],
    "Oliver (Lib)":    [14,   2,   30,   186],
    "Ayyadurai (Ind)": [3,    0,   3,    19],
    "All Write-ins":   [1,    0,   6,    25],
}

# Which two candidates to focus the two-way / pairwise analysis on.
# Set to None to auto-pick the two with highest totals.
two_way_candidates = ["Trump (R)", "Harris (D)"]

# Optional: a comparison dict {method: trump_two_way_pct} from a prior run
# Set to None if not comparing.
comparison_data = None
# Example:
# comparison_data = {
#     "label": "Kenton County",
#     "values": {"Mail-in Absentee": 47.22, "Walk-in Absentee": 59.81,
#                "Early Voting": 59.39, "Election Day": 63.75},
# }


# =============================================================================
# 2. ANALYSIS (no edits needed below)
# =============================================================================

def analyze(jurisdiction, election, source, methods, votes,
            two_way_candidates=None, comparison_data=None):
    """Run the full vote-method analysis. Returns a dict of results."""

    candidates = list(votes.keys())
    arr = np.array([votes[c] for c in candidates])
    df = pd.DataFrame(arr, index=candidates, columns=methods)

    # Auto-pick two-way candidates if not specified
    if two_way_candidates is None:
        totals = df.sum(axis=1).sort_values(ascending=False)
        two_way_candidates = list(totals.index[:2])
    a_name, b_name = two_way_candidates

    print("=" * 80)
    print(f"{jurisdiction} — {election}")
    print(f"Source: {source}")
    print("=" * 80)
    print("\nRaw vote counts:\n")
    print(df.to_string())
    print("\nMethod totals:")
    print(df.sum(axis=0).to_string())
    print(f"\nGrand total: {df.values.sum():,}")

    # Percentages by method
    print("\n" + "=" * 80)
    print("PERCENTAGES BY VOTING METHOD")
    print("=" * 80)
    pct = df.div(df.sum(axis=0), axis=1) * 100
    print(pct.round(2).to_string())

    # Two-way share
    print("\n" + "=" * 80)
    print(f"TWO-WAY SHARE: {a_name} vs {b_name}")
    print("=" * 80)
    two_way = df.loc[[a_name, b_name]]
    two_way_pct = two_way.div(two_way.sum(axis=0), axis=1) * 100
    print(two_way_pct.round(2).to_string())
    margins = two_way_pct.loc[a_name] - two_way_pct.loc[b_name]
    print(f"\n{a_name} margin (pp) by method:")
    print(margins.round(2).to_string())

    # Chi-square: full table
    print("\n" + "=" * 80)
    print(f"CHI-SQUARE: full table ({len(candidates)} candidates × {len(methods)} methods)")
    print("=" * 80)
    print("H0: Candidate choice is independent of voting method")
    chi2, p, dof, _ = stats.chi2_contingency(arr)
    n = arr.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(arr.shape) - 1)))
    print(f"chi-square = {chi2:,.2f}, dof = {dof}, p = {p:.4e}")
    print(f"n = {n:,}, Cramer's V = {cramers_v:.4f}  (0.1=small, 0.3=med, 0.5=large)")

    # Chi-square: two-way only
    print("\n" + "=" * 80)
    print(f"CHI-SQUARE: {a_name} vs {b_name} (2 × {len(methods)} table)")
    print("=" * 80)
    tw_arr = arr[[candidates.index(a_name), candidates.index(b_name)], :]
    chi2_2, p_2, dof_2, _ = stats.chi2_contingency(tw_arr)
    n2 = tw_arr.sum()
    v_2 = np.sqrt(chi2_2 / (n2 * (min(tw_arr.shape) - 1)))
    print(f"chi-square = {chi2_2:,.2f}, dof = {dof_2}, p = {p_2:.4e}")
    print(f"n = {n2:,}, Cramer's V = {v_2:.4f}")

    # Pairwise 2x2
    n_pairs = len(list(combinations(range(len(methods)), 2)))
    bonf_alpha = 0.05 / n_pairs
    print("\n" + "=" * 80)
    print(f"PAIRWISE 2x2 ({a_name} vs {b_name} share, between method pairs)")
    print(f"Bonferroni alpha = 0.05 / {n_pairs} = {bonf_alpha:.5f}")
    print("=" * 80)

    rows = []
    for i, j in combinations(range(len(methods)), 2):
        sub = tw_arr[:, [i, j]]
        chi2_p, p_p, _, _ = stats.chi2_contingency(sub)
        a_i = sub[0, 0] / sub[:, 0].sum() * 100
        a_j = sub[0, 1] / sub[:, 1].sum() * 100
        # Odds ratio with continuity guard
        a, b = sub[0, 0], sub[1, 0]
        c, d = sub[0, 1], sub[1, 1]
        if b * c == 0:
            odds_ratio = float('inf')
        else:
            odds_ratio = (a * d) / (b * c)

        if p_p < bonf_alpha:
            sig = "***"
        elif p_p < 0.05:
            sig = "*"
        else:
            sig = "ns"

        rows.append({
            "Method A": methods[i],
            "Method B": methods[j],
            f"{a_name} % A": round(a_i, 2),
            f"{a_name} % B": round(a_j, 2),
            "Delta (pp)": round(a_i - a_j, 2),
            "Odds ratio": round(odds_ratio, 3) if odds_ratio != float('inf') else "inf",
            "chi2": round(chi2_p, 2),
            "p-value": p_p,
            "Sig": sig,
        })
    pairwise_df = pd.DataFrame(rows)
    print(pairwise_df.to_string(index=False))

    # Optional comparison
    if comparison_data is not None:
        print("\n" + "=" * 80)
        print(f"COMPARISON: {jurisdiction} vs {comparison_data['label']}")
        print("=" * 80)
        comp = pd.DataFrame({
            f"{jurisdiction} {a_name} %": two_way_pct.loc[a_name].round(2),
            f"{comparison_data['label']} {a_name} %":
                pd.Series(comparison_data["values"]),
        })
        comp["Diff (pp)"] = (comp.iloc[:, 0] - comp.iloc[:, 1]).round(2)
        print(comp.to_string())

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    summary_lines = [
        f"Jurisdiction: {jurisdiction}",
        f"Election: {election}",
        f"Total votes (full table): {n:,}",
        f"Total votes ({a_name} + {b_name}): {n2:,}",
        f"",
        f"{a_name} margin (pp) by method:",
    ]
    for m in methods:
        summary_lines.append(f"  {m:25s} {margins[m]:+.1f}")
    summary_lines.extend([
        f"",
        f"Full-table chi-square: p = {p:.2e}, Cramer's V = {cramers_v:.3f}",
        f"Two-way chi-square:    p = {p_2:.2e}, Cramer's V = {v_2:.3f}",
    ])
    print("\n".join(summary_lines))

    return {
        "df": df,
        "pct": pct,
        "two_way_pct": two_way_pct,
        "margins": margins,
        "chi2_full": (chi2, p, dof, cramers_v),
        "chi2_two_way": (chi2_2, p_2, dof_2, v_2),
        "pairwise": pairwise_df,
        "n": n,
        "n_two_way": n2,
    }


if __name__ == "__main__":
    analyze(JURISDICTION, ELECTION, SOURCE, methods, votes,
            two_way_candidates=two_way_candidates,
            comparison_data=comparison_data)
