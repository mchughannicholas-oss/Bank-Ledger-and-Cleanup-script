# Import project modules
from pathlib import Path
import pandas as pd
import numpy as np

# Automatically find the folder where this script is saved
script_dir = Path(__file__).resolve().parent

# Load the raw CSV exports (pointing into the data script folder)
general_ledger_df = pd.read_csv(script_dir / "data script" / "dirty_general_ledger.csv")
bank_statement_df = pd.read_csv(script_dir / "data script" / "raw_bank_statement.csv")

# Initial inspection of the datasets
print("--- General Ledger Info ---")
general_ledger_df.info()

print("\n--- Bank Statement Info ---")
bank_statement_df.info()

# Inspect columns and data types
print("\n--- General Ledger Columns ---")
print(general_ledger_df.columns)
print(general_ledger_df.dtypes)

print("\n--- Bank Statement Columns ---")
print(bank_statement_df.columns)
print(bank_statement_df.dtypes)

# 1. Clean Bank Statement Amount
cleaned_amount = (
    bank_statement_df['Amount']
    .astype(str)
    .str.strip()
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.replace('(', '-', regex=False)
    .str.replace(')', '', regex=False)
)
bank_statement_df['Amount'] = pd.to_numeric(cleaned_amount, errors='coerce')

# 2. Clean General Ledger Debit Amount
cleaned_debit = (
    general_ledger_df['Debit Amount']
    .astype(str)
    .str.strip()
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.replace('(', '-', regex=False)
    .str.replace(')', '', regex=False)
)
general_ledger_df['Debit Amount'] = pd.to_numeric(cleaned_debit, errors='coerce')

# 3. Clean General Ledger Credit Amount
cleaned_credit = (
    general_ledger_df['Credit Amount']
    .astype(str)
    .str.strip()
    .str.replace('$', '', regex=False)
    .str.replace(',', '', regex=False)
    .str.replace('(', '-', regex=False)
    .str.replace(')', '', regex=False)
)
general_ledger_df['Credit Amount'] = pd.to_numeric(cleaned_credit, errors='coerce')

# Verify the new data types
print("\n--- After Cleaning Data Types ---")
print("Bank Amount Type:", bank_statement_df['Amount'].dtype)
print("GL Debit Type:", general_ledger_df['Debit Amount'].dtype)
print("GL Credit Type:", general_ledger_df['Credit Amount'].dtype)

# Date parsing and alignment
# Clean column header spaces first
general_ledger_df.columns = general_ledger_df.columns.str.strip()
bank_statement_df.columns = bank_statement_df.columns.str.strip()

# Now parse the dates safely
general_ledger_df['Txn Date'] = pd.to_datetime(general_ledger_df['Txn Date'], errors='coerce', dayfirst=True)
bank_statement_df['Transaction_Date'] = pd.to_datetime(bank_statement_df['Transaction_Date'], errors='coerce')

# Verify data types
print("\n--- Date Parsing Complete ---")
print("GL Txn Date Type:", general_ledger_df['Txn Date'].dtype)
print("Bank Statement Date Type:", bank_statement_df['Transaction_Date'].dtype)

# Text Cleaning & Description Normalization
# --- PHASE 4: Text Cleaning & Description Normalization ---
# Clean General Ledger text columns (Payee Name and Category)
general_ledger_df['Payee Name'] = general_ledger_df['Payee Name'].str.strip().str.upper()
general_ledger_df['Category'] = general_ledger_df['Category'].str.strip().str.upper()

# Clean Bank Statement text column (Bank Description)
bank_statement_df['Bank Description'] = bank_statement_df['Bank Description'].str.strip().str.upper()

# --- Verification ---
print("\n--- Phase 4 Complete: Text Cleaned ---")
print("Sample Cleaned Payees:", general_ledger_df['Payee Name'].head(3).tolist())
print("Sample Cleaned Bank Descriptions:", bank_statement_df['Bank Description'].head(3).tolist())

# --- PHASE 5: Duplicate & Missing Value Management ---

# 1. Check for missing values (NaNs created during cleaning)
print("\n--- Missing Values Count ---")
print("General Ledger Missing Values:\n", general_ledger_df.isna().sum())
print("\nBank Statement Missing Values:\n", bank_statement_df.isna().sum())

# 2. Drop rows where critical columns are missing (e.g., missing date or amount)
general_ledger_df = general_ledger_df.dropna(subset=['Txn Date', 'Debit Amount', 'Credit Amount'])
bank_statement_df = bank_statement_df.dropna(subset=['Transaction_Date', 'Amount'])

# 3. Check for and drop exact duplicate rows
print("\n--- Duplicate Rows Check ---")
print("GL Duplicate Count:", general_ledger_df.duplicated().sum())
print("Bank Statement Duplicate Count:", bank_statement_df.duplicated().sum())

general_ledger_df = general_ledger_df.drop_duplicates()
bank_statement_df = bank_statement_df.drop_duplicates()

print("\n--- Phase 5 Complete: Data Quality Cleaned ---")

# Reconciliation & Ledger Export
# 1. Sort General Ledger chronologically and calculate running balance
general_ledger_df = general_ledger_df.sort_values('Txn Date').reset_index(drop=True)

# Net amount column creation for GL (Credits minus Debits, or adjust based on your sign convention)
general_ledger_df['Net_Amount'] = general_ledger_df['Credit Amount'].fillna(0) - general_ledger_df['Debit Amount'].fillna(0)
general_ledger_df['running_balance'] = general_ledger_df['Net_Amount'].cumsum()

# Format date back to standard string format for export (YYYY-MM-DD)
general_ledger_df['Txn Date'] = general_ledger_df['Txn Date'].dt.strftime('%Y-%m-%d')
bank_statement_df['Transaction_Date'] = bank_statement_df['Transaction_Date'].dt.strftime('%Y-%m-%d')

# 2. Export the final cleaned files
gl_output_path = script_dir / "clean_general_ledger.csv"
bank_output_path = script_dir / "clean_bank_statement.csv"

general_ledger_df.to_csv(gl_output_path, index=False)
bank_statement_df.to_csv(bank_output_path, index=False)

print("\n--- Pipeline Fully Complete! ---")
print(f"Clean General Ledger saved to: {gl_output_path}")
print(f"Clean Bank Statement saved to: {bank_output_path}")

