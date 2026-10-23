# Poll Results Visualizer

A beginner-friendly, reproducible Python project that cleans poll responses, calculates vote counts and percentages, compares segments, generates charts, and writes plain-language findings. The included demonstration dataset is synthetic and fictional.

## 1. Project explanation

**Simple explanation:** a poll results visualizer turns a spreadsheet of answers into totals, percentages, charts, and a short summary that helps people understand what respondents selected.

**Technical explanation:** it is a small data pipeline that ingests row-level categorical responses, validates and normalizes fields, removes unusable/duplicate records, aggregates counts and within-segment shares, then exports tables, static visualizations, and descriptive insights.

Organizations use this kind of workflow to review election polling, customer feedback, employee satisfaction, product preferences, and classroom or event feedback. The lifecycle is:

`poll data input → preprocessing → analysis → visualization → insights → decision-making`

This demo illustrates the mechanics. It does not estimate election outcomes or claim population representativeness.

## 2. Tech stack options

| Option | Tools | Visuals / dashboard | Difficulty |
|---|---|---|---|
| A — Easy | Python, Pandas, Matplotlib | Static charts; no interactive dashboard | Beginner |
| B — Intermediate (selected) | Python, Pandas, NumPy, Matplotlib, command line | Five saved charts plus CSV and text outputs; dashboard can be added later | Beginner to intermediate |
| C — Advanced | Python, Pandas, Plotly, Streamlit, database/API | Interactive dashboard and live data integration | Intermediate to advanced |

Option B is the best starting point for a student: it is executable with a small dependency list, easy to explain in interviews, and produces reviewable GitHub artifacts without needing a hosted service.

## 3. Architecture

```text
CSV upload or synthetic generator
              │
              ▼
  Validate columns and normalize fields
              │
              ▼
 Clean rows and deduplicate respondents
              │
              ▼
 Counts, shares, region/age comparisons, trend
              │
        ┌─────┴─────────┐
        ▼               ▼
  CSV summary tables   PNG charts
        └─────┬─────────┘
              ▼
       insights.txt + console summary
```

Expected input fields: respondent ID, response date, question, selected option, region, and age group. Processing trims strings, parses dates, standardizes option capitalization, rejects invalid options and missing required fields, and keeps the first row for each respondent-question pair. It calculates overall shares using valid responses as the denominator, and segment shares using each region or age group as its own denominator.

## 4. Phase-wise implementation plan

| Phase | What / why | Expected output | Avoid |
|---|---|---|---|
| 1 Setup | Create a virtual environment and install requirements for isolation | Working Python environment | Installing packages globally by habit |
| 2 Data | Generate the reproducible demo or prepare a CSV with the required schema | `data/poll_responses.csv` or supplied input | Real names/emails in public data |
| 3 Cleaning | Normalize fields, parse dates, remove unusable/duplicate rows | `outputs/cleaned_responses.csv` | Silently accepting invalid categories |
| 4 EDA | Review totals, date range, missing/removed rows and category coverage | Console summary and CSV tables | Treating synthetic patterns as real findings |
| 5 Analysis | Calculate vote counts, shares and segment comparisons | Summary CSVs | Comparing raw segment counts as if group sizes match |
| 6 Visualization | Create bar, pie, stacked segment, and trend charts | Five PNGs | Using pie charts for too many categories |
| 7 Insights | Read the generated leader and segment summaries in context | `outputs/insights.txt` | Claiming causality or representativeness |
| 8 GitHub | Add README, reproducible commands, screenshots, and commits | Public portfolio repository | Uploading secrets or private respondent data |

## 5. Repository structure

```text
Poll-Results-Visualizer/
├── data/             # Demo CSV is generated here; schema/privacy notes
├── notebooks/        # Optional notebooks for exploratory learning
├── src/              # Reusable cleaning, analysis, chart, and insight functions
├── outputs/          # Generated CSV summaries, PNG charts, and insights
├── images/           # Manually captured proof screenshots
├── README.md         # Project, setup, results, and portfolio guide
├── requirements.txt  # Python dependencies
└── main.py           # Command-line entry point
```

## 6. Installation

Use Python 3.10 or newer. From the project folder:

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for that terminal, then activate again. In Command Prompt, activate with `.venv\Scripts\activate.bat`.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 7. Run the project

Generate demo data and all outputs:

```bash
python main.py
```

Use a larger or repeatable synthetic sample:

```bash
python main.py --respondents 1200 --seed 7
```

Analyze a CSV export:

```bash
python main.py --input data/my_poll.csv
```

The input needs columns `respondent_id,response_date,question,selected_option,region,age_group`. Accepted options are Option A, Option B, Option C, and Option D. Use those labels in your CSV, or edit `OPTIONS` in `src/poll_visualizer.py` to match the poll.

## 8. Outputs and virtual simulation

The generator assigns each fictional respondent a date, region, age group, and option. Probabilities vary slightly by segment so the comparison charts are useful to inspect. The seed makes each run reproducible. A small number of rows have extra whitespace or lowercase options to demonstrate cleaning.

The program writes:

- `data/poll_responses.csv` — generated input data (only when no CSV is supplied)
- `outputs/cleaned_responses.csv` — accepted and normalized rows
- `outputs/option_summary.csv` — vote totals and overall shares
- `outputs/region_share.csv` and `outputs/age_group_share.csv` — within-segment percentages
- `outputs/daily_trend.csv` — counts by date and option
- `outputs/option_votes.png` — labeled option count and share bar chart
- `outputs/option_share.png` — overall response share pie chart
- `outputs/region_comparison.png` and `outputs/age_comparison.png` — 100% stacked comparisons
- `outputs/daily_trend.png` — daily counts by option
- `outputs/insights.txt` — generated summary and caveat

