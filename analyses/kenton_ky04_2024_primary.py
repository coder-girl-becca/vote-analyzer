"""
Kenton County 2024 Republican Primary, KY-04 (US House District 4)
==================================================================
Vote-method analysis: do candidate vote shares differ across voting methods?

Source: KY State Board of Elections, 2024 Primary Recap Sheets, Kenton County.
URL: https://elect.ky.gov/results/2020-2029/2024ElectionReports/PrimaryRecaps/Kenton%20County.pdf
The recap is precinct-by-precinct. Counts below are raw per-precinct counts for
each KY-04 R candidate by voting method. Methods order in the source PDF is:
[Election Day, Absentee (Mail), Early Excused 6-Day, Early No-Excuse 3-Day,
 Provisional]. Provisional is all-zero in this race and is dropped.

For consistency with prior analyses (Campbell, Kenton General, Boone primary),
counts here are reordered to:
[Mail-in Absentee, Walk-in (6-Day Excused), Early Voting (3-Day No Excuse), Election Day].

Candidates: Michael McGINNIS, Eric DETERS, Thomas MASSIE.

NOTE: The Kenton totals derived here are duplicated as a 4-tuple in
ky04_2024_boone_kenton_aggregate.py for the multi-county aggregation.
If you correct any numbers here, update the aggregate script to match.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from vote_method_analyzer import analyze

# Per-precinct KY-04 R primary counts, in source-PDF order:
# Tuples: (precinct_id, mcginnis_5tuple, deters_5tuple, massie_5tuple)
# Each 5-tuple: [Election Day, Mail, Walk-in (6Day), Early (3Day), Provisional]
# Precincts with 0 votes total in KY-04 R primary (B207 DEC 1.5, B214 IND 6.5,
# C305 EDG 1.5) are omitted.

PRECINCTS_SRC = [
    # A1xx series — Covington area
    ("A101 BRM",      [2,0,0,0,0],    [4,0,0,2,0],   [18,0,0,4,0]),
    ("A102 COV 1",    [5,1,0,1,0],    [10,0,0,0,0],  [25,2,0,2,0]),
    ("A103 COV 2",    [11,1,0,0,0],   [4,0,0,1,0],   [18,0,0,8,0]),
    ("A104 COV 3",    [6,0,0,0,0],    [5,0,0,0,0],   [23,1,0,0,0]),
    ("A105 COV 4",    [1,0,0,0,0],    [3,0,0,0,0],   [16,0,0,0,0]),
    ("A106 COV 5",    [5,0,1,0,0],    [7,0,0,3,0],   [21,3,2,4,0]),
    ("A107 COV 6",    [4,0,0,2,0],    [9,0,0,2,0],   [50,2,1,5,0]),
    ("A108 COV 7",    [6,0,1,2,0],    [4,0,0,1,0],   [28,0,0,4,0]),
    ("A109 COV 8",    [2,0,0,0,0],    [2,0,0,0,0],   [19,4,0,0,0]),
    ("A110 COV 9",    [7,0,0,0,0],    [1,0,0,0,0],   [22,0,0,3,0]),
    ("A111 COV 10",   [0,1,0,0,0],    [0,3,0,0,0],   [6,21,0,2,0]),
    ("A112 COV 11",   [0,0,0,1,0],    [0,0,0,2,0],   [15,0,0,5,0]),
    ("A113 COV 12",   [6,0,0,0,0],    [24,2,0,4,0],  [52,3,0,15,0]),
    ("A114 COV 13",   [6,0,0,2,0],    [15,0,0,1,0],  [48,1,1,12,0]),
    ("A115 COV 14",   [1,0,0,0,0],    [10,0,0,3,0],  [37,0,0,11,0]),
    ("A116 FTM 1",    [3,1,0,5,0],    [9,0,0,3,0],   [46,0,0,9,0]),
    ("A117 FTM 2",    [26,3,1,4,0],   [13,0,0,4,0],  [128,2,0,26,0]),
    ("A118 FTM 3",    [16,4,0,5,0],   [7,0,1,5,0],   [60,1,0,32,0]),
    ("A119 FTW 1",    [30,0,0,12,0],  [28,0,0,2,0],  [185,5,0,24,0]),
    ("A120 FTW 2",    [18,1,0,3,0],   [15,0,0,0,0],  [118,0,1,14,0]),
    ("A121 KV",       [0,0,0,1,0],    [1,0,0,0,0],   [0,0,0,0,0]),
    ("A122 LUD",      [15,0,0,3,0],   [13,0,0,2,0],  [82,2,0,6,0]),
    ("A123 PH",       [25,1,0,1,0],   [4,4,0,1,0],   [114,1,2,7,0]),

    # B2xx series
    ("B201 BRACHT 1", [5,0,0,0,0],    [8,0,0,0,0],   [72,0,0,5,0]),
    ("B202 BRACHT 2", [8,0,0,0,0],    [10,0,0,1,0],  [23,0,0,0,0]),
    ("B203 COV 15",   [3,0,0,6,0],    [3,1,0,4,0],   [37,1,0,12,0]),
    ("B204 COV 16",   [18,0,0,5,0],   [28,1,0,7,0],  [107,1,0,9,0]),
    ("B205 COV 17",   [22,0,0,5,0],   [16,0,0,2,0],  [174,2,2,24,0]),
    ("B206 DEC",      [10,0,0,2,0],   [16,0,0,0,0],  [59,0,0,4,0]),
    ("B208 IND 1",    [20,2,0,13,0],  [60,0,0,9,0],  [221,3,3,57,0]),
    ("B209 IND 2",    [17,0,1,9,0],   [28,1,0,4,0],  [111,2,0,31,0]),
    ("B210 IND 3",    [11,2,0,3,0],   [17,1,0,8,0],  [71,2,0,11,0]),
    ("B211 IND 4",    [20,0,0,6,0],   [16,1,0,2,0],  [107,2,0,27,0]),
    ("B212 IND 5",    [6,0,0,0,0],    [10,0,0,1,0],  [34,3,0,11,0]),
    ("B213 IND 6",    [9,0,0,3,0],    [13,1,0,7,0],  [93,3,1,23,0]),
    ("B215 IND 7",    [23,1,0,7,0],   [24,0,0,9,0],  [133,3,0,42,0]),
    ("B216 IND 8",    [12,0,0,5,0],   [27,0,0,2,0],  [159,4,0,30,0]),
    ("B217 IND 9",    [14,0,0,11,0],  [18,0,1,8,0],  [94,1,1,46,0]),
    ("B218 MGVW",     [6,0,0,2,0],    [18,0,0,5,0],  [61,0,0,15,0]),
    ("B219 NICH 1",   [9,3,0,6,0],    [20,1,1,9,0],  [95,2,0,20,0]),
    ("B220 NICH 2",   [11,0,0,12,0],  [20,0,1,8,0],  [115,4,1,31,0]),
    ("B221 NICH 3",   [21,1,0,4,0],   [29,1,0,7,0],  [158,1,0,41,0]),
    ("B222 PINER",    [16,0,0,3,0],   [10,0,0,0,0],  [80,0,0,6,0]),
    ("B223 TM 1",     [17,2,0,11,0],  [30,0,1,6,0],  [154,2,0,22,0]),
    ("B224 TM 2",     [31,1,2,14,0],  [16,0,0,2,0],  [130,4,1,25,0]),
    ("B225 TM 3",     [6,0,0,1,0],    [3,1,0,2,0],   [43,0,0,9,0]),
    ("B226 WT",       [6,2,0,4,0],    [12,0,0,3,0],  [64,1,0,13,0]),

    # C3xx series
    ("C301 CSP",      [31,0,0,4,0],   [29,0,1,3,0],  [170,3,1,10,0]),
    ("C302 CRH 1",    [22,0,0,2,0],   [18,0,0,2,0],  [106,1,0,14,0]),
    ("C303 CRH 2",    [17,0,0,2,0],   [10,0,0,0,0],  [60,3,0,8,0]),
    ("C304 EDG 1",    [12,0,0,2,0],   [7,0,0,2,0],   [86,1,0,20,0]),
    ("C306 EDG 2",    [23,2,0,7,0],   [11,0,1,4,0],  [141,4,0,15,0]),
    ("C307 EDG 3",    [42,0,1,8,0],   [29,3,0,2,0],  [179,6,1,37,0]),
    ("C308 EDG 4",    [13,1,0,4,0],   [10,0,0,0,0],  [97,3,2,15,0]),
    ("C309 ELS 1",    [5,1,0,0,0],    [8,2,0,0,0],   [59,3,0,1,0]),
    ("C310 ELS 2",    [13,0,0,2,0],   [18,0,1,0,0],  [70,0,0,2,0]),
    ("C311 ELS 3",    [5,0,0,0,0],    [3,0,0,0,0],   [61,2,0,3,0]),
    ("C312 ERL 1",    [14,1,0,5,0],   [18,1,0,4,0],  [104,3,0,17,0]),
    ("C313 ERL 2",    [2,0,0,0,0],    [6,0,0,5,0],   [75,6,0,20,0]),
    ("C314 ERL 3",    [9,0,0,3,0],    [12,8,0,3,0],  [60,11,0,7,0]),
    ("C315 ERL 4",    [18,1,1,4,0],   [32,0,0,5,0],  [163,2,1,14,0]),
    ("C316 ERL 5",    [20,0,0,6,0],   [18,0,0,3,0],  [141,2,0,29,0]),
    ("C317 ERL 6",    [37,1,0,15,0],  [17,2,0,3,0],  [130,13,1,37,0]),
    ("C318 LSP",      [20,4,0,10,0],  [10,0,0,2,0],  [109,3,0,22,0]),
    ("C319 VH 1",     [25,0,0,10,0],  [14,1,0,4,0],  [130,1,3,12,0]),
    ("C320 VH 2",     [24,1,1,2,0],   [17,0,0,0,0],  [109,11,2,15,0]),
    ("C321 VH 3",     [28,2,0,12,0],  [10,3,0,5,0],  [78,1,0,21,0]),
    ("C322 ERL 1.5",  [0,0,0,0,0],    [0,0,0,0,0],   [5,0,0,0,0]),
]

# Reorder source 5-tuples [ED, Mail, 6Day, 3Day, Prov] to analyzer 4-tuples
# [Mail, 6Day, 3Day, ED] (drop Provisional, which is all-zero).
def reorder(src):
    ed, mail, six_day, three_day, _prov = src
    return [mail, six_day, three_day, ed]

PRECINCTS = []
for pid, mc, dt, ma in PRECINCTS_SRC:
    PRECINCTS.append((pid, reorder(mc), reorder(dt), reorder(ma)))

print(f"Number of precincts loaded: {len(PRECINCTS)}")

# Sanity-check: source-tuple Provisional column should be all zero for this race
prov_total = sum(mc[4] + dt[4] + ma[4] for _, mc, dt, ma in PRECINCTS_SRC)
print(f"Provisional total (should be 0): {prov_total}")

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
print("=== Kenton County KY-04 R Primary totals by method ===")
print(f"Methods:           Mail-in, Walk-in, Early,    Election Day")
print(f"McGINNIS:          {mcginnis}  sum={sum(mcginnis)}")
print(f"DETERS:            {deters}   sum={sum(deters)}")
print(f"MASSIE:            {massie}  sum={sum(massie)}")
print(f"Grand total:       {sum(mcginnis)+sum(deters)+sum(massie)}")

# Build inputs for the analyzer
JURISDICTION = "Kenton County, KY"
ELECTION = "2024 Republican Primary — US House District 4 (KY-04)"
SOURCE = (
    "Kentucky State Board of Elections, 2024 Primary Recap Sheets, "
    "Kenton County. "
    "https://elect.ky.gov/results/2020-2029/2024ElectionReports/"
    "PrimaryRecaps/Kenton%20County.pdf"
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

# Second pass: Massie vs combined challenger vote.
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
