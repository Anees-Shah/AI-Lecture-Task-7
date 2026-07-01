import csv

def reconcile_books():
    print("--- RECONCILING TEAM OFFSITE TRIP FUNDS ---\n")
    
    # 1. SETUP EXPECTED DATA
    expected_total = 1500.00
    trip_cost_per_person = 150.00
    expected_people = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ian", "Jane"]
    
    # Track who has paid and how much
    payments_received = {person: 0.0 for person in expected_people}
    extra_funds = 0.0 # Money collected for non-trip things (like the raffle)

    # 2. LOAD AND CLEAN THE MESSY DATA
    messy_data = """Date,Sender,Amount,Memo
2023-10-01,Alice Smith,150.00,Offsite trip
2023-10-02,Bob Jones,150.00,
2023-10-03,Charlie B,150.00,Trip fee
2023-10-04,Diana Prince,100.00,Trip partial
2023-10-05,E. Van,150.00,Trip
2023-10-06,Fiona Gallagher,170.00,Trip + Raffle
2023-10-07,George Costanza,150.00,Offsite
2023-10-08,Hannah Abbott,150.00,Trip fund"""

    # Parse the CSV string
    reader = csv.DictReader(messy_data.splitlines())
    
    for row in reader:
        sender = row['Sender'].strip()
        amount = float(row['Amount'].strip())
        memo = row['Memo'].strip().lower()
        
        # APPLY RULE 1: Name matching
        if "E. Van" in sender:
            clean_name = "Evan"
        elif "Alice" in sender: clean_name = "Alice"
        elif "Bob" in sender: clean_name = "Bob"
        elif "Charlie" in sender: clean_name = "Charlie"
        elif "Diana" in sender: clean_name = "Diana"
        elif "Fiona" in sender: clean_name = "Fiona"
        elif "George" in sender: clean_name = "George"
        elif "Hannah" in sender: clean_name = "Hannah"
        else: clean_name = sender # Fallback

        # APPLY RULE 2: Deduct non-trip funds (Raffle)
        if "raffle" in memo:
            amount -= 20.00
            extra_funds += 20.00

        # APPLY RULE 3: Cap trip contribution at $150
        trip_contribution = min(amount, trip_cost_per_person)
        if amount > trip_cost_per_person:
            extra_funds += (amount - trip_cost_per_person)

        # Record the payment
        if clean_name in payments_received:
            payments_received[clean_name] += trip_contribution
        else:
            print(f"WARNING: Unknown person '{clean_name}' paid ${amount}.")

    # 3. CALCULATE THE GAP
    total_collected_for_trip = sum(payments_received.values())
    financial_gap = expected_total - total_collected_for_trip

    print(f"FINANCIAL SUMMARY:")
    print(f" -> Expected Total: ${expected_total:,.2f}")
    print(f" -> Total Trip Funds Collected: ${total_collected_for_trip:,.2f}")
    if extra_funds > 0:
        print(f" -> Extra Non-Trip Funds Collected: ${extra_funds:,.2f}")
    print(f" -> FINANCIAL GAP (Missing): ${financial_gap:,.2f}\n")

    # 4. IDENTIFY WHO TO FOLLOW UP WITH
    print("--- FOLLOW-UP LIST (Who owes money) ---")
    missing_people = []
    
    for person, paid in payments_received.items():
        if paid == 0:
            missing_people.append(f"{person} (Completely missing - owes ${trip_cost_per_person:.2f})")
        elif paid < trip_cost_per_person:
            shortfall = trip_cost_per_person - paid
            missing_people.append(f"{person} (Short payment - owes ${shortfall:.2f})")
            
    if not missing_people:
        print("Everyone has paid! No follow-up needed.")
    else:
        for person in missing_people:
            print(f" -> {person}")

if __name__ == "__main__":
    reconcile_books()