import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

db = Path("food_delivery.db")
if not db.exists():
    print("Error: database file not found.")
else:
    try:
        with sqlite3.connect(db) as conn:
            query = """
            SELECT restaurant_name, COUNT(*) order_count,
                   ROUND(AVG(rating),2) avg_rating,
                   SUM(order_value) total_revenue
            FROM orders
            GROUP BY restaurant_name
            HAVING COUNT(*) >= 5
            ORDER BY avg_rating DESC
            LIMIT 3
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            print("No restaurant has at least 5 orders.")
        else:
            total = df["total_revenue"].sum()
            df["revenue_share_pct"] = 0.0 if total == 0 else df["total_revenue"] / total * 100

            plot_df = df.sort_values("avg_rating").reset_index(drop=True)
            fig, ax = plt.subplots(figsize=(9,5))
            bars = ax.barh(plot_df["restaurant_name"], plot_df["avg_rating"])
            ax.set(title="Top 3 Restaurants by Average Rating",
                   xlabel="Average Customer Rating", ylabel="Restaurant")

            for bar, share in zip(bars, plot_df["revenue_share_pct"]):
                ax.text(bar.get_width()+0.02,
                        bar.get_y()+bar.get_height()/2,
                        f"{share:.1f}% revenue share", va="center")
            plt.tight_layout()
            plt.show()
    except sqlite3.Error as e:
        print(f"Database error: {e}")