# Vote-Method Analyzer

A statistical script that tests whether candidate vote shares differ across voting methods (mail-in, early in-person, election day) in a given jurisdiction.

## What it does

Takes a contingency table of votes (candidates × voting methods) and outputs:

- Raw counts and percentage breakdowns
- Two-way (e.g. Trump-vs-Harris) margins by method
- Chi-square test of independence on the full table
- Chi-square test on the two-way subset
- Pairwise 2×2 chi-square between every pair of methods, with Bonferroni correction
- Effect sizes (Cramer's V) — important to look at alongside p-values, since with large n almost any difference becomes "significant"
- Optional side-by-side comparison against a previous analysis

## How to use

1. Open `vote_method_analyzer.py`.
2. Edit the input section (clearly marked):
   - `JURISDICTION`, `ELECTION`, `SOURCE` — descriptive metadata.
   - `methods` — list of voting-method labels in the order you want them.
   - `votes` — dict mapping candidate name to a list of vote counts in `methods` order.
   - `two_way_candidates` — which two candidates to focus pairwise comparison on (or `None` to auto-pick the top two by total).
   - `comparison_data` — optional, for comparing against a previous run.
3. Run: `python3 vote_method_analyzer.py`

Requires `numpy`, `pandas`, `scipy`. No other dependencies.

## How to feed Claude this for a new analysis

In a chat where this script is in the project files, just say something like:

> "Run a vote-method analysis for [county/district] [election year] [race]. Pull the data from the county clerk's cumulative results PDF if available, otherwise the KY State Board of Elections recap sheets."

Claude should be able to fetch the source, transcribe vote counts into the script's input format, run it, and interpret the output.

## Where to find the data (Kentucky)

- **State summary (county totals only, 2-bucket "Absentee" + "Total"):**
  https://vrsws.sos.ky.gov/liveresults/

- **County clerk cumulative/summary PDFs (full method breakdown):** Each county clerk posts these separately and URL formats vary. Search for "[County Name] county clerk Kentucky 2024 cumulative results" to find them. Two confirmed examples:
  - Campbell: `campbellcountyclerk.ky.gov/wp-content/uploads/2024/11/Campbell-County-Cumulative-Results-11-5-2024-10-55-46-PM.pdf`
  - Kenton: `kentoncountykyclerk.com/wp-content/uploads/2024/11/24-General-Summary-Report.pdf`

- **State Board of Elections precinct recap PDFs (2024 General):** Have the breakdown at the precinct level — sum across precincts to get county totals if the county clerk's cumulative file isn't available.
  https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx

## Kentucky-specific notes on voting methods

In 2024 Kentucky reported four distinct voting categories:

- **Absentee Mail-in** — Ballot mailed to voter and returned by mail/dropbox.
- **Absentee Walk-in (Excused, 6-Day)** — In-person voting Oct 23-30 with an excuse (out of county, illness, etc.).
- **Early Voting (No-Excuse, 3-Day)** — In-person voting Oct 31 - Nov 2, no excuse needed.
- **Election Day** — Nov 5 in-person.

Different counties' reports use slightly different column labels for the same categories. The script doesn't care what you call them — just be consistent and document the mapping in `SOURCE`.

## Important interpretive caveats

1. **Statistical significance ≠ substantive significance.** With 50K-80K vote samples, even a 0.5-point difference can be highly significant. Look at the magnitude (Delta pp) and effect size (Cramer's V), not just the p-value.

2. **Selection effects, not method effects.** Any partisan difference across methods reflects *who chose each method*, not the method causing partisan choice. Mail-in voters in 2024 skewed Democratic nationally, but that was a self-selection pattern post-2020.

3. **Partial-county districts.** If your jurisdiction is a congressional district that splits a county, county totals are an over-approximation. Note this in the output.

4. **Uncontested races.** Vote-method differences in uncontested races (e.g. KY-04 House 2024) mostly capture protest-voting / undervote patterns, not partisan preference. Different question, same script.

## Past analyses run with this script

| Jurisdiction | Election | Race | Result summary |
|---|---|---|---|
| Campbell County, KY | 2024 General | President | Mail-in Harris +9.7; Election Day Trump +23.3. Walk-in and Early voting statistically identical. |
| Kenton County, KY | 2024 General | President | Mail-in Harris +5.6; Election Day Trump +27.5. Same shape as Campbell, slightly more R overall. |
