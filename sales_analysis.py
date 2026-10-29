"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import pandas as pd
import csv
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent / "electronics_sales.csv"
HIGH_VALUE_THRESHOLD = 50_000.


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(f"Read {len(rows)} rows. Columns: {reader.fieldnames}\n")
        return rows

def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted.
 
    Repaired: surrounding spaces, thousands separators ('38,999'), a 'KES' prefix.
    Rejected: blanks, words ('two'), 'N/A', zero/negative, NaN/inf.
    """
    if value is None:
        return None
    text = value.strip().upper()
    if text.startswith("KES"):
        text = text[3:].strip()
    text = text.replace(",", "")
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number



def _describe(raw: str, label: str) -> str:
    return f"missing {label}" if not raw.strip() else f"invalid {label} {raw!r}"
 
 
def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    clean, skipped = [], []
    for row in rows:
        quantity = parse_number(row["quantity"])
        price = parse_number(row["unit_price_kes"])
        if quantity is not None and not quantity.is_integer():
            quantity = None  # a fractional unit count cannot be trusted
        reasons = []
        if quantity is None:
            reasons.append(_describe(row["quantity"], "quantity"))
        if price is None:
            reasons.append(_describe(row["unit_price_kes"], "unit price"))
        if reasons:
            skipped.append({**row, "reason": "; ".join(reasons)})
            continue
        clean.append({
            **row,
            "quantity": int(quantity),
            "unit_price_kes": price,
            "revenue": quantity * price,
        })
    return clean, skipped


def total_revenue(rows: list[dict]) -> float:
    total = 0.0
    for row in rows:
        total += row["revenue"]
    return total


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals: dict[str, float] = {}
    for row in rows:
        key = row[field]
        if key not in totals:
            totals[key] = 0.0
        totals[key] += row["revenue"]
    return dict(sorted(totals.items(), key=lambda item: (-item[1], item[0])))


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    return sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:n]

def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [row for row in rows if row["revenue"] >= threshold]


# Reusable statistics - implement these yourself, no statistics module.
def _require_values(values: list[float], name: str) -> None:
    if not values:
        raise ValueError(f"{name}() needs at least one value, got an empty list")
def mean(values: list[float]) -> float:
    _require_values(values, "mean")
    return sum(values) / len(values)

def high_value_by_store(big: list[dict], rows: list[dict]) -> dict[str, int]:
    """Number of high-value sales per store (every store listed, zero included)."""
    stores = sorted({row["store"] for row in rows})
    return {store: len([r for r in big if r["store"] == store]) for store in stores}

def median(values: list[float]) -> float:
    _require_values(values, "median")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2

def minimum_maximum(values: list[float]) -> tuple[float, float]:
    _require_values(values, "minimum_maximum")
    low = high = values[0]
    for v in values[1:]:
        if v < low:
            low = v
        if v > high:
            high = v
    return low, high


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
 
    def to_num(series: pd.Series) -> pd.Series:
        text = (series.str.upper().str.replace("KES", "", regex=False)
                .str.replace(",", "", regex=False).str.strip())
        return pd.to_numeric(text, errors="coerce")
 
    df["qty"], df["price"] = to_num(df["quantity"]), to_num(df["unit_price_kes"])
    df = df[(df["qty"] > 0) & (df["price"] > 0) & (df["qty"] % 1 == 0)].copy()
    df["revenue"] = df["qty"] * df["price"]
 
    p_total = df["revenue"].sum()
    p_by_product = df.groupby("product")["revenue"].sum()
    p_top3 = (p_by_product.reset_index().sort_values(["revenue", "product"], ascending=[False, True])
              .head(3))
    p_top3 = list(zip(p_top3["product"], p_top3["revenue"]))
    p_mean, p_median = df["revenue"].mean(), df["revenue"].median()
 
    def same(a, b):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6)
 
    def verdict(ok, pure, pand):
        return "MATCH" if ok else f"MISMATCH (pure={pure}, pandas={pand})"
 
    by_product_ok = (set(p_by_product.index) == set(my_results["by_product"])
                     and all(same(my_results["by_product"][k], v) for k, v in p_by_product.items()))
    top3_ok = ([k for k, _ in my_results["top3"]] == [k for k, _ in p_top3]
               and all(same(a[1], b[1]) for a, b in zip(my_results["top3"], p_top3)))
    stats_ok = same(my_results["mean"], p_mean) and same(my_results["median"], p_median)
 
    print("=== pandas verification ===")
    print(f"Total revenue      : {verdict(same(my_results['total'], p_total), my_results['total'], p_total)}")
    print(f"Revenue by product : {verdict(by_product_ok, '...', '...')}")
    print(f"Top 3              : {verdict(top3_ok, my_results['top3'], p_top3)}")
    print(f"Mean / median      : {verdict(stats_ok, (my_results['mean'], my_results['median']), (p_mean, p_median))}")

def print_report(raw, clean, skipped) -> dict:
    total = total_revenue(clean)
    by_product = revenue_by(clean, "product")
    top3 = top_n(by_product, 3)
    big = sorted(high_value(clean, HIGH_VALUE_THRESHOLD), key=lambda r: (-r["revenue"], r["sale_id"]))
    big_by_store = high_value_by_store(big, clean)
    by_store = revenue_by(clean, "store")
    by_payment = revenue_by(clean, "payment_method")
    revenues = [r["revenue"] for r in clean]
    low, high = minimum_maximum(revenues)
    avg, mid = mean(revenues), median(revenues)
 
    skipped_text = ", ".join(f"{r['sale_id']}: {r['reason']}" for r in skipped)
    print("=== Sales report: September 2026 ===")
    print(f"Rows read          : {len(raw)}")
    print(f"Rows used          : {len(clean)}")
    print(f"Rows skipped       : {len(skipped)}   ({skipped_text})")
    print(f"\nTotal revenue (KES): {total:,.2f}")
 
    print("\nRevenue by product (KES)")
    for product, amount in by_product.items():
        print(f"  {product:<24}{amount:>14,.2f}")
 
    print("\nTop 3 products")
    for i, (product, amount) in enumerate(top3, 1):
        print(f"  {i}. {product} - KES {amount:,.2f}")
 
    print(f"\nHigh-value transactions (>= KES {HIGH_VALUE_THRESHOLD:,.0f}): {len(big)}")
    for r in big:
        print(f"  {r['sale_id']}  {r['sale_date']}  {r['store']}  {r['product']}  KES {r['revenue']:,.2f}")
 
    print("\nHigh-value sales per store")
    for store, n in big_by_store.items():
        print(f"  {store:<24}{n:>3}")
 
    print("\nTransaction revenue statistics")
    print(f"  mean   : {avg:,.2f}")
    print(f"  median : {mid:,.2f}")
    print(f"  min    : {low:,.2f}")
    print(f"  max    : {high:,.2f}")
 
    print("\nRevenue by store (KES)")
    for store, amount in by_store.items():
        print(f"  {store:<24}{amount:>14,.2f}")
    print("\nRevenue by payment method (KES)")
    for method, amount in by_payment.items():
        print(f"  {method:<24}{amount:>14,.2f}")
    print()
    return {"total": total, "by_product": by_product, "top3": top3, "mean": avg, "median": mid}
if __name__ == "__main__":
    raw = read_sales()
    clean, skipped = convert_rows(raw)
    results = print_report(raw, clean, skipped)
    verify_with_pandas(DATA_PATH, results)
#     pass
