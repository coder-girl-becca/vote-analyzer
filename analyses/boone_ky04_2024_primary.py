"""
Boone County 2024 Republican Primary, KY-04 (US House District 4)
=================================================================
Vote-method analysis: do candidate vote shares differ across voting methods?

Source: KY State Board of Elections, 2024 Primary Recap Sheets, Boone County.
URL: https://elect.ky.gov/results/2020-2029/2024ElectionReports/PrimaryRecaps/Boone%20County.pdf
The recap is precinct-by-precinct (52 precincts). The numbers below are the
raw per-precinct counts for each KY-04 R candidate by voting method, summed
across all precincts to produce Boone County totals. Counts are in order:
[Absentee Mail-in, Absentee Walk-in, Early Voting, Election Day].

Candidates: Michael McGINNIS, Eric DETERS, Thomas MASSIE.
Total ballots cast in the Boone County primary: 14,199.

NOTE: The per-precinct PRECINCTS data below is duplicated in
ky04_2024_boone_kenton_aggregate.py for the multi-county aggregation.
If you correct any numbers here, update the aggregate script to match.
"""
import numpy as np
import pandas as pd
from scipy import stats
from itertools import combinations
import sys, os

# Make sure we can import the analyzer (parent directory of /analyses)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from vote_method_analyzer import analyze

# Per-precinct KY-04 counts: (precinct_id, mcginnis_4tuple, deters_4tuple, massie_4tuple)
# Methods: [Mail-in Absentee, Walk-in Absentee, Early Voting, Election Day]
# Extracted from the recap PDF, one row per precinct (52 precincts total).
PRECINCTS = [
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

# Sanity check: count of precincts (the recap says 52 polling places, but
# there are precincts with both A- and B- prefixes etc.; the recap shows blocks
# only for precincts that had ballots cast in this contest).
print(f"Number of precincts loaded: {len(PRECINCTS)}")

# Sum across all precincts
mcginnis = [0,0,0,0]
deters   = [0,0,0,0]
massie   = [0,0,0,0]
for _, m, d, ma in PRECINCTS:
    for i in range(4):
        mcginnis[i] += m[i]
        deters[i]   += d[i]
        massie[i]   += ma[i]

print()
print("=== Boone County KY-04 Republican Primary totals by method ===")
print(f"Methods:           Mail-in, Walk-in, Early,    Election Day")
print(f"McGINNIS:          {mcginnis}  sum={sum(mcginnis)}")
print(f"DETERS:            {deters}   sum={sum(deters)}")
print(f"MASSIE:            {massie}  sum={sum(massie)}")
print(f"Grand total:       {sum(mcginnis)+sum(deters)+sum(massie)}")

# Build inputs for the analyzer
JURISDICTION = "Boone County, KY"
ELECTION = "2024 Republican Primary — US House District 4 (KY-04)"
SOURCE = (
    "Kentucky State Board of Elections, 2024 Primary Recap Sheets, "
    "Boone County (52 of 52 precincts). "
    "https://elect.ky.gov/results/2020-2029/2024ElectionReports/PrimaryRecaps/Boone%20County.pdf"
)
methods = ["Mail-in Absentee", "Walk-in Absentee", "Early Voting", "Election Day"]
votes = {
    "Massie (Inc.)": massie,
    "Deters":        deters,
    "McGinnis":      mcginnis,
}
two_way_candidates = ["Massie (Inc.)", "Deters"]

analyze(JURISDICTION, ELECTION, SOURCE, methods, votes,
        two_way_candidates=two_way_candidates,
        comparison_data=None)

# Second pass: Massie vs the COMBINED challenger vote.
# In a contested incumbent primary, what often matters strategically is
# Incumbent share vs Anti-Incumbent share.
print("\n\n" + "#" * 80)
print("# SECOND ANALYSIS: Massie (incumbent) vs combined challengers")
print("#" * 80)
combined_challenge = [deters[i] + mcginnis[i] for i in range(4)]
votes2 = {
    "Massie (Inc.)":   massie,
    "Anti-Massie":     combined_challenge,
}
analyze(JURISDICTION, ELECTION + " — Inc. vs combined challenge",
        SOURCE, methods, votes2,
        two_way_candidates=["Massie (Inc.)", "Anti-Massie"],
        comparison_data=None)
