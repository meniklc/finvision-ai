import pandas as pd

def detect_overspending():

    # Load dataset
    df = pd.read_csv("dataset.csv")

    # Convert month to datetime
    df['month'] = pd.to_datetime(df['month'])

    # Calculate total spending per month
    monthly_total = df.groupby('month')['amount'].sum()

    # Calculate average spending
    avg_spending = monthly_total.mean()

    # Get current month spending (latest)
    current_month = monthly_total.index.max()
    current_spending = monthly_total[current_month]

    # Compare
    if current_spending > avg_spending:
        status = "Overspending"
    else:
        status = "Normal"

    return {
        "average": avg_spending,
        "current": current_spending,
        "status": status
    }
