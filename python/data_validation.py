"""
Customer Sales — Data Validation Pipeline
Author : Dhruv Tandel
Purpose: 3 automated validation routines — null detection, format validation,
         and outlier flagging (Pandas) — run on every ingestion cycle.
"""
import pandas as pd
import numpy as np

VALID_GENDERS         = {"Male", "Female"}
VALID_PAYMENT_METHODS = {"Cash", "Credit Card", "Debit Card"}
VALID_CATEGORIES      = {"Clothing","Shoes","Technology","Cosmetics","Toys","Books","Souvenir","Food & Beverage"}

# ── 1. NULL DETECTION ────────────────────────────────────────
def check_nulls(df, required_cols):
    null_summary = df[required_cols].isnull().sum().reset_index()
    null_summary.columns = ["column", "null_count"]
    null_summary["null_pct"] = (null_summary["null_count"] / len(df) * 100).round(2)
    issues = null_summary[null_summary["null_count"] > 0]
    if not issues.empty:
        print("[WARN] Null values detected:")
        print(issues.to_string(index=False))
    else:
        print("[OK] No null values found.")
    return null_summary

# ── 2. FORMAT / DOMAIN VALIDATION ────────────────────────────
def validate_formats(df):
    issues = {}
    if "gender"         in df.columns:
        bad = df[~df["gender"].isin(VALID_GENDERS)]["gender"].unique().tolist()
        if bad: issues["gender"] = bad
    if "payment_method" in df.columns:
        bad = df[~df["payment_method"].isin(VALID_PAYMENT_METHODS)]["payment_method"].unique().tolist()
        if bad: issues["payment_method"] = bad
    if "category"       in df.columns:
        bad = df[~df["category"].isin(VALID_CATEGORIES)]["category"].unique().tolist()
        if bad: issues["category"] = bad
    if "age"            in df.columns:
        bad_age = df[(df["age"] < 0) | (df["age"] > 120)]
        if not bad_age.empty: issues["age"] = f"{len(bad_age)} rows out of range"
    if issues:
        print("[WARN] Format issues:", issues)
    else:
        print("[OK] All format checks passed.")
    return issues

# ── 3. OUTLIER FLAGGING (IQR) ────────────────────────────────
def flag_outliers(df, numeric_cols, multiplier=1.5):
    outlier_mask = pd.Series(False, index=df.index)
    for col in numeric_cols:
        if col not in df.columns: continue
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - multiplier*iqr, q3 + multiplier*iqr
        col_out = (df[col] < lo) | (df[col] > hi)
        print(f"[{'WARN' if col_out.sum() else 'OK'}] {col}: {col_out.sum()} outlier(s) | bounds [{lo:.2f}, {hi:.2f}]")
        outlier_mask |= col_out
    df = df.copy()
    df["is_outlier"] = outlier_mask
    return df

# ── MASTER RUNNER ─────────────────────────────────────────────
def run_validation(df):
    print("=" * 55)
    required = ["customer_id","gender","age","category","payment_method","quantity","revenue"]
    check_nulls(df, [c for c in required if c in df.columns])
    validate_formats(df)
    df = flag_outliers(df, ["quantity","revenue","age"])
    print(f"  Outliers flagged: {df['is_outlier'].sum()} ({df['is_outlier'].mean()*100:.1f}%)")
    print("=" * 55)
    return df

if __name__ == "__main__":
    df_raw = pd.read_csv("data/raw_sales.csv")
    df_validated = run_validation(df_raw)
    df_clean = df_validated[~df_validated["is_outlier"]]
    df_clean.to_csv("data/clean_sales.csv", index=False)
    print(f"Clean dataset saved — {len(df_clean)} rows.")
