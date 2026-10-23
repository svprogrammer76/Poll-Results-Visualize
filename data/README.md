# Input data

The program generates a fictional demo CSV here on its first run. Replace it with a poll export by running `python main.py --input path/to/responses.csv`.

Required CSV columns: `respondent_id`, `response_date`, `question`, `selected_option`, `region`, `age_group`. Options must be Option A, Option B, Option C, or Option D (case and surrounding whitespace are normalized). Keep personal or sensitive information out of public repositories.
