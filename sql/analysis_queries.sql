-- ============================================================
-- Customer Sales Analysis Dashboard — KPI & Analytical Queries
-- Author : Dhruv Tandel
-- ============================================================
USE customer_sales_db;

-- 1. EXECUTIVE KPIs
SELECT
    ROUND(SUM(f.revenue), 0)      AS total_revenue,
    COUNT(f.sale_id)              AS total_transactions,
    COUNT(DISTINCT f.customer_id) AS total_customers,
    SUM(f.quantity)               AS total_products_sold
FROM fact_sales f;

-- 2. REVENUE BY GENDER
SELECT
    c.gender,
    COUNT(DISTINCT c.customer_id)                                   AS customer_count,
    ROUND(SUM(f.revenue), 0)                                        AS total_revenue,
    ROUND(SUM(f.revenue)*100.0 / SUM(SUM(f.revenue)) OVER(), 2)    AS revenue_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.gender ORDER BY total_revenue DESC;

-- 3. REVENUE BY AGE GROUP
SELECT
    c.age_group,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    ROUND(SUM(f.revenue), 0)      AS total_revenue,
    SUM(f.quantity)               AS products_sold
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.age_group ORDER BY total_revenue DESC;

-- 4. REVENUE BY PRODUCT CATEGORY
SELECT
    p.category,
    COUNT(f.sale_id)                                                AS transactions,
    SUM(f.quantity)                                                 AS units_sold,
    ROUND(SUM(f.revenue), 0)                                        AS total_revenue,
    ROUND(SUM(f.revenue)*100.0 / SUM(SUM(f.revenue)) OVER(), 2)    AS revenue_share_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category ORDER BY total_revenue DESC;

-- 5. PAYMENT METHOD DISTRIBUTION
SELECT
    pm.payment_method,
    COUNT(f.sale_id)                                                    AS transaction_count,
    ROUND(COUNT(f.sale_id)*100.0 / SUM(COUNT(f.sale_id)) OVER(), 1)    AS pct_of_total
FROM fact_sales f
JOIN dim_payment pm ON f.payment_id = pm.payment_id
GROUP BY pm.payment_method ORDER BY transaction_count DESC;

-- 6. CATEGORY PREFERENCE BY GENDER (CTE crosstab)
WITH base AS (
    SELECT c.gender, p.category, COUNT(f.sale_id) AS txn_count
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    JOIN dim_product  p ON f.product_id  = p.product_id
    GROUP BY c.gender, p.category
)
SELECT category,
    MAX(CASE WHEN gender='Female' THEN txn_count END) AS female_txns,
    MAX(CASE WHEN gender='Male'   THEN txn_count END) AS male_txns
FROM base GROUP BY category ORDER BY (female_txns+male_txns) DESC;

-- 7. STORED PROCEDURE — Parameterised KPI Refresh
DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS sp_kpi_summary(IN p_start DATE, IN p_end DATE)
BEGIN
    SELECT ROUND(SUM(f.revenue),0) AS total_revenue,
           COUNT(f.sale_id)        AS total_transactions,
           COUNT(DISTINCT f.customer_id) AS unique_customers,
           ROUND(AVG(f.revenue),2) AS avg_order_value
    FROM fact_sales f JOIN dim_date d ON f.date_id=d.date_id
    WHERE d.full_date BETWEEN p_start AND p_end;
END $$
DELIMITER ;
-- Usage: CALL sp_kpi_summary('2025-01-01','2025-03-31');
