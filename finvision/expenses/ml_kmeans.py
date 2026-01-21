import pandas as pd
from sklearn.cluster import KMeans

def user_spending_type():

    # 1. Load dataset
    df = pd.read_csv("dataset.csv")

    # 2. Group by month (total per month)
    monthly_total = df.groupby('month')['amount'].sum().reset_index()

    # 3. Convert to ML format
    X = monthly_total[['amount']]

    # 4. Apply KMeans
    model = KMeans(n_clusters=3, random_state=42)
    model.fit(X)

    # 5. Get cluster labels
    monthly_total['cluster'] = model.labels_

    # 6. Sort clusters by spending
    cluster_mean = (
        monthly_total.groupby('cluster')['amount']
        .mean()
        .sort_values()
    )

    # 7. Map clusters to names
    mapping = {}
    names = ['Saver', 'Balanced', 'Spender']

    for i, cluster_id in enumerate(cluster_mean.index):
        mapping[cluster_id] = names[i]

    # 8. Latest month user type
    latest = monthly_total.iloc[-1]
    user_type = mapping[latest['cluster']]

    return user_type, monthly_total
