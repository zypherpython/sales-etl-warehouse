# 🏢 Sales ETL Warehouse

> *Enterprise-Grade Data Warehouse Platform with Multi-File ETL & Star Schema Integration*

---

## 🚀 Why This Project is NEXT LEVEL

This isn't just an ETL pipeline—it's a **complete data warehouse solution** built for enterprise analytics.

### 📊 How It's Better Than The Last One:

| Feature | Student Pipeline | Sales Warehouse |
|---------|-------------------|------------------|
| **Data Volume** | Single CSV (100 rows) | ✨ **Multiple Large Files** |
| **Processing** | Basic CSV reading | ✨ **Pandas DataFrames** (faster, smarter) |
| **Data Model** | Flat structure | ✨ **Star Schema** (Facts & Dimensions) |
| **Database** | Single table | ✨ **Data Warehouse** (optimized queries) |
| **Joins** | Manual queries | ✨ **Automated Joins** (dimensions linked) |
| **Scalability** | Limited | ✨ **Enterprise-ready** |
| **Analytics** | Basic stats | ✨ **Complex Aggregations** |

---

## 📈 Project Overview

**Sales ETL Warehouse** is a sophisticated data pipeline designed to:
- 📥 **Extract** multiple sales data sources (products, orders, customers, transactions)
- 🔄 **Transform** raw data into a clean, normalized structure using Pandas
- 🏪 **Load** into PostgreSQL as a fully normalized Star Schema warehouse
- 📊 **Enable** powerful analytics through dimensional modeling

### 🎯 Use Case
Perfect for businesses needing:
- Real-time sales analytics
- Customer behavior insights
- Product performance tracking
- Revenue forecasting
- Historical trend analysis

---

## 🏗️ Architecture: Star Schema Data Warehouse

```
                    ┌─────────────────┐
                    │  SALES_FACT     │ (Central Fact Table)
                    │                 │
                    │ • sale_id       │
                    │ • product_id ◄──┼──────┐
                    │ • customer_id ◄─┼──┐   │
                    │ • order_id ◄────┼──┼───┼─┐
                    │ • amount        │  │   │ │
                    │ • quantity      │  │   │ │
                    │ • timestamp     │  │   │ │
                    └─────────────────┘  │   │ │
                           ▲             │   │ │
                 ┌─────────┴─────────┬───┴───┼─┘
                 │                   │       │
         ┌───────▼─────────┐  ┌──────▼──┐  ┌──────▼──────┐
         │ PRODUCT_DIM     │  │CUSTOMER │  │   ORDER_DIM │
         │ (Dimensions)    │  │   _DIM  │  │ (Dimensions)│
         │                 │  │         │  │             │
         │ • product_id ✓  │  │ • cust..│  │ • order_id✓ │
         │ • name          │  │ • name  │  │ • status    │
         │ • category      │  │ • email │  │ • date      │
         │ • price         │  │ • city  │  │ • priority  │
         └─────────────────┘  └─────────┘  └─────────────┘

✨ Benefits:
   - Fast queries through pre-joined tables
   - Easy analysis across dimensions
   - Scalable for millions of records
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|----------|
| **Data Processing** | Pandas | Fast, efficient data manipulation |
| **Data Source** | CSV Files | Multiple input sources |
| **Warehouse DB** | PostgreSQL | Enterprise RDBMS for analytics |
| **Connection** | psycopg2 | Python-PostgreSQL bridge |
| **Language** | Python 3.8+ | Clean, readable code |

---

## 📊 Project Phases

### ✅ Phase 1: Extract (COMPLETED)
- ✨ Multi-file CSV extraction using Pandas
- ✨ Automatic column detection
- ✨ Data profiling and validation
- ✨ Error handling & logging

**Status:** Ready for production

---

### 🔄 Phase 2: Transform (IN PROGRESS - COMING SOON!)
Will include:
- Data cleaning & deduplication
- Dimension table creation
- Fact table aggregation
- Data quality checks
- Business logic implementation

**Timeline:** Coming in next update ⏰

---

### 📦 Phase 3: Load & Warehouse (UPCOMING)
Will include:
- PostgreSQL Star Schema creation
- Bulk data loading with transactions
- Constraint management
- Incremental updates (SCD Type 2)
- Data warehouse optimization

**Timeline:** Phase 3 coming soon! 🚀

---

## 🎯 Key Features

### Extract Phase ⚡
```python
✨ Multi-file support
✨ Pandas-powered processing  
✨ Automatic column detection
✨ Data profiling & stats
✨ Robust error handling
```

### Transform Phase 🔄 (Coming Soon)
```python
✨ Data cleaning & normalization
✨ Duplicate removal
✨ Null value handling
✨ Type conversion & validation
✨ Business rule application
```

### Load Phase 📦 (Coming Soon)
```python
✨ Star Schema creation
✨ Fact table loading
✨ Dimension table management
✨ Incremental updates
✨ Data warehouse optimization
```

---

## 💻 Getting Started

### Prerequisites
```bash
Python 3.8+
PostgreSQL 12+
Pandas
psycopg2
```

### Installation
```bash
# Clone the repository
git clone https://github.com/zypherpython/sales-etl-warehouse.git
cd sales-etl-warehouse

# Install dependencies
pip install pandas psycopg2-binary
```

### Quick Start
```python
from etl_warehouse import extract, transform, load

# Extract sales data from multiple files
products = extract('data/products.csv')
customers = extract('data/customers.csv')
orders = extract('data/orders.csv')

# Transform data
clean_products = transform(products)
clean_customers = transform(customers)
clean_orders = transform(orders)

# Load to warehouse (coming in Phase 3)
load(clean_products, 'product_dim')
load(clean_customers, 'customer_dim')
load(clean_orders, 'sales_fact')
```

---

## 📁 Project Structure

```
sales-etl-warehouse/
├── etl_warehouse.py          # Main ETL pipeline
├── data/                     # Sample datasets
│   ├── products.csv
│   ├── customers.csv
│   ├── orders.csv
│   └── transactions.csv
├── README.md                 # This file
├── requirements.txt          # Dependencies
└── docs/
    ├── SCHEMA.md             # Star schema documentation
    ├── ROADMAP.md            # Development roadmap
    └── PERFORMANCE.md        # Benchmarks (coming soon)
```

---

## 🔬 Data Warehouse Schema

### Fact Table: SALES_FACT
```sql
CREATE TABLE sales_fact (
    sale_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product_dim(product_id),
    customer_id INT REFERENCES customer_dim(customer_id),
    order_id INT REFERENCES order_dim(order_id),
    amount DECIMAL(10, 2),
    quantity INT,
    timestamp TIMESTAMP
);
```

### Dimension Table: PRODUCT_DIM
```sql
CREATE TABLE product_dim (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2)
);
```

*(More dimensions coming in Phase 2)*

---

## 📊 Performance & Scalability

**Designed for enterprise scale:**
- ✨ Handles millions of records
- ✨ Optimized indexes for fast queries
- ✨ Batch processing capabilities
- ✨ Incremental update support
- ✨ Compression & partitioning ready

---

## 🎓 Learning Path

This project teaches:
- 📚 ETL pipeline architecture
- 📚 Data warehouse design (Star Schema)
- 📚 Pandas for data manipulation
- 📚 PostgreSQL database design
- 📚 Python database integration
- 📚 Dimensional modeling
- 📚 Data quality & validation

---

## 🗺️ Development Roadmap

### Phase 1: Extract ✅
- [x] Multi-file CSV extraction
- [x] Pandas DataFrame handling
- [x] Error handling & logging

### Phase 2: Transform 🔄
- [ ] Data cleaning functions
- [ ] Dimension table creation
- [ ] Data validation framework
- [ ] Business logic implementation

### Phase 3: Load 📦
- [ ] PostgreSQL Star Schema
- [ ] Fact table loading
- [ ] Dimension table management
- [ ] Incremental updates

### Phase 4: Analytics 📈
- [ ] Sample queries
- [ ] Aggregation views
- [ ] Performance dashboards
- [ ] Reporting examples

### Phase 5: Advanced Features 🚀
- [ ] Real-time data ingestion
- [ ] Data quality monitoring
- [ ] Automated scheduling
- [ ] API for warehouse access

---

## 🤝 Contributing

This is a **learning project**, but contributions are welcome!
- 💡 Suggestions for improvements
- 🐛 Bug reports
- 📖 Documentation enhancements
- 🎯 Feature ideas
- ⭐ Feedback & reviews

---

## Acknowledgments

| Contributor | Role |
|-------------|------|
| zypherpython | Project Lead & Developer |
| Copilot | Architecture & Documentation |

---

## 📝 License

Open source under MIT License - See LICENSE file for details

---

## 🎯 Why This Matters

**Data warehouses are the backbone of modern analytics.**

This project demonstrates how to build enterprise-grade solutions that handle:
- Complex data relationships
- Multi-source integration  
- Scalable architecture
- High-performance queries
- Real business insights

Perfect for learning **real-world data engineering** at scale! 🚀

---

<div align="center">
  <h3>🌟 Ready to Transform Data into Decisions? 🌟</h3>
  <br/>
  <p><strong>From Raw Data to Intelligent Insights</strong></p>
  <br/>
  <p>⏰ <strong>Stay tuned for Phase 2 & Phase 3 updates!</strong></p>
  <br/>
  <p><em>Enterprise-grade data warehousing starts here 📊</em></p>
</div>
