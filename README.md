# 🧾 Sales Warehouse ETL Pipeline

> Multi-File ETL Pipeline with Data Cleaning, Validation, Warehouse Modeling, and PostgreSQL Load.

---

## 👋 What is this?

This script takes three messy sales CSVs (**customers**, **products**, **orders**), cleans them up with pandas, checks they're not broken, merges them into one tidy sales table — complete with a calculated `revenue` column — and loads the result straight into a **PostgreSQL** table. 💰

Read top-to-bottom in a few minutes ⏱️ and you'll see the whole pipeline: extract → transform → validate → build → load.

---

## 🔍 What it actually does

| Function | Job |
|---|---|
| 📥 `extract()` | Reads a CSV into a DataFrame, logs it, returns `None` if the file's missing |
| 🧹 `transform()` | Drops duplicate rows, drops rows with missing values, title-cases `name`/`city`, casts `customer_id` to `int` |
| ✅ `validate()` | Makes sure a DataFrame isn't `None` or empty before you trust it |
| 🏗️ `build_warehouse()` | Merges orders + products + customers → adds `revenue` |
| 🚚 `load()` | Connects to Postgres, creates `sales_warehouse` if needed, inserts every row |
| 🧵 `main()` | Runs the whole extract → transform → validate → build → load chain |

Six functions, one job each. No bloat. 🪶

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
| `orders.csv` | `product_id`, `customer_id`, `quantity` |
| `products.csv` | `product_id`, `price`, `product_name`, `category` |
| `customers.csv` | `customer_id`, `name`, `city` |

Output = one wide table: every order, joined with its product info and customer info, revenue calculated and ready to load. 🎉

---

## 🚀 Usage

### 1. Set up your `.env`

```env
DB_HOST=localhost
DB_NAME=sales_warehouse
DB_USER=your_user
DB_PASSWORD=your_password
```

### 2. Drop your CSVs in the working directory

`main()` reads `customers.csv`, `products.csv`, and `orders.csv` from the current working directory (it prints `os.getcwd()` at startup so you can confirm where it's looking).

### 3. Run it

```bash
python etl_warehouse.py
```

That single call runs the full pipeline and loads `sales_warehouse` into Postgres. If you just want the cleaned DataFrame without touching a database, you can still call the pieces yourself:

```python
from etl_warehouse import extract, transform, validate, build_warehouse

customers = transform(extract('customers.csv'))
products  = transform(extract('products.csv'))
orders    = transform(extract('orders.csv'))

if all(validate(df, name) for df, name in [
    (customers, 'customers.csv'),
    (products, 'products.csv'),
    (orders, 'orders.csv'),
]):
    warehouse = build_warehouse(customers, products, orders)
    print(warehouse.head())
```

---

## 🗄️ What lands in Postgres

`load()` creates this table if it doesn't already exist:

```sql
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
```

It's a single flat table — every order row, fully joined with its customer and product details, plus `revenue`. Rows are inserted one at a time and committed at the end of the run.

---

## 📜 Logging

Every run writes to `etl.log` so you've got receipts 🧾:

```
 2026-06-20 10:42:11 INFO Extracted customers.csv
 2026-06-20 10:42:11 INFO Removed 3 duplicate rows
 2026-06-20 10:42:11 INFO Removed 2 Missing rows
 2026-06-20 10:42:12 INFO Warehouse created with 1247
 2026-06-20 10:42:13 INFO Loaded 1247 rows
```

If a file's missing, `extract()` prints a friendly warning instead of crashing the whole run 🙅 — `validate()` catches it before things go further downstream. If the load fails (bad credentials, connection refused, etc.), the error is caught, printed, and logged rather than crashing the script.

---

## ⚙️ Requirements

```bash
pip install pandas psycopg2-binary python-dotenv
```

Python 3.7+ recommended. You'll also need a running PostgreSQL instance reachable with the credentials in your `.env`.

---

## 📁 Project structure

```
.
├── etl_warehouse.py     # extract, transform, validate, build_warehouse, load, main
├── .env                  # DB_HOST, DB_NAME, DB_USER, DB_PASSWORD (not committed)
├── customers.csv
├── products.csv
├── orders.csv
└── etl.log               # generated on run 📝
```

---

## ⚠️ Known limitations (keepin' it real)

- 🔓 `build_warehouse` assumes clean key columns — unmatched rows quietly vanish on merge (default `how='inner'`) instead of raising a flag.
- 🔎 `validate()` only checks `None`/empty, not whether required columns actually exist.
- 🐌 `load()` inserts row-by-row in a Python loop — fine for learning-project volumes, but a bulk insert (`execute_values`, `COPY`, etc.) would be a lot faster at scale.
- ⭐ The warehouse is a single flat table, not a star schema — there's no `customer_dim` / `product_dim` / `sales_fact` split (see below).
- 🔁 Re-running the script re-inserts everything; there's no upsert/dedupe-on-load, so repeat runs will duplicate rows in `sales_warehouse`.
- 🔐 Credentials come from `.env` via `python-dotenv` — make sure `.env` is in your `.gitignore`.

---

## 🗺️ Possible next steps

- [ ] 🛡️ Schema/column validation in `validate()`
- [ ] 🔀 Configurable join type (inner vs. left) for `build_warehouse`
- [ ] 🩹 Smarter null handling — right now any row with a missing value anywhere is dropped, which can be heavy-handed for large `quantity`/`price` gaps
- [ ] ⚡ Bulk insert / upsert in `load()` instead of row-by-row `INSERT`
- [ ] ⭐ Split the flat table into a proper star schema (`customer_dim`, `product_dim`, `sales_fact`) instead of one wide table
- [ ] 🖥️ CLI entry point (`python etl_warehouse.py --data-dir ./data`) instead of hardcoded filenames in the working directory

---

## 📄 License

MIT — do what you want with it 🤙
