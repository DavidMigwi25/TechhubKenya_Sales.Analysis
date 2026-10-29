# Tech Hub Kenya — Sales Data Analysis



## 1. Overview



Tech Hub Kenya sells phones, laptops, and accessories across five stores in Nairobi, Mombasa, Kisumu, and Nakuru.



The finance manager needs a September sales report to understand total revenue, identify the highest-earning products, and flag high-value transactions that may require follow-up.



This project uses Python's standard library to read, clean, analyse, and summarise sales data. Pandas is used separately to verify the headline results against an independent implementation of the same cleaning rules.



The analysis focuses on data quality, accurate calculations, reusable functions, and transparent reporting decisions.



## 2. Learning Objectives



\- Read CSV files using `csv.DictReader`.

\- Convert messy numeric values safely using exception handling.

\- Document invalid records and explain why they were excluded.

\- Aggregate revenue using dictionaries.

\- Rank products using tuples and `sorted()`.

\- Filter high-value transactions using list comprehensions.

\- Build reusable statistical functions for mean, median, minimum, and maximum.

\- Verify standard-library calculations using pandas.



## 3. Technologies Used



\- \*\*Python  — data processing and analysis.

\- \*\*CSV module\*\* — reading and writing CSV files.

\- \*\*Dictionaries and tuples\*\* — aggregations and product rankings.

\- \*\*List and dictionary comprehensions\*\* — filtering and summarising transactions.

\- \*\*Exception handling\*\* — managing invalid numeric values.

\- \*\*Pandas\*\* — independent verification of headline results.



The core analysis is designed to run using Python's standard library without third-party packages. Pandas is required only for the separate verification step.



## 4. Project Structure



```text

Sales_Analysis_Without_Pandas/

├── sales_analysis.py

├── electronic_sales.csv

├── README.md

├── requirements.txt

```



## 5. Analysis Methodology



### 5.1 Reading the CSV File



The `read\_sales(path)` function uses `csv.DictReader` to read the sales data into dictionaries.



It reports:

\- The number of rows read.

\- The column names found in the file.



This approach avoids using pandas for the initial data ingestion.



### 5.2 Cleaning and Converting Numeric Values



The `parse\_number(value)` function converts valid numeric strings into appropriate numeric types. The `convert\_rows(rows)` function applies the conversion rules to each record and tracks skipped rows with a reason for each exclusion.



\*\*Data-cleaning decisions\*\*



The cleaning policy should reflect the actual source data. The proposed rules are:



\- Trim leading and trailing whitespace before parsing values.

\- Accept valid integer quantities and numeric unit prices.

\- Repair a price only when the intended numeric value is unambiguous, such as removing a clearly identifiable currency prefix or thousands separator.

\- Reject missing, non-numeric, or ambiguous values rather than guessing the intended value.

\- Reject quantities or prices that violate agreed business rules, such as non-positive quantities or negative unit prices, where applicable.

\- Record every skipped row and the reason for exclusion.



These rules must be confirmed against the actual CSV. Any repair or exclusion should be documented so the report is reproducible and auditable.



### 5.3 Calculating Total Revenue



The `total\_revenue(rows)` function calculates transaction revenue as:



\*\*Revenue = Quantity × Unit Price\*\*



The total is reported in Kenyan shillings (KES), formatted to two decimal places with thousands separators.



### 5.4 Revenue Breakdown



The `revenue_by(rows, field)` function uses a plain Python dictionary to calculate revenue by a selected field.



It is used to produce:

\- Revenue by product.

\- Revenue by store.

\- Revenue by payment method.



The product breakdown is sorted from highest to lowest revenue to identify the strongest-performing products.



### 5.5 Top Three Products



The `top_n(totals, n)` function returns a list of `(product, revenue)` tuples.



The products are ranked using `sorted()` and a key function. Where two products have equal revenue, the tie-break rule is alphabetical order by product name, ensuring consistent results.



\### 5.6 High-Value Transactions



The `high_value(rows, threshold)` function uses a list comprehension to select transactions with revenue greater than or equal to KES 50,000.



The report includes qualifying transactions and a dictionary comprehension that counts high-value sales for each store.



The threshold is applied to transaction revenue, not unit price alone.



### 5.7 Descriptive Statistics



Three reusable functions are implemented without relying on Python's `statistics` module:



\- `mean(values)` — calculates average transaction revenue.

\- `median(values)` — calculates the middle transaction revenue after sorting the values.

\- `minimum\_maximum(values)` — returns the smallest and largest transaction revenue without using the built-in `min()` or `max()` functions.



Each function raises a clear `ValueError` when given an empty list.



The statistics are calculated using cleaned, valid transaction revenues.



### 5.8 Verification with Pandas



