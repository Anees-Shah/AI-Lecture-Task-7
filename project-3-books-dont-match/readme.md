I did not have data for this task, so I generated dummy data through AI.


Prompt:I am organizing a Team Offsite Trip for 10 colleagues. The cost is $150 per person, so my known, hand-counted expected total is $1,500.
I have a messy digital payment export from our payment app. The formatting is inconsistent, people use nicknames, and some people bundled other purchases into their trip payment.
Here are my personal rules for interpreting the messy data:
'E. Van' is actually Evan.
If the memo says 'Raffle', subtract $20 from the total amount, because that $20 was for a raffle, not the trip.
Any amount paid above $150 by a single person (after rule adjustments) is considered an overpayment/extra donation, but their trip contribution is capped at $150.




Result: The script acts as an accountant matching a bank statement to a checklist. First, it sets up a checklist of the 10 expected people and initializes their payment to zero. It then reads the messy digital export row by row. For every payment, it applies my personal rules: it translates nicknames (like 'E. Van' to 'Evan'), subtracts money meant for side-bets (like the $20 raffle), and caps the trip contribution at $150, putting any extra money into an 'extra funds' bucket. Finally, it adds up everyone's capped trip contributions, compares that total to my expected $1,500 to find the exact dollar gap, and prints a 'Follow-Up List' showing exactly who hasn't paid in full and how much they still owe