Simulation steps: generate fictional respondents → introduce mild regional and age preference differences → add a few formatting issues → normalize and validate → count and divide by valid totals → compare segments and dates → identify the overall leader → write outputs. A leading option is simply the one with the highest valid response count in this dataset.

## 9. Screenshot and proof plan

Capture these after running the program:

1. `data/poll_responses.csv` opened in a spreadsheet (dataset preview).
2. `outputs/cleaned_responses.csv` (cleaned data preview).
3. `outputs/option_summary.csv` (vote/share table).
4. `outputs/option_votes.png` and `outputs/option_share.png`.
5. `outputs/region_comparison.png` and `outputs/age_comparison.png`.
6. `outputs/daily_trend.png` and the final terminal output / `insights.txt`.
7. GitHub repository page showing README and files.

Save screenshots in `images/`, use clear filenames such as `option-votes.png`, and ensure no personal data is visible. The project currently creates static charts; there is no dashboard in this version.

## 10. GitHub upload steps

Suggested repository name: `poll-results-visualizer`  
Description: `A reproducible Python project for cleaning poll responses, comparing vote shares, and generating charts and insights.`  
Topics: `python`, `pandas`, `data-analysis`, `data-visualization`, `survey-analysis`, `portfolio-project`

Create an empty repository on GitHub, then in this folder:

```bash
git init
git add README.md requirements.txt main.py src data/README.md outputs/README.md images/README.md .gitignore
git commit -m "Build poll results analysis pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/poll-results-visualizer.git
git push -u origin main
```

After generating results and reviewing screenshots, add selected screenshots and commit them:

```bash
git add images/
git commit -m "Add project result screenshots"
git push
```

Avoid committing generated respondent data if it contains personal information. A good commit sequence is `Add project structure and setup`, `Add reproducible synthetic poll data`, `Add cleaning and share analysis`, `Add charts and insight report`, `Document usage and add screenshots`.


## 12. Interview preparation

1. **What problem does the project solve?** It turns response-level poll data into validated counts, percentages, segment comparisons, and readable outputs so a reviewer can inspect results quickly.
2. **How do you calculate share?** Overall share is option count divided by all valid responses, multiplied by 100. Segment share uses the segment's valid response count as denominator.
3. **How do you handle bad data?** I check the schema, trim text, normalize option capitalization, parse dates, drop missing/invalid rows, and deduplicate by respondent and question. The pipeline reports retained and removed row counts.
4. **Why include synthetic data?** It makes the project runnable without private survey access and provides a reproducible demonstration. It is explicitly labeled fictional and not used for real-world claims.
5. **What is a limitation of a poll?** Selection and nonresponse bias can make respondents unrepresentative. A large sample alone does not fix a biased sampling method.
6. **Why show percentages by region?** Regional groups may have different sample sizes; within-region shares make option preference patterns easier to compare than raw totals.
7. **What does the trend chart show?** Daily response counts by option over the observed dates. It is descriptive and does not establish why counts changed.
8. **How would you improve this project?** Add configurable question/options, uncertainty intervals, input validation reports, automated data-quality checks, and a Streamlit interface.
9. **How would you protect respondent privacy?** Remove direct identifiers, restrict access to raw data, aggregate small groups, follow consent and retention rules, and never publish confidential exports.
10. **How do you ensure reproducibility?** Pin compatible dependency ranges, use a fixed random seed, document the data schema and command, and keep analysis functions separate from the CLI entry point.

**HR explanation:** “I built a Python poll analysis project that takes survey-style CSV data, cleans and validates responses, compares vote shares by demographic group, and produces charts and a short report. I used fictional reproducible data because I don't have access to enterprise survey data, and I documented the limitations and privacy considerations.”

**Technical explanation:** “The pipeline uses Pandas for schema validation, normalization, deduplication, crosstabs, and group-by aggregation; NumPy generates repeatable categorical samples; Matplotlib exports static charts. Shares use valid response denominators, while the report flags that synthetic and observational patterns are descriptive rather than causal.”

## 13. Future improvements

- Streamlit interactive dashboard with question and segment filters.
- Configurable question/option metadata for multiple polls.
- Sentiment analysis for optional open-ended comments, with privacy review.
- Demographic drill-downs and minimum cell-size safeguards.
- API or live-poll integration with access controls and refresh handling.
- Power BI dashboard fed by the exported summary tables.
- Confidence intervals and weighting for appropriately designed real surveys.

## 14. Troubleshooting

| Error / issue | Fix |
|---|---|
| `python` is not recognized | Install Python 3.10+ and enable PATH, or use `py` on Windows / `python3` on macOS/Linux. |
| `ModuleNotFoundError: pandas` | Activate `.venv`, then run `pip install -r requirements.txt` using that environment's Python. |
| PowerShell activation is blocked | Use the process-scoped execution policy command in the installation section, or use Command Prompt activation. |
| Missing required columns | Rename CSV headers to the six required names listed above. |
| No valid responses remain | Check date parsing, blank fields, duplicate respondent/question rows, and option labels. |
| Charts don't appear in a window | PNG files are saved under `outputs/`; this project uses a non-interactive plotting backend. |
| Shares do not sum to 100 due to rounding | Values are rounded to two decimals; small displayed rounding differences are expected. |

## License and data note

The included generator and sample are for learning. 