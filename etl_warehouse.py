# Sales Warehouse ETL Pipeline

 

import os
import logging

import pandas as pd
import psycopg2
from dotenv import load_dotenv

# ============================================================

# Configuration & Environment Variables

# ============================================================

logging.basicConfig(
filename="etl.log",
level=logging.INFO,
format=" %(asctime)s %(levelname)s %(message)s "
)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ============================================================

# Extract

# ============================================================

def extract(filename):
try:
df = pd.read_csv(filename)

```
    logging.info(f"Extracted {filename}")
    return df

except FileNotFoundError:
    print(f"{filename} not found")
    return None
```

# ============================================================

# Transform

# ============================================================

def transform(df):

```
if df is None:
    return None

before = len(df)

df = df.drop_duplicates()

logging.info(
    f"Removed {before - len(df)} duplicate rows"
)

before = len(df)

df = df.dropna()

logging.info(
    f"Removed {before - len(df)} Missing rows"
)

if "name" in df.columns:
    df["name"] = df["name"].str.strip().str.title()

if "city" in df.columns:
    df["city"] = df["city"].str.strip().str.title()

if "customer_id" in df.columns:
    df["customer_id"] = df["customer_id"].astype(int)

return df
```

# ============================================================

# Validate

# ============================================================

def validate(df, filename):

```
if df is None:
    return False

if df.empty:
    print(f"{filename} is empty!")
    return False

return True
```

# ============================================================

# Warehouse Builder

# ============================================================

def build_warehouse(customer_df, products_df, orders_df):

```
order_productdf = orders_df.merge(
    products_df,
    on="product_id"
)

full_df = order_productdf.merge(
    customer_df,
    on="customer_id"
)

full_df["revenue"] = (
    full_df["quantity"] * full_df["price"]
)

logging.info(
    f"Warehouse created with {len(full_df)}"
)

return full_df
```

# ============================================================

# Load

# ============================================================

def load(df):

```
try:

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sales_warehouse(
            product_id INTEGER,
            customer_id INTEGER,
            order_id INTEGER,
            quantity INTEGER,
            name VARCHAR(225),
            city VARCHAR(225),
            product_name VARCHAR(225),
            category VARCHAR(225),
            price NUMERIC,
            revenue NUMERIC
        )
        """
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO sales_warehouse(
                product_id,
                customer_id,
                order_id,
                quantity,
                name,
                city,
                product_name,
                category,
                price,
                revenue
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                row["product_id"],
                row["customer_id"],
                row["order_id"],
                row["quantity"],
                row["name"],
                row["city"],
                row["product_name"],
                row["category"],
                row["price"],
                row["revenue"]
            )
        )

    conn.commit()

    cur.close()
    conn.close()

    print("Data loaded successfully!")

    logging.info(
        f"Loaded {len(df)} rows"
    )

except Exception as e:

    print(f"Error {e}")

    logging.error(
        f" Load failed {e}"
    )
```

# ============================================================

# Main Pipeline

# ============================================================

def main():

```
print(os.listdir())
print(os.getcwd())

customers = extract("customers.csv")
products = extract("products.csv")
orders = extract("orders.csv")

customers = transform(customers)
products = transform(products)
orders = transform(orders)

if not validate(customers, "customers.csv"):
    return

if not validate(products, "products.csv"):
    return

if not validate(orders, "orders.csv"):
    return

warehouse = build_warehouse(
    customers,
    products,
    orders
)

load(warehouse)
```

if **name** == "**main**":
main()
