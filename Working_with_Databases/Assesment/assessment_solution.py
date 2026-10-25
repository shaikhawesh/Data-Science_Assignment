import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
DB = BASE / "food_delivery.db"

# ---------------- TASK 1 ----------------
def task1():
    np.random.seed(42)
    orders = np.random.randint(100, 801, 30)
    revenue = np.random.uniform(5000, 50001, 30)

    mean = np.mean(orders)
    std = np.std(orders)
    mask = orders > mean + std

    print("TASK 1 - NumPy")
    print("Total orders:", np.sum(orders))
    print("Total revenue:", round(np.sum(revenue), 2))
    print("Mean orders:", round(mean, 2))
    print("Std deviation:", round(std, 2))
    print("Highest revenue day:", np.argmax(revenue) + 1)
    print("Peak-day count:", np.sum(mask))
    print("Peak-day revenue:", round(np.sum(revenue[mask]), 2))
    print("Weekly totals:", orders.reshape(5, 6).sum(axis=1))
    return orders, revenue

# ---------------- TASK 2 ----------------
def dirty_data():
    rows = [
        [1,"Aarav","Spice Hub","North Indian",32,450,4.5],
        [2,"Diya","Pizza Point","Fast Food",28,320,4.1],
        [3,"Rohan","Curry House","North Indian",41,650,4.7],
        [4,"Meera","South Bowl","South Indian",35,280,4.0],
        [5,"Kabir","Biryani Palace","Biryani",45,550,4.3],
        [6,"Isha","Cafe Bliss","Cafe",22,240,3.8],
        [7,"Vivaan","Taco Town","Mexican",38,500,4.2],
        [8,"Anaya","Spice Hub","North Indian",31,420,4.6],
        [9,"Arjun","Pizza Point","Fast Food",29,300,3.9],
        [10,"Sara","Curry House","North Indian",44,720,4.8],
        [11,"Reyansh","South Bowl","South Indian",33,260,4.1],
        [12,"Myra","Biryani Palace","Biryani",49,600,4.4],
        [13,"Aditya","Cafe Bliss","Cafe",25,220,3.7],
        [14,"Kiara","Taco Town","Mexican",36,480,4.0],
        [15,"Dev","Spice Hub","North Indian",None,460,4.5],
        [16,"Tara","Pizza Point","Fast Food",30,None,4.2],
        [17,"Yash","Curry House","North Indian",43,680,None],
        [18,"Nisha","South Bowl",None,34,290,4.0],
        [19,"Om","Biryani Palace","Biryani",52,620,4.5],
        [20,None,"Cafe Bliss","Cafe",24,230,3.6],
    ]
    cols=["order_id","customer_name","restaurant_name","category",
          "delivery_time_mins","order_value","rating"]
    df=pd.DataFrame(rows,columns=cols)
    return pd.concat([df,df.iloc[[0,4,14]]],ignore_index=True)

def task2():
    df=dirty_data()
    print("\nTASK 2 - Data Cleaning")
    print("Nulls before:\n",df.isnull().sum())
    df["delivery_time_mins"]=df["delivery_time_mins"].fillna(df["delivery_time_mins"].median())
    df["order_value"]=df["order_value"].fillna(df["order_value"].median())
    df["rating"]=df["rating"].fillna(round(df["rating"].mean(),1))
    df["category"]=df["category"].fillna(df["category"].mode()[0])
    df["customer_name"]=df["customer_name"].fillna("Unknown")
    print("Nulls after:\n",df.isnull().sum())
    print("Shape before:",df.shape)
    df=df.drop_duplicates().reset_index(drop=True)
    print("Shape after:",df.shape)

    q1=df["order_value"].quantile(.25); q3=df["order_value"].quantile(.75)
    iqr=q3-q1; upper=q3+1.5*iqr; lower=q1-1.5*iqr
    out=df[(df["order_value"]<lower)|(df["order_value"]>upper)]
    print("Outliers:\n",out)
    df["order_value"]=df["order_value"].clip(lower,upper)
    return df

# ---------------- TASK 3 ----------------
def task3(df):
    fig,ax=plt.subplots(2,2,figsize=(14,10))
    sns.countplot(data=df,x="category",hue="category",legend=False,ax=ax[0,0])
    ax[0,0].set(title="Order Count by Category",xlabel="Category",ylabel="Orders")
    sns.boxplot(data=df,x="category",y="delivery_time_mins",hue="category",legend=False,ax=ax[0,1])
    ax[0,1].set(title="Delivery Time by Category",xlabel="Category",ylabel="Minutes")
    avg=df.groupby("restaurant_name")["order_value"].mean().sort_values()
    ax[1,0].barh(avg.index,avg.values)
    ax[1,0].set(title="Average Order Value by Restaurant",xlabel="Average Value",ylabel="Restaurant")
    corr=df[["order_id","delivery_time_mins","order_value","rating"]].corr()
    sns.heatmap(corr,annot=True,ax=ax[1,1])
    ax[1,1].set(title="Numeric Correlation",xlabel="Variable",ylabel="Variable")
    plt.tight_layout()
    out=BASE/"food_delivery_dashboard.png"
    plt.savefig(out,dpi=150,bbox_inches="tight")
    plt.close()
    print("Dashboard saved:",out)

