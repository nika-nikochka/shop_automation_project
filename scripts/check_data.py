# scripts/check_data.py
import pandas as pd

df = pd.read_csv('data/processed/orders_enriched.csv', parse_dates=['order_date'])

print("🔍 Проверка данных:")
print(f"Колонки: {df.columns.tolist()}")
print(f"\nПропуски (NaN):")
print(df.isnull().sum())
print(f"\nСтатистика:")
print(df.describe())
print(f"\nПример данных:")
print(df.head())