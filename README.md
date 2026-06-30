# .ENV

This repository features a fast Python scanner that acts as a strict linter for your environment configuration files. It instantly audits .env, .gitignore, .env.example, and README.md files to verify secrets are kept out of version control and templates are properly formatted.

## How to Use

1. Clone this repository.
2. Ensure you have your local `.env` file set up (copy `.env.example` to `.env` and fill in your actual secrets).
3. Run the scanner to check your project for security leaks and missing configurations:

\`\`\`bash
python scanner.py
\`\`\`

## What it Checks

* **.gitignore:** Ensures your actual environment variable file is ignored and your template is tracked.
* **.env:** Checks for missing values or empty strings.
* **.env.example:** Scans to ensure you didn't accidentally leave a real API key or password in the template.
* **README.md:** Verifies that setup instructions for the environment variables exist.
