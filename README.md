# 🧾 Sales ETL Pipeline[Learning Project]

>  Multi-File ETL Pipeline with Data Validation, Warehouse Modeling, and PostgreSQL Integration Roadmap.

---

## 👋 What is this?

This script takes three messy sales CSVs (**customers**, **products**, **orders**), cleans them up with pandas, checks they're not broken, and merges them into one tidy sales table — complete with a calculated `revenue` column. 💰

No database. No 47 dependencies. Just a script you can read top-to-bottom in **two minutes** ⏱️ and actually understand.

---

## 🔍 What it actually does

| Function | Job |
|---|---|
| 📥 `extract()` | Reads a CSV into a DataFrame, logs it, returns `None` if the file's missing |
| 🧹 `transform()` | Drops duplicate rows, logs how many got the boot |
| ✅ `validate()` | Makes sure a DataFrame isn't `None` or empty before you trust it |
| 🏗️ `build_warehouse()` | Merges orders + products + customers → adds revenue |

That's it. Four functions, one job each. No bloat. 🪶

---

## 🔗 How the merge works

```
🛒 orders ──merge(product_id)──▶ 📦 products ──merge(customer_id)──▶ 👤 customers
                                                                         │
                                                                         ▼
                                                       💵 revenue = quantity × price
```

Your CSVs need these columns or the joins will sulk:

| File | Required column(s) |
|---|---|
| `orders.csv` | `product_id`, `customer_id` |
| `products.csv` | `product_id`, `price` |
| `customers.csv` | `customer_id` |

Output = one wide table: every order, joined with its product info and customer info, revenue calculated and ready to go. 🎉

---

## 🚀 Usage

```python
from etl_warehouse import extract, transform, validate, build_warehouse

# 📥 Extract
customers = extract('data/customers.csv')
products  = extract('data/products.csv')
orders    = extract('data/orders.csv')

# 🧹 Transform (dedupe)
customers = transform(customers)
products  = transform(products)
orders    = transform(orders)

# ✅ Validate before merging
if all(validate(df, name) for df, name in [
    (customers, 'customers.csv'),
    (products, 'products.csv'),
    (orders, 'orders.csv'),
]):
    warehouse = build_warehouse(customers, products, orders)
    print(warehouse.head())
```

---

## 📜 Logging

Every run writes to `etl.log` so you've got receipts 🧾:

```
 2026-06-20 10:42:11 INFO Extracted data/orders.csv 
 2026-06-20 10:42:11 INFO Removed 3 duplicate rows
 2026-06-20 10:42:12 INFO Warehouse created with 1247
```

If a file's missing, `extract()` prints a friendly warning instead of crashing the whole run 🙅 — `validate()` catches it before things go further downstream.

---

## ⚙️ Requirements

```bash
pip install pandas
```

That's genuinely the whole list. 🐍 Python 3.7+ recommended.

---

## 📁 Project structure

```
.
├── etl_warehouse.py    # extract, transform, validate, build_warehouse
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
└── etl.log              # generated on run 📝
```

---

## ⚠️ Known limitations (keepin' it real)

- 🔓 `build_warehouse` assumes clean key columns — unmatched rows quietly vanish on merge (default `how='inner'`) instead of raising a flag.
- 🕳️ No null/type handling yet beyond dedupe — a missing `price` or `quantity` = `NaN` revenue.
- 🚫 No database load step yet — output lives in memory; saving it (CSV/SQL/whatever) is on you for now.
- 🔎 `validate()` only checks `None`/empty, not whether required columns actually exist.

---

## 🗺️ Possible next steps

- [ ] 🛡️ Schema/column validation in `validate()`
- [ ] 🔀 Configurable join type (inner vs. left) for `build_warehouse`
- [ ] 💾 Export step (`to_csv`, `to_sql`, etc.)
- [ ] 🩹 Null handling for `quantity`/`price` before computing revenue
- [ ] 🖥️ CLI entry point (`python etl_warehouse.py --data-dir ./data`)

---

## 🔮 Future plans: turning this into a real warehouse

Right now `build_warehouse()` hands back one flat DataFrame. The dream 💭 is to grow this into a proper **star schema** and actually load it into Postgres — not just merge stuff in memory and call it a day.

### 1️⃣ Split the flat table into fact + dimensions

```
        ⭐ customer_dim          ⭐ product_dim
        ───────────              ───────────
        customer_id PK           product_id PK
        name                     name
        email                    category
        city                     price
              │                        │
              └──────────┬─────────────┘
                          ▼
                   🎯 sales_fact
                   ───────────
                   sale_id PK
                   customer_id FK
                   product_id  FK
                   order_id    FK
                   quantity
                   revenue
                   order_date
```

`customer_dim` and `product_dim` hold the descriptive details; `sales_fact` holds just keys and numbers in the middle. One fact table, dimensions orbiting it like a little solar system ⭐ — that's the "star" in star schema.

### 2️⃣ Add a `load()` function

A fourth step joining `extract` → `transform` → `validate`:

```python
import psycopg2

def load(df, table_name, conn_params):
    """Load a DataFrame into a Postgres table. 🚚"""
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    # bulk insert / upsert logic here
    conn.commit()
    cur.close()
    conn.close()
    logging.info(f'Loaded {len(df)} rows into {table_name}')
```

Planned call pattern:

```python
load(customer_dim, 'customer_dim', conn_params)
load(product_dim, 'product_dim', conn_params)
load(sales_fact, 'sales_fact', conn_params)
```

### 3️⃣ Load target: pgAdmin / PostgreSQL 🐘

Once `load()` lands, the warehouse gets managed through **pgAdmin**, so you'll be able to:
- 👀 Browse `customer_dim`, `product_dim`, and `sales_fact` as real tables
- 🧠 Run SQL joins/aggregations straight in pgAdmin's query tool
- 🔍 Verify row counts and foreign keys after every load

> 🚧 Heads up: none of this — `load()`, the fact/dim split, or the Postgres connection — exists in the code yet. This is the roadmap, not a feature list. Wanted to be upfront about that so nobody clones this expecting a database. 🙏

---

## 📄 License

MIT — do what you want with it 🤙
