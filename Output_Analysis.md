# Methodology

## Data Cleaning & Preparation
Date Normalization: The datasets used different timestamp formats (DD-MM-YYYY HH:MM vs YYYY-MM-DD). Both were parsed and normalized to a daily date_key to enable accurate merging.

Type Conversion: Financial columns (Closed PnL, Size USD, Fee) contained commas and string formatting. These were cleaned and converted to numeric floats for calculation.

Handling Missing Data: Trades executed on days where Sentiment Data was unavailable were excluded to ensure statistical accuracy.

## Data Enrichment
Merged the transaction-level data with the daily classification (e.g., Fear, Greed) from the Sentiment Index.

Aggregated metrics to calculate Win Rate, Average PnL, and Volume per sentiment category.

# Key Insights & Findings
Based on the analysis of 210,000+ trades, distinct patterns emerged regarding when traders are most profitable.

## "Extreme Greed" is the Most Profitable State
Contrary to the popular "contrarian" belief, traders performed significantly better during periods of Extreme Greed.

Observation: This state yielded the highest Average PnL ($67.89) and the highest Win Rate (46.5%).

Reasoning: Retail traders tend to excel in strong momentum trends (FOMO phases) where "long" positions are easily rewarded by the market tide.

## The "Fear" Paradox
Observation: "Fear" periods saw the highest trading activity (Volume: $483M) and respectable profitability. However, when sentiment shifted to "Extreme Fear", performance collapsed to the lowest tier ($34.54 PnL).

Reasoning: Traders manage moderate volatility well, but during panic events (Extreme Fear), they likely suffer from liquidations or panic selling at the bottom.

## Neutral Markets are Dangerous
Observation: Neutral sentiment resulted in the lowest profitability (~$34.31) and a sub-40% win rate.

Reasoning: Without a clear directional trend, traders likely get "chopped out" by range-bound price action.

# Strategy Recommendations
Based on these findings, we recommend the following product strategies to optimize user success and platform volume:

## Capitalize on "Extreme Greed" (Momentum Tools)
Context: Users are most successful here (Win Rate: 46.5%).

Recommendation: Aggressively market Trailing Stop-Loss tools. Since users are already winning, the goal is to help them capture more of the trend without exiting too early, maximizing volume and fees.

## Protect Users during "Neutral" Phases
Context: Users bleed capital in sideways markets (Avg PnL: ~$34).

Recommendation: Introduce or highlight Grid Trading Bots. These tools are designed specifically to profit from the chop/volatility of a neutral market, whereas manual directional trading fails here.

## Risk Management in "Extreme Fear"
Context: Win rates drop to ~37% (the "falling knife" scenario).

Recommendation: Implement dynamic warnings for high-leverage positions during these specific days. Encouraging Dollar Cost Averaging (DCA) strategies here would be superior to manual "bottom fishing."

# User Segmentation
The analysis script also includes a segmentation module that clusters users into "Whales" (Top 20% by volume) vs. "Retail". This allows for granular analysis of how institutional-sized traders behave differently during Fear periods compared to smaller accounts.
