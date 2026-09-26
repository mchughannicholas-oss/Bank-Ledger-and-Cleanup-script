import csv
import os

def generate_datasets():
    # 1. Messy General Ledger Data (Internal Accounting System Export)
    # Principles tested: Extra whitespace, missing categories, string money fields, mixed dates
    gl_headers = [" Txn Date ", "Account_Code", "Payee Name", "Category", "Debit Amount", "Credit Amount"]
    gl_rows = [
        ["2026-10-01", "5100", " Amazon Mktp ", "Office Supplies", " $45.50 ", "$0.00"],
        ["10/02/2026", " 1010 ", "ATM CASH", "", " $100.00 ", "$0.00"],
        ["2026-10-03", "4000", "Acme Corp ", "Revenue", "$0.00", " $1,500.00 "],
        ["10/05/2026", "5200", "Office Depot", "Office Supplies", " $85.20 ", "$0.00"],
        ["2026-10-06", "5300", "  Digicel Jamaica  ", "Utilities", " $120.00 ", "$0.00"] # Outstanding check
    ]

    # 2. Raw Bank Statement Data (External Bank Feed Export)
    # Principles tested: POS string noise, accounting parenthesis amounts (45.50), date settlement delays, bank service fees
    bank_headers = ["Transaction_Date", "Bank Description", "Amount"]
    bank_rows = [
        ["01/10/2026", "POS PURCHASE - AMAZON MKTPLACE SEATTLE WA #8812", "(45.50)"],
        ["02/10/2026", "ATM WITHDRAWAL - NCB MAIN ST BRANCH", "-100.00"],
        ["03/10/2026", "DIRECT DEP - ACME CORP PAYROLL", "1500.00"],
        ["07/10/2026", "POS CHECKOUT - OFFICE DEPOT #441", "(85.20)"], # Cleared 2 days later
        ["08/10/2026", "BANK SERVICE FEE - MONTHLY MAINT", "-15.00"] # Unrecorded bank fee
    ]

    # Write General Ledger CSV
    with open("dirty_general_ledger.csv", mode="w", newline="", encoding="utf-8") as gl_file:
        writer = csv.writer(gl_file)
        writer.writerow(gl_headers)
        writer.writerows(gl_rows)

    # Write Bank Statement CSV
    with open("raw_bank_statement.csv", mode="w", newline="", encoding="utf-8") as bank_file:
        writer = csv.writer(bank_file)
        writer.writerow(bank_headers)
        writer.writerows(bank_rows)

    print("=" * 60)
    print("✅ SUCCESS: Project datasets generated in your local directory!")
    print(f"   • {os.path.abspath('dirty_general_ledger.csv')}")
    print(f"   • {os.path.abspath('raw_bank_statement.csv')}")
    print("=" * 60)

if __name__ == "__main__":
    generate_datasets()