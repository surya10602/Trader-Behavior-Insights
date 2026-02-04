import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Step 1: Load Datasets

try:
    df_trades = pd.read_csv('historical_data.csv')
    df_sentiment = pd.read_csv('fear_greed_index.csv')
    print("Datasets loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading files: {e}")

# Step 2: Data Preparation & Cleaning

df_trades['datetime'] = pd.to_datetime(df_trades['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')

df_trades['date_key'] = df_trades['datetime'].dt.normalize()

cols_to_numeric = ['Closed PnL', 'Size USD', 'Fee', 'Execution Price']
for col in cols_to_numeric:
    if col in df_trades.columns:
        df_trades[col] = pd.to_numeric(df_trades[col].astype(str).str.replace(',', ''), errors='coerce')

df_sentiment['date_key'] = pd.to_datetime(df_sentiment['date']).dt.normalize()

df_merged = pd.merge(df_trades, df_sentiment[['date_key', 'value', 'classification']], on='date_key', how='left')

print(f"Total trades: {len(df_merged)}")
print(f"Trades with missing sentiment: {df_merged['classification'].isna().sum()}")
df_merged.dropna(subset=['classification'], inplace=True)

# Step 3: Exploratory Analysis

sentiment_metrics = df_merged.groupby('classification').agg(
    total_trades=('Account', 'count'),
    avg_pnl=('Closed PnL', 'mean'),
    total_volume=('Size USD', 'sum'),
    win_rate=('Closed PnL', lambda x: (x > 0).mean() * 100)
).reset_index()

order_map = {'Extreme Fear': 0, 'Fear': 1, 'Neutral': 2, 'Greed': 3, 'Extreme Greed': 4}
sentiment_metrics['sort_order'] = sentiment_metrics['classification'].map(order_map)
sentiment_metrics = sentiment_metrics.sort_values('sort_order')

print("\n--- Trader Performance vs Market Sentiment ---")
print(sentiment_metrics)

# Step 4: Visualizations

# Plot 1: Average PnL by Sentiment
plt.figure()
sns.barplot(data=sentiment_metrics, x='classification', y='avg_pnl', palette='RdYlGn')
plt.title('Average Trader PnL per Trade by Market Sentiment')
plt.ylabel('Average Closed PnL (USD)')
plt.xlabel('Market Sentiment')
plt.show()

# Plot 2: Trading Volume by Sentiment
plt.figure()
sns.barplot(data=sentiment_metrics, x='classification', y='total_trades', palette='Blues')
plt.title('Trading Activity (Number of Trades) by Market Sentiment')
plt.ylabel('Total Trade Count')
plt.xlabel('Market Sentiment')
plt.show()

# Step 5: Group by Account to find "Whales" vs "Retail"
trader_profiles = df_merged.groupby('Account').agg(
    total_volume=('Size USD', 'sum'),
    avg_pnl=('Closed PnL', 'mean'),
    trade_count=('Account', 'count')
)

volume_threshold = trader_profiles['total_volume'].quantile(0.8) 
trader_profiles['trader_type'] = np.where(trader_profiles['total_volume'] > volume_threshold, 'Whale', 'Retail')

df_segmented = pd.merge(df_merged, trader_profiles[['trader_type']], on='Account', how='left')

# Compare PnL during "Fear" for Whales vs Retail
fear_performance = df_segmented[df_segmented['classification'] == 'Fear'].groupby('trader_type')['Closed PnL'].mean()
print("\n--- Performance during 'Fear' Periods ---")
print(fear_performance)