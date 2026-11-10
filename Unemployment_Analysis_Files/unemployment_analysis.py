"""
Unemployment analysis (India, 2019-2020)
Run: python unemployment_analysis.py
Place this script beside archive.zip. It extracts/reads the two CSV files from the ZIP.
"""
import zipfile
import pandas as pd
import matplotlib.pyplot as plt

ARCHIVE = "archive.zip"
with zipfile.ZipFile(ARCHIVE) as z:
    first = pd.read_csv(z.open("Unemployment in India.csv"))
    second = pd.read_csv(z.open("Unemployment_Rate_upto_11_2020.csv"))

for df in (first, second):
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

first = first.dropna(subset=["Region"])
rate = "Estimated Unemployment Rate (%)"

monthly = first.groupby("Date")[rate].mean()
print("Monthly average unemployment rate:")
print(monthly.round(2))
print("\\nAverage by area:")
print(first.groupby("Area")[rate].mean().round(2))
print("\\nHighest regional averages:")
print(first.groupby("Region")[rate].mean().sort_values(ascending=False).head(8).round(2))

pre = monthly.loc["2020-01":"2020-02"].mean()
covid = monthly.loc["2020-04":"2020-05"].mean()
print(f"Pre-lockdown average: {pre:.2f}%")
print(f"April-May average: {covid:.2f}%")
print(f"Increase: {covid-pre:.2f} percentage points")

monthly.plot(marker="o", title="Average unemployment rate by month")
plt.ylabel("Unemployment rate (%)")
plt.tight_layout()
plt.savefig("monthly_trend.png", dpi=180)
plt.show()

first.pivot_table(index="Date", columns="Area", values=rate).plot(
    marker="o", title="Rural and urban unemployment rates"
)
plt.ylabel("Unemployment rate (%)")
plt.tight_layout()
plt.savefig("rural_urban.png", dpi=180)
plt.show()
