import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("food_delivery.db")
query = """
SELECT restaurant_name, COUNT(*) order_count, AVG(rating) avg_rating,
       SUM(order_value) total_revenue
FROM orders
GROUP BY restaurant_name
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC
LIMIT 3
"""
df = pd.read_sql_query(query, conn)
df["revenue_share_pct"] = df["total_revenue"] / df["total_revenue"].sum() * 100

plot_df = df.sort_values("avg_rating")
ax = plot_df.plot(x="restaurant_name", y="avg_rating", kind="barh")
for i, value in enumerate(plot_df["avg_rating"]):
    ax.text(value, i, f"{df.iloc[i]['revenue_share_pct']:.1f}%")
plt.show()