"""
Boone + Kenton 2024 R Primary KY-04 — Multi-county aggregation
==============================================================
Runs the Massie-vs-(Deters+McGinnis) two-way analysis on Boone, then aggregates
Boone + Kenton and runs the same analysis on the pooled data. Also produces a
side-by-side summary table of Massie's share of all KY-04 R votes by method
across the two counties and the aggregate.

This script demonstrates the multi-jurisdiction pooling pattern: when method
effects are small per-county, pooling across counties increases statistical
power to detect (or rule out) consistent method-level differences.

NOTE: This script carries copies of the Boone per-precinct data and the
Kenton per-method totals. If you correct any numbers in
boone_ky04_2024_primary.py or kenton_ky04_2024_primary.py, update the
corresponding data here to match.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from vote_method_analyzer import analyze

# ----------------------------------------------------------------------
# Boone County per-precinct data — KEEP IN SYNC with boone_ky04_2024_primary.py
# Methods order: [Mail, Walk-in, Early, ED].
# ----------------------------------------------------------------------
BOONE_PRECINCTS = [
    ("A102", [0,0,2,6],   [0,0,4,20],  [1,3,7,91]),
    ("A103", [2,0,5,26],  [0,1,5,36],  [1,3,22,198]),
    ("A104", [0,1,4,23],  [0,1,3,27],  [4,4,24,215]),
    ("A105", [0,1,3,22],  [0,0,3,21],  [0,3,6,135]),
    ("A106", [0,1,0,10],  [0,0,0,19],  [1,4,3,80]),
    ("A107", [0,1,1,6],   [0,0,0,7],   [0,1,3,42]),
    ("A108", [0,0,4,21],  [1,0,0,31],  [0,4,16,129]),
    ("A109", [2,0,3,27],  [3,2,2,43],  [2,2,2,115]),
    ("A110", [0,0,2,17],  [0,0,0,32],  [3,4,8,129]),
    ("A111", [0,0,0,24],  [1,0,4,24],  [3,2,16,131]),
    ("A112", [0,1,1,13],  [0,1,2,22],  [3,1,9,85]),
    ("A113", [0,0,3,9],   [0,0,6,19],  [1,2,32,119]),
    ("A114", [4,0,8,37],  [1,0,3,45],  [5,4,33,247]),
    ("A115", [2,0,2,19],  [2,0,0,30],  [4,1,13,157]),
    ("A116", [0,0,4,18],  [0,0,6,15],  [2,0,13,84]),
    ("A117", [0,1,2,44],  [1,0,5,36],  [3,3,20,238]),
    ("A118", [0,1,2,15],  [0,0,0,15],  [3,2,15,209]),
    ("A119", [0,0,0,9],   [0,0,3,9],   [2,0,3,31]),
    ("A120", [1,0,8,30],  [0,0,6,32],  [2,0,22,210]),
    ("A121", [3,0,6,39],  [0,0,5,45],  [2,4,24,217]),
    ("A122", [1,0,1,18],  [0,0,2,18],  [1,0,10,93]),
    ("A123", [2,0,5,17],  [1,0,3,25],  [0,2,12,150]),
    ("B114", [1,0,1,11],  [1,1,0,25],  [1,2,15,159]),
    ("B115", [2,0,0,10],  [0,0,2,15],  [0,2,10,85]),
    ("B118", [0,0,2,12],  [0,0,3,12],  [1,0,8,67]),
    ("B120", [3,0,2,15],  [0,0,2,9],   [6,0,12,118]),
    ("B121", [0,0,5,34],  [0,1,4,40],  [3,3,13,220]),
    ("B122", [0,1,3,25],  [1,0,7,29],  [4,2,24,243]),
    ("B123", [1,0,10,34], [1,1,7,42],  [8,0,20,236]),
    ("B124", [0,0,2,18],  [0,0,2,11],  [0,2,4,94]),
    ("B125", [1,0,1,26],  [1,0,1,25],  [4,3,13,149]),
    ("B126", [0,0,1,17],  [2,0,0,14],  [1,3,8,166]),
    ("B127", [1,1,0,9],   [1,0,0,16],  [3,0,7,109]),
    ("B128", [0,0,0,17],  [0,1,0,34],  [0,1,7,150]),
    ("B129", [2,0,3,25],  [0,0,2,21],  [0,2,20,138]),
    ("B130", [2,1,5,30],  [0,0,3,33],  [2,2,7,145]),
    ("B131", [0,0,6,19],  [2,1,4,16],  [1,1,23,117]),
    ("B132", [0,0,4,20],  [0,0,1,25],  [8,6,13,143]),
    ("B133", [0,0,4,27],  [0,0,3,34],  [1,2,22,162]),
    ("B134", [1,0,2,24],  [0,0,0,15],  [1,1,12,98]),
    ("B135", [2,0,7,47],  [0,0,7,36],  [5,2,17,213]),
    ("B136", [0,0,1,10],  [0,0,0,4],   [1,0,7,67]),
    ("C102", [2,0,0,14],  [0,0,3,22],  [4,0,13,97]),
    ("C110", [2,0,1,13],  [1,1,1,15],  [3,0,14,59]),
    ("C116", [0,0,0,10],  [0,0,1,15],  [0,2,1,60]),
    ("C117", [0,0,1,21],  [0,0,2,14],  [5,1,7,123]),
    ("C118", [0,2,0,16],  [1,0,9,31],  [3,3,19,159]),
    ("C119", [0,0,0,12],  [0,0,3,19],  [0,4,9,67]),
    ("C121", [1,0,2,13],  [0,0,3,10],  [2,0,4,57]),
    ("C123", [0,0,0,5],   [0,0,0,7],   [0,0,2,25]),
    ("C124", [0,0,0,7],   [0,0,3,17],  [0,0,3,60]),
    ("C125", [1,0,0,11],  [0,0,0,16],  [2,0,0,42]),
    ("C126", [1,0,0,1],   [2,0,0,3],   [2,0,2,15]),
    ("C127", [0,0,1,5],   [2,0,0,14],  [2,1,10,74]),
    ("C128", [0,0,1,3],   [0,0,0,13],  [0,1,3,62]),
    ("C129", [0,0,1,15],  [0,0,1,9],   [0,2,3,58]),
    ("C130", [1,0,3,11],  [2,0,1,16],  [4,2,3,95]),
    ("C131", [0,0,1,9],   [0,0,0,14],  [2,0,12,50]),
    ("C132", [0,0,1,4],   [0,0,1,16],  [2,0,8,62]),
    ("C133", [0,0,1,6],   [0,0,0,8],   [0,0,2,33]),
    ("C134", [1,0,2,30],  [1,0,1,28],  [5,2,11,194]),
    ("C135", [0,0,1,10],  [0,1,4,13],  [0,0,6,59]),
    ("C136", [0,0,1,15],  [0,0,0,13],  [1,0,4,69]),
    ("C137", [0,0,3,25],  [0,2,3,26],  [2,0,15,143]),
]
b_mc = [0,0,0,0]; b_dt = [0,0,0,0]; b_ma = [0,0,0,0]
for _, m, d, ma in BOONE_PRECINCTS:
    for i in range(4):
        b_mc[i] += m[i]; b_dt[i] += d[i]; b_ma[i] += ma[i]

# ----------------------------------------------------------------------
# Kenton County per-method totals — KEEP IN SYNC with kenton_ky04_2024_primary.py
# Methods order: [Mail, Walk-in, Early, ED].
# ----------------------------------------------------------------------
k_ma = [168, 27, 1026, 5659]
k_dt = [38, 8, 189, 937]
k_mc = [41, 9, 272, 896]

methods = ["Mail-in Absentee", "Walk-in Absentee", "Early Voting", "Election Day"]
SOURCE_BOTH = (
    "KY SBE 2024 Primary Recap Sheets, Boone County and Kenton County. "
    "https://elect.ky.gov/results/2020-2029/2024ElectionReports/PrimaryRecaps/"
)

# ----------------------------------------------------------------------
# 1) Boone — Massie vs combined challengers
# ----------------------------------------------------------------------
print("#" * 80)
print("# BOONE COUNTY — Massie (Inc.) vs combined challengers (Deters+McGinnis)")
print("#" * 80)
boone_anti = [b_dt[i] + b_mc[i] for i in range(4)]
votes_b = {
    "Massie (Inc.)": b_ma,
    "Anti-Massie":   boone_anti,
}
analyze("Boone County, KY",
        "2024 R Primary — KY-04 — Inc. vs combined challenge",
        SOURCE_BOTH + "Boone%20County.pdf",
        methods, votes_b,
        two_way_candidates=["Massie (Inc.)", "Anti-Massie"],
        comparison_data=None)

# ----------------------------------------------------------------------
# 2) Aggregate Boone + Kenton — Massie vs combined challengers
# ----------------------------------------------------------------------
agg_ma = [b_ma[i] + k_ma[i] for i in range(4)]
agg_dt = [b_dt[i] + k_dt[i] for i in range(4)]
agg_mc = [b_mc[i] + k_mc[i] for i in range(4)]
agg_anti = [agg_dt[i] + agg_mc[i] for i in range(4)]

print("\n\n" + "#" * 80)
print("# AGGREGATE (Boone + Kenton) — Massie vs combined challengers")
print("#" * 80)
votes_agg2 = {
    "Massie (Inc.)": agg_ma,
    "Anti-Massie":   agg_anti,
}
analyze("Boone + Kenton (aggregated), KY",
        "2024 R Primary — KY-04 — Inc. vs combined challenge",
        SOURCE_BOTH + "{Boone,Kenton}%20County.pdf",
        methods, votes_agg2,
        two_way_candidates=["Massie (Inc.)", "Anti-Massie"],
        comparison_data=None)

# Also run the full 3-candidate aggregate to expose McGinnis pattern.
print("\n\n" + "#" * 80)
print("# AGGREGATE (Boone + Kenton) — full 3-candidate table")
print("#" * 80)
votes_agg3 = {
    "Massie (Inc.)": agg_ma,
    "Deters":        agg_dt,
    "McGinnis":      agg_mc,
}
analyze("Boone + Kenton (aggregated), KY",
        "2024 R Primary — KY-04 — full 3-way",
        SOURCE_BOTH + "{Boone,Kenton}%20County.pdf",
        methods, votes_agg3,
        two_way_candidates=["Massie (Inc.)", "Deters"],
        comparison_data=None)

# ----------------------------------------------------------------------
# 3) Side-by-side summary table: Massie share of all votes, by method,
#    in each county and aggregated.
# ----------------------------------------------------------------------
print("\n\n" + "#" * 80)
print("# SIDE-BY-SIDE SUMMARY: Massie share of all KY-04 R votes, by method")
print("#" * 80)
def pcts(ma, anti):
    return [ma[i]/(ma[i]+anti[i])*100 if (ma[i]+anti[i])>0 else float('nan')
            for i in range(4)]
b_pct = pcts(b_ma, boone_anti)
k_pct = pcts(k_ma, [k_dt[i]+k_mc[i] for i in range(4)])
a_pct = pcts(agg_ma, agg_anti)

def n_total(ma, anti):
    return [ma[i]+anti[i] for i in range(4)]
b_n = n_total(b_ma, boone_anti)
k_n = n_total(k_ma, [k_dt[i]+k_mc[i] for i in range(4)])
a_n = n_total(agg_ma, agg_anti)

print(f"\n{'Method':25s} {'Boone n':>9s} {'Boone %':>9s} {'Kenton n':>10s} {'Kenton %':>10s} {'Agg n':>9s} {'Agg %':>9s}")
print("-" * 86)
for i, m in enumerate(methods):
    print(f"{m:25s} {b_n[i]:>9d} {b_pct[i]:>8.2f}  {k_n[i]:>10d} {k_pct[i]:>9.2f}  {a_n[i]:>9d} {a_pct[i]:>8.2f}")

# Also tabulate Election Day vs Early Voting gap in each
print(f"\nElection Day − Early Voting (pp), Massie share of all R votes:")
print(f"  Boone:      {b_pct[3]-b_pct[2]:+.2f}")
print(f"  Kenton:     {k_pct[3]-k_pct[2]:+.2f}")
print(f"  Aggregate:  {a_pct[3]-a_pct[2]:+.2f}")
