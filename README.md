# Nova Product Ops & QA Performance Dashboard

A Power BI dashboard analyzing product release delivery, QA bug tracking, and customer satisfaction for a simulated product operations team — modeled on real product/QA operations work I've done professionally.

### Problem
Product teams often can't see, in one place, whether releases are shipping on time, how much QA debt (bugs) is piling up, and whether customers are actually happier as a result. This project builds that single view.

### Data
Synthetic dataset (48 releases, 681 bugs, 238 customer feedback responses, Jan-Dec 2025) generated with Python (generate_data.py) to realistically mirror real product ops patterns (10-20 bugs/release, ~90% on-time delivery, rising satisfaction over time) without using confidential company data.

### Method
Loaded data into SQLite (technova_product_ops.db)
Wrote 8 SQL queries (sql_queries.sql) covering on-time delivery rate, bug volume by severity, resolution time, monthly trends, and satisfaction by region
Built a Power BI dashboard on top of the queried data with KPI cards, trend lines, and an interactive module filter

### Key Findings
Overall on-time delivery rate: 93.8%
Average of ~14 bugs per release; Critical bugs resolved in ~1 day on average vs. ~10 days for Low severity
Customer satisfaction rose from ~3.1/5 to ~4.3/5 over the year

### Screenshot
<img width="647" height="362" alt="image" src="https://github.com/user-attachments/assets/d96e0a8c-b762-4e14-931a-8d54fa3c6544" />

### View Interactive Dashboard
https://www.loom.com/embed/bebe845a16ac4ad3a479a441c106a6b8

### Tools Used
#### SQL (SQLite)
#### Python (pandas, for data generation)
#### Power BI Desktop, 
#### DAX

### Files
#### generate_data.py — synthetic data generator
#### releases.csv, bugs.csv, feedback.csv — raw data
#### technova_product_ops.db — SQLite database
#### sql_queries.sql — analysis queries
#### Nova Product Ops & QA Performance Dashboard.pbix — Power BI file (open in Power BI Desktop)
