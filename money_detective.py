import pandas as pd

def run_money_detective(file_path):
    print("--- MONEY DETECTIVE: ANALYZING TRANSACTIONS ---\n")
    
    # 1. LOAD AND CLEAN THE DATA
    # We use skipinitialspace=True to handle the space in the " Amount" column header
    df = pd.read_csv(file_path, skipinitialspace=True)
    df.columns = df.columns.str.strip() # Clean column names
    
    # Clean the Amount column: remove quotes, commas, and extra spaces, then convert to float
    df['Amount'] = df['Amount'].astype(str).str.replace('"', '').str.replace(',', '').str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'])
    
    # Parse dates (DD/MM/YYYY format)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    # Separate income and expenses
    expenses = df[df['Amount'] < 0].copy()
    income = df[df['Amount'] > 0].copy()

    # 2. VERIFY BASELINE FIGURES (For your peace of mind)
    total_income = income['Amount'].sum()
    total_expenses = expenses['Amount'].sum()
    net_balance = total_income + total_expenses
    
    print(f"VERIFICATION TOTALS:")
    print(f"Total Income:   ${total_income:,.2f}")
    print(f"Total Expenses: ${total_expenses:,.2f}")
    print(f"Net Balance:    ${net_balance:,.2f}\n")

    # 3. FIND RECURRING CHARGES & DUPLICATES
    # Group by Description and Amount to find identical charges
    grouped = expenses.groupby(['Description', 'Amount']).size().reset_index(name='Count')
    anomalies = grouped[grouped['Count'] > 1].sort_values(by='Count', ascending=False)
    
    print("--- DETECTIVE FINDINGS ---")
    if anomalies.empty:
        print("No recurring charges or duplicates found.")
    else:
        # Define keywords that usually indicate subscriptions
        sub_keywords = ['subscription', 'premium', 'membership', 'bill', 'netflix', 'spotify', 'gym']
        
        for index, row in anomalies.iterrows():
            desc = row['Description']
            amt = row['Amount']
            count = row['Count']
            total_leaked = amt * count
            
            # Check if it's likely a subscription based on keywords
            is_sub = any(keyword in desc.lower() for keyword in sub_keywords)
            category = "SUBSCRIPTION / RECURRING" if is_sub else "REPEATED / DUPLICATE CHARGE"
            
            print(f"[{category}]")
            print(f" -> Merchant: {desc}")
            print(f" -> Amount:   ${amt:,.2f} (Charged {count} times)")
            print(f" -> Total:    ${total_leaked:,.2f}")
            
            # Show the exact dates it occurred
            dates = expenses[(expenses['Description'] == desc) & (expenses['Amount'] == amt)]['Date'].dt.strftime('%d-%b').tolist()
            print(f" -> Dates:    {', '.join(dates)}\n")

if __name__ == "__main__":
    # Run the detective script
    run_money_detective('Wallet-Oct-2023.csv')