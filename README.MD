# Bank Ledger & Data Cleanup Pipeline

A robust, automated data cleaning and reconciliation pipeline built in Python using `pandas`. This tool ingests messy, real-world accounting exports (General Ledgers and Bank Statements), standardizes data types, resolves text and formatting inconsistencies, calculates running balances, and outputs pristine CSV files ready for financial analysis.

---

## Features & Pipeline Phases

1. **Pathing & Ingestion:** Dynamically locates and loads raw CSV datasets using `pathlib` regardless of execution directory.
2. **Amount Standardization:** Strips currency symbols (`$`), commas, and handles accounting negative formats (e.g., parentheses `(100.00)`) to convert text into clean floating-point numbers.
3. **Date Parsing & Alignment:** Converts disparate date columns into true chronological `datetime64` objects and standardizes formatting (`YYYY-MM-DD`).
4. **Text Normalization:** Strips hidden whitespace and normalizes categorical descriptions and payees to uppercase. Fills missing categories with `"UNCATEGORIZED"`.
5. **Data Quality Management:** Scans for missing values (`NaN`) resulting from conversion errors, drops invalid rows, and eliminates exact duplicate entries.
6. **Financial Calculations:** Computes net transaction amounts and generates a cumulative `running_balance` sorted chronologically.
7. **Clean Export:** Exports verified, audit-ready CSV datasets.

---

## Project Structure

```text
Bank Ledger and cleanup script/
│
├── main.py                  # Main execution script
├── requirements.txt         # Project dependencies
└── data script/
    ├── dirty_general_ledger.csv
    ├── raw_bank_statement.csv
    ├── clean_general_ledger.csv  (Generated output)
    └── clean_bank_statement.csv  (Generated output)