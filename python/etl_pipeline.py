"""
Customer Sales — ETL Pipeline
Author : Dhruv Tandel
Purpose: Extract raw CSV → validate → transform to star-schema tables → load to MySQL 8.0
"""
import pandas as pd
import numpy as np
import mysql.connector
from data_validation import run_validation

DB_CONFIG = {"host":"localhost","database":"customer_sales_db","user":"root","password":"your_password"}
RAW_FILE  = "data/raw_sales.csv"

# ── EXTRACT ──────────────────────────────────────────────────
def extract(filepath):
    df = pd.read_csv(filepath, parse_dates=["date"])
    print(f"[EXTRACT] {len(df)} rows loaded.")
    return df

# ── TRANSFORM — dimension tables ─────────────────────────────
def age_bucket(age):
    if age<18: return "Teen"
    if age<26: return "18-25"
    if age<36: return "26-35"
    if age<46: return "36-45"
    if age<56: return "46-55"
    if age<66: return "56-65"
    return "65+"

def build_dim_customer(df):
    dim = df[["customer_id","customer_name","gender","age"]].drop_duplicates("customer_id").copy()
    dim["age_group"] = dim["age"].apply(age_bucket)
    return dim

def build_dim_product(df):
    return df[["product_id","product_name","category","unit_price"]].drop_duplicates("product_id").copy()

def build_dim_date(df):
    dates = df["date"].drop_duplicates().reset_index(drop=True)
    dim = pd.DataFrame({"full_date": dates})
    dim["day"]        = dim["full_date"].dt.day
    dim["month"]      = dim["full_date"].dt.month
    dim["month_name"] = dim["full_date"].dt.strftime("%B")
    dim["quarter"]    = dim["full_date"].dt.quarter
    dim["year"]       = dim["full_date"].dt.year
    dim.insert(0, "date_id", range(1, len(dim)+1))
    return dim

def build_dim_payment(df):
    methods = df["payment_method"].drop_duplicates().reset_index(drop=True)
    return pd.DataFrame({"payment_id": range(1,len(methods)+1), "payment_method": methods.values})

def build_fact_sales(df, dim_customer, dim_product, dim_date, dim_payment):
    fact = df.copy()
    fact = fact.merge(dim_date[["date_id","full_date"]].rename(columns={"full_date":"date"}), on="date")
    fact = fact.merge(dim_payment, on="payment_method")
    fact["revenue"] = (fact["quantity"] * fact["unit_price"]).round(2)
    return fact[["sale_id","customer_id","product_id","date_id","payment_id","quantity","unit_price","revenue"]]

# ── LOAD ──────────────────────────────────────────────────────
def load(tables):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for table, df in tables.items():
        cols    = ", ".join(df.columns)
        holders = ", ".join(["%s"]*len(df.columns))
        sql     = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({holders})"
        cursor.executemany(sql, [tuple(r) for r in df.itertuples(index=False)])
        print(f"  [LOAD] {cursor.rowcount} rows → {table}")
    conn.commit(); cursor.close(); conn.close()

# ── ORCHESTRATOR ──────────────────────────────────────────────
def run_pipeline():
    df = extract(RAW_FILE)
    df = run_validation(df)
    df = df[~df["is_outlier"]].drop(columns=["is_outlier"])
    load({
        "dim_customer": build_dim_customer(df),
        "dim_product":  build_dim_product(df),
        "dim_date":     build_dim_date(df),
        "dim_payment":  build_dim_payment(df),
        "fact_sales":   build_fact_sales(df, build_dim_customer(df), build_dim_product(df),
                                          build_dim_date(df), build_dim_payment(df)),
    })
    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
