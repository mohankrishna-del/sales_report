import os
import sys

# --- imports with helpful error messages ---
try:
    import pandas as pd
except ImportError:
    print("Pandas is not installed. Install: python -m pip install pandas")
    sys.exit(1)

try:
    import matplotlib
    # use non-interactive backend so plt.show() won't fail on headless systems
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("Matplotlib is not installed. Install: python -m pip install matplotlib")
    sys.exit(1)

# --- CSV path check ---
csv_path = "sales_data.csv"  # use full path if file is elsewhere
if not os.path.exists(csv_path):
    print(f"Error: data file not found: {csv_path}")
    print("Place the CSV in the script folder or provide the full path in csv_path.")
    sys.exit(1)

# --- main logic ---
df = pd.read_csv(csv_path)
print("First 5 rows:\n", df.head())

# ensure Date column exists before converting
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M")
else:
    print("Warning: 'Date' column not found — continuing without date parsing.")
    df["Month"] = None

# compute summaries safely
if "Product" in df.columns and "Sales" in df.columns:
    product_sales = df.groupby("Product")["Sales"].sum()
    print("\nSales by Product:\n", product_sales)
else:
    product_sales = pd.Series(dtype=float)
    print("\nProduct or Sales column missing.")

if "Region" in df.columns and "Sales" in df.columns:
    region_sales = df.groupby("Region")["Sales"].sum()
    print("\nSales by Region:\n", region_sales)
else:
    region_sales = pd.Series(dtype=float)

if "Month" in df.columns and df["Month"].notna().any():
    monthly_sales = df.groupby("Month")["Sales"].sum()
    print("\nMonthly Sales:\n", monthly_sales)
else:
    monthly_sales = pd.Series(dtype=float)

# plotting & saving (no plt.show())
if not product_sales.empty:
    plt.figure(figsize=(10, 6))
    product_sales.plot(kind="bar", title="Sales by Product")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("product_sales.png")
    plt.close()

if not region_sales.empty:
    plt.figure(figsize=(8, 8))
    region_sales.plot(kind="pie", autopct="%1.1f%%", title="Sales by Region")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("region_sales.png")
    plt.close()

if not monthly_sales.empty:
    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend")
    plt.ylabel("Sales")
    plt.xlabel("Month")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("monthly_sales.png")
    plt.close()

print("Plots saved (product_sales.png, region_sales.png, monthly_sales.png if available).")
