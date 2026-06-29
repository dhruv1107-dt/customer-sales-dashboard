-- ============================================================
-- Customer Sales Analysis Dashboard — Star Schema
-- Author : Dhruv Tandel
-- ============================================================

CREATE DATABASE IF NOT EXISTS customer_sales_db;
USE customer_sales_db;

-- DIMENSION: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id   INT           NOT NULL AUTO_INCREMENT,
    customer_name VARCHAR(100)  NOT NULL,
    gender        ENUM('Male','Female') NOT NULL,
    age           INT           NOT NULL,
    age_group     VARCHAR(20)   NOT NULL,
    PRIMARY KEY (customer_id)
);

-- DIMENSION: Product
CREATE TABLE IF NOT EXISTS dim_product (
    product_id    INT           NOT NULL AUTO_INCREMENT,
    product_name  VARCHAR(100)  NOT NULL,
    category      VARCHAR(50)   NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (product_id)
);

-- DIMENSION: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id    INT  NOT NULL AUTO_INCREMENT,
    full_date  DATE NOT NULL,
    day        INT  NOT NULL,
    month      INT  NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter    INT  NOT NULL,
    year       INT  NOT NULL,
    PRIMARY KEY (date_id),
    UNIQUE KEY uq_date (full_date)
);

-- DIMENSION: Payment
CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id     INT         NOT NULL AUTO_INCREMENT,
    payment_method VARCHAR(50) NOT NULL,
    PRIMARY KEY (payment_id)
);

-- FACT: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id     INT            NOT NULL AUTO_INCREMENT,
    customer_id INT            NOT NULL,
    product_id  INT            NOT NULL,
    date_id     INT            NOT NULL,
    payment_id  INT            NOT NULL,
    quantity    INT            NOT NULL DEFAULT 1,
    unit_price  DECIMAL(10,2)  NOT NULL,
    revenue     DECIMAL(12,2)  NOT NULL,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id)  REFERENCES dim_product(product_id),
    FOREIGN KEY (date_id)     REFERENCES dim_date(date_id),
    FOREIGN KEY (payment_id)  REFERENCES dim_payment(payment_id),
    INDEX idx_customer (customer_id),
    INDEX idx_product  (product_id),
    INDEX idx_date     (date_id)
);