The `verify_with_pandas(path, my_results)` function independently recalculates headline figures using pandas.



The pandas verification applies the same data-cleaning rules as the standard-library implementation and compares the results.



Each comparison reports either:



\- `MATCH` — the two calculations agree.

\- `MISMATCH` — the results differ and require investigation.



Potential causes of a mismatch include inconsistent cleaning rules, different treatment of invalid rows, incorrect numeric conversion, rounding differences, or calculation errors.



Any mismatch should be investigated and explained rather than ignored.



## 6. Key Outputs



The analysis is designed to report:



1\. Number of CSV records and discovered column names.

2\. Total revenue for valid transactions.

3\. Revenue by product, store, and payment method.

4\. Top three products by revenue.

5\. Transactions worth at least KES 50,000.

6\. High-value transaction counts by store.

7\. Mean, median, minimum, and maximum transaction revenue.

8\. Skipped records and their exclusion reasons.

9\. Pandas verification results for headline metrics.



## 7. How to Run



\### Run the Standard-Library Analysis



Open a terminal in the project folder and execute:



```bash

python sales\_analysis.py

```



Use the correct script filename and CSV path if they differ from the examples above.



\### Run the Pandas Verification



Install pandas on your laptop if it is not already available:



```bash

python -m pip install pandas

```



Run the script using the same command. The verification step should report `MATCH` or `MISMATCH` for each headline metric.



The standard-library analysis should remain usable on the reporting server even when pandas is unavailable. If the script imports pandas unconditionally at startup, separate the verification code or handle the optional dependency so the core analysis can still run.



## 8. Data Quality and Limitations



The reliability of the results depends on the accuracy of the source CSV and the consistency of the cleaning rules.



\- Ambiguous prices should not be silently guessed.

\- Excluded rows should be recorded with clear reasons.

\- Revenue calculations should use validated numeric values.

\- Pandas verification can detect implementation errors, but it does not prove correctness if both implementations share the same faulty assumptions.

\- Results describe the supplied September dataset and should not be generalised to other periods without further analysis.



## 9. Conclusion



This project demonstrates how Python's built-in tools can support practical sales reporting in a restricted environment. It combines data cleaning, aggregation, ranking, filtering, and descriptive statistics with a separate pandas verification step.



The resulting analysis provides the finance manager with a transparent view of revenue performance, leading products, and transactions that may warrant follow-up.



\### Console Output Report 



```=== Sales report: September 2026 ===

Rows read          : 50

Rows used          : 46

Rows skipped       : 4   (S-3006: invalid quantity 'two', S-3030: invalid unit price 'N/A', S-3035: missing quantity, S-3039: missing unit price)



Total revenue (KES): 1,310,812.00



Revenue by product (KES)

HP 15 Laptop                389,994.00

Hisense 43in Smart TV       272,993.00

Lenovo Tab M10              199,992.00

Tecno Spark 20              161,988.00

Infinix Hot 40               63,996.00

Samsung Galaxy A15           56,997.00

JBL Go 3 Speaker             49,491.00

Anker Power Bank 20000       38,691.00

Xiaomi Redmi Buds            25,592.00

Oraimo FreePods              19,593.00

USB-C Charger 25W            19,487.00

Safaricom Neon Ray           11,998.00



Top 3 products

1. HP 15 Laptop - KES 389,994.00

2. Hisense 43in Smart TV - KES 272,993.00

3. Lenovo Tab M10 - KES 199,992.00



High-value transactions (>= KES 50,000): 5

S-3022  2026-09-13  Nairobi CBD  HP 15 Laptop  KES 259,996.00

S-3017  2026-09-10  Kisumu Mega Plaza  Hisense 43in Smart TV  KES 155,996.00

S-3048  2026-09-30  Kisumu Mega Plaza  HP 15 Laptop  KES 129,998.00

S-3013  2026-09-08  Westgate  Lenovo Tab M10  KES 99,996.00

S-3036  2026-09-21  Nakuru Westside  Tecno Spark 20  KES 53,996.00



High-value sales per store

Kisumu Mega Plaza         2

Mombasa City Mall         0

Nairobi CBD               1

Nakuru Westside           1

Westgate                  1



Transaction revenue statistics

mean   : 28,495.91

median : 11,097.00

min    : 1,499.00

max    : 259,996.00



Revenue by store (KES)

Kisumu Mega Plaza           449,678.00

Nairobi CBD                 331,085.00

Westgate                    235,979.00

Mombasa City Mall           154,082.00

Nakuru Westside             139,988.00



Revenue by payment method (KES)

M-Pesa                      738,568.00

Cash                        304,375.00

Card                        267,869.00



=== pandas verification ===

Total revenue      : MATCH

Revenue by product : MATCH

Top 3              : MATCH

Mean / median      : MATCH

```



