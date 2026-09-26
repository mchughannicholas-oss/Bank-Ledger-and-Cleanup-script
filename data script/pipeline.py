from pathlib import Path
import pandas as pd
import numpy as np

def main():
    # Automatically get the folder where pipeline.py is located
    script_dir = Path(__file__).resolve().parent

    print("📥 Importing raw CSV datasets into Pandas...\n")

    # Load raw CSV exports using robust paths
    gl_df = pd.read_csv(script_dir / "dirty_general_ledger.csv")
    bank_df = pd.read_csv(script_dir / "raw_bank_statement.csv")

    print("--- 1. Raw General Ledger Export ---")
    print(gl_df.info())
    print("\nFirst 3 rows:")
    print(gl_df.head(3))

    print("\n" + "="*50 + "\n")

    print("--- 2. Raw Bank Statement Export ---")
    print(bank_df.info())
    print("\nFirst 3 rows:")
    print(bank_df.head(3))

if __name__ == "__main__":
    main()