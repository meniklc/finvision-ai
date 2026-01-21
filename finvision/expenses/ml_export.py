import csv
from .models import Expense

def export_expenses_to_csv():
    expenses = Expense.objects.all()

    with open('dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Header
        writer.writerow(['category', 'amount', 'month'])

        for e in expenses:
            writer.writerow([
                e.category,
                e.amount,
                e.date.strftime("%Y-%m")
            ])

    print("CSV file created successfully!")