# ---------------- TASK 4 ----------------
def setup_db():
    if DB.exists(): DB.unlink()
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE restaurants(restaurant_id INTEGER PRIMARY KEY,name TEXT,category TEXT,city TEXT)")
    con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY,restaurant_id INTEGER,order_value REAL,delivery_time_mins REAL,rating REAL)")
    restaurants=[
        (1,"Spice Hub","North Indian","Ahmedabad"),(2,"Pizza Point","Fast Food","Ahmedabad"),
        (3,"Curry House","North Indian","Ahmedabad"),(4,"South Bowl","South Indian","Ahmedabad"),
        (5,"Biryani Palace","Biryani","Ahmedabad"),(6,"Cafe Bliss","Cafe","Ahmedabad"),
        (7,"Taco Town","Mexican","Ahmedabad"),(8,"Urban Dine","Multi-Cuisine","Ahmedabad")]
    orders=[
        (1,1,450,32,4.5),(2,1,520,35,4.4),(3,1,390,29,4.2),(4,2,320,28,4.1),
        (5,2,450,31,4.0),(6,2,280,26,3.9),(7,3,650,41,4.7),(8,3,720,44,4.8),
        (9,3,580,39,4.6),(10,4,280,35,4.0),(11,4,310,34,4.1),(12,4,260,33,3.9),
        (13,5,550,45,4.3),(14,5,600,49,4.4),(15,5,620,52,4.5),(16,6,240,22,3.8),
        (17,6,220,25,3.7),(18,6,260,23,3.9),(19,7,500,38,4.2),(20,7,480,36,4.0),
        (21,7,530,37,4.1),(22,8,800,40,4.6),(23,8,750,42,4.5),(24,8,900,45,4.7),
        (25,1,470,30,4.6)]
    con.executemany("INSERT INTO restaurants VALUES(?,?,?,?)",restaurants)
    con.executemany("INSERT INTO orders VALUES(?,?,?,?,?)",orders)
    con.commit()
    return con

def task4(con):
    q="""SELECT r.restaurant_id,r.name,r.category,r.city,
    COUNT(o.order_id) total_orders,SUM(o.order_value) total_revenue,
    ROUND(AVG(o.rating),2) avg_rating
    FROM restaurants r LEFT JOIN orders o ON r.restaurant_id=o.restaurant_id
    GROUP BY r.restaurant_id,r.name,r.category,r.city"""
    df=pd.read_sql_query(q,con).fillna({"total_revenue":0,"avg_rating":0})
    df["revenue_rank"]=df["total_revenue"].rank(ascending=False,method="min").astype(int)
    df=df.sort_values("revenue_rank")
    print("\nTASK 4 - Full report\n",df.to_string(index=False))
    print("\nTOP 5\n",df.head(5).to_string(index=False))
    df.to_csv(BASE/"restaurant_performance_report.csv",index=False)
    return df

# ---------------- SECTION C ----------------
def capstone(cleaned,con):
    q1="""SELECT r.category,COUNT(o.order_id) total_orders,
    ROUND(SUM(o.order_value),2) total_revenue,ROUND(AVG(o.rating),2) avg_rating
    FROM restaurants r JOIN orders o ON r.restaurant_id=o.restaurant_id
    GROUP BY r.category ORDER BY total_revenue DESC"""
    q2="""SELECT r.name,r.city,r.category,COUNT(o.order_id) total_orders,
    ROUND(SUM(o.order_value),2) total_revenue
    FROM restaurants r LEFT JOIN orders o ON r.restaurant_id=o.restaurant_id
    GROUP BY r.restaurant_id,r.name,r.city,r.category"""
    a=pd.read_sql_query(q1,con); b=pd.read_sql_query(q2,con)
    with pd.ExcelWriter(BASE/"food_delivery_report.xlsx",engine="openpyxl") as w:
        cleaned.to_excel(w,sheet_name="Cleaned Data",index=False)
        a.to_excel(w,sheet_name="SQL Category",index=False)
        b.to_excel(w,sheet_name="SQL Restaurant",index=False)
    print("Excel report saved:",BASE/"food_delivery_report.xlsx")

def main():
    _,_=task1()
    df=task2()
    task3(df)
    con=setup_db()
    task4(con)
    capstone(df,con)
    con.close()
    print("\nAll Section B/C files generated successfully.")

if __name__=="__main__":
    main()