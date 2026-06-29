# Customer Sales Analysis Dashboard

**Power BI · SQL (MySQL) · Python · Star Schema** | Jan – Mar 2025

A full end-to-end retail analytics project covering 1,000 customers, 2,980 transactions, and ₹2.365M in total revenue. Raw transactional data was modelled into a MySQL star schema, cleansed and validated in Python, and surfaced as a 4-page Power BI executive dashboard with 15+ DAX measures.

---

## Key Findings

| Metric | Value |
|---|---|
| Total Revenue | ₹2.365M |
| Total Transactions | 2,980 |
| Total Customers | 1,000 |
| Top Category | Clothing — ₹1.04M (44% of revenue) |
| Top Gender Segment | Female — ₹1.41M (62% of base) |
| Top Age Cohort | 56–65 — ₹517K |
| Most Used Payment | Cash — 42% |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Database | MySQL 8.0 — Star Schema, Stored Procedures, CTEs, Window Functions |
| ETL & Validation | Python — Pandas, NumPy |
| Visualisation | Power BI — DAX, Power Query, RLS |

---

## Repository Structure

```
customer-sales-dashboard/
├── sql/
│   ├── star_schema.sql
│   └── analysis_queries.sql
├── python/
│   ├── data_validation.py
│   └── etl_pipeline.py
└── README.md
```

---

## How to Run

1. Run `sql/star_schema.sql` in MySQL Workbench
2. Run `python etl_pipeline.py` to load data
3. Open `CustomerSalesDashboard.pbix` in Power BI and refresh
