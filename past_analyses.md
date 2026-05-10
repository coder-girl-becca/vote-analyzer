# Past Analyses — Reference Data

This file holds completed vote-method analyses run with `vote_method_analyzer.py`. Use it as reference data for future comparisons or to verify the script reproduces these results.

---

## Campbell County, KY — 2024 General Election, President & VP

**Source:** Campbell County Clerk Cumulative Results Report, 11/5/2024 10:55 PM, 37 of 37 precincts reporting.
**URL:** https://campbellcountyclerk.ky.gov/wp-content/uploads/2024/11/Campbell-County-Cumulative-Results-11-5-2024-10-55-46-PM.pdf
**Total presidential votes:** 48,334

### Raw vote counts

| Candidate       | Mail-in Absentee | Walk-in Absentee | Early Voting | Election Day |
|-----------------|-----------------:|-----------------:|-------------:|-------------:|
| Trump (R)       |            1,106 |              458 |        7,281 |       19,605 |
| Harris (D)      |            1,343 |              311 |        5,111 |       12,187 |
| Kennedy (Ind)   |               16 |                2 |           49 |          364 |
| Stein (KY)      |               14 |                2 |           31 |          165 |
| Oliver (Lib)    |               14 |                2 |           30 |          186 |
| Ayyadurai (Ind) |                3 |                0 |            3 |           19 |
| All Write-ins   |                1 |                0 |            6 |           25 |

### Two-way share (Trump vs Harris)

| Method           | Trump % | Harris % | Trump margin (pp) |
|------------------|--------:|---------:|------------------:|
| Mail-in Absentee |   45.16 |    54.84 |             −9.68 |
| Walk-in Absentee |   59.56 |    40.44 |            +19.12 |
| Early Voting     |   58.76 |    41.24 |            +17.51 |
| Election Day     |   61.67 |    38.33 |            +23.33 |

### Statistical results

| Test                                | chi-square | df |  p-value | Cramer's V |
|-------------------------------------|-----------:|---:|---------:|-----------:|
| Full 7×4 table                      |     374.31 | 18 | 2.05e-68 |      0.051 |
| Trump vs Harris × 4 methods (2×4)   |     269.56 |  3 | 3.84e-58 |      0.075 |

### Pairwise (Trump's two-way share, Bonferroni α = 0.00833)

| Method A         | Method B         | Δ (pp) | p-value   | Significant? |
|------------------|------------------|-------:|-----------|--------------|
| Mail-in Absentee | Walk-in Absentee | −14.40 | 4.30e-12  | ✓            |
| Mail-in Absentee | Early Voting     | −13.59 | 3.43e-35  | ✓            |
| Mail-in Absentee | Election Day     | −16.51 | 3.67e-58  | ✓            |
| Walk-in Absentee | Early Voting     |  +0.80 | 0.689     | ns           |
| Walk-in Absentee | Election Day     |  −2.11 | 0.250     | ns           |
| Early Voting     | Election Day     |  −2.91 | 1.90e-08  | ✓            |

### Key findings

- Mail-in is the only method Harris won.
- Walk-in absentee and Early voting are statistically indistinguishable.
- Election Day is significantly more R-leaning than Early voting (small but precisely measured).

---

## Kenton County, KY — 2024 General Election, President & VP

**Source:** Kenton County Clerk Summary Results Report, 11/5/2024 11:15 PM, 72 of 72 precincts reporting.
**URL:** https://kentoncountykyclerk.com/wp-content/uploads/2024/11/24-General-Summary-Report.pdf
**Total presidential votes:** 80,243

Note: Kenton's report also lists a "Provisional" column, which is all zeros and dropped from this analysis. Column-name mapping: "Absentee (Mail)" → Mail-in; "Early Excused (6Day)" → Walk-in absentee; "Early No Excuse (3Day)" → Early Voting.

### Raw vote counts

| Candidate       | Mail-in Absentee | Walk-in Absentee | Early Voting | Election Day |
|-----------------|-----------------:|-----------------:|-------------:|-------------:|
| Trump (R)       |            2,451 |              494 |       17,657 |       27,147 |
| Harris (D)      |            2,740 |              332 |       12,073 |       15,435 |
| Kennedy (Ind)   |               40 |                3 |          168 |          483 |
| Stein (KY)      |               30 |                2 |          108 |          293 |
| Oliver (Lib)    |               20 |                1 |           90 |          253 |
| Ayyadurai (Ind) |                2 |                1 |           13 |           45 |
| All Write-ins   |               30 |                1 |          118 |          213 |

### Two-way share (Trump vs Harris)

| Method           | Trump % | Harris % | Trump margin (pp) |
|------------------|--------:|---------:|------------------:|
| Mail-in Absentee |   47.22 |    52.78 |             −5.57 |
| Walk-in Absentee |   59.81 |    40.19 |            +19.61 |
| Early Voting     |   59.39 |    40.61 |            +18.78 |
| Election Day     |   63.75 |    36.25 |            +27.50 |

### Statistical results

| Test                                | chi-square | df |   p-value | Cramer's V |
|-------------------------------------|-----------:|---:|----------:|-----------:|
| Full 7×4 table                      |     734.53 | 18 | 2.65e-144 |      0.055 |
| Trump vs Harris × 4 methods (2×4)   |     582.71 |  3 | 5.63e-126 |      0.086 |

### Pairwise (Trump's two-way share, Bonferroni α = 0.00833)

| Method A         | Method B         | Δ (pp) | p-value    | Significant? |
|------------------|------------------|-------:|------------|--------------|
| Mail-in Absentee | Walk-in Absentee | −12.59 | 2.30e-11   | ✓            |
| Mail-in Absentee | Early Voting     | −12.17 | 3.61e-60   | ✓            |
| Mail-in Absentee | Election Day     | −16.54 | 1.36e-118  | ✓            |
| Walk-in Absentee | Early Voting     |  +0.42 | 0.839      | ns           |
| Walk-in Absentee | Election Day     |  −3.95 | 0.0215     | ns (Bonf.)   |
| Early Voting     | Election Day     |  −4.36 | 1.54e-32   | ✓            |

---

## Cross-county comparison (Trump's two-way share)

| Method           | Kenton | Campbell | Difference (Kenton − Campbell, pp) |
|------------------|-------:|---------:|-----------------------------------:|
| Mail-in Absentee |  47.22 |    45.16 |                              +2.06 |
| Walk-in Absentee |  59.81 |    59.56 |                              +0.25 |
| Early Voting     |  59.39 |    58.76 |                              +0.63 |
| Election Day     |  63.75 |    61.67 |                              +2.08 |

The pattern shape is essentially identical: mail-in is the partisan outlier in both counties, in-person early methods cluster together, and Election Day is the most R-leaning. Kenton is ~2 pp more Republican than Campbell at the extremes (mail-in and Election Day) but the gradient between methods is the same.

---

## Notes for future runs

- KY-04 has 17 fully-included counties and 4 partial. Boone is the largest county not yet analyzed and would be a natural third data point — it's the most R-leaning of the three big northern KY counties, so it tests whether the "mail-in is D-leaning" pattern holds in a redder environment.
- Statewide KY 2024 president would also be feasible if all 120 county clerks publish cumulative reports in the same format. The KY SBE precinct recap PDFs have the breakdown but require precinct-level summing.
- For non-presidential races (Senate, House, ballot measures), the same script works — just substitute the relevant rows from the source PDF.
