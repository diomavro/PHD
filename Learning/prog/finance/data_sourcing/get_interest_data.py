# Fetch the 10-Year U.S. Treasury yield (symbol: ^TNX on Yahoo Finance)
import yfinance as yf

bond_yield = yf.Ticker('^TNX')

# Get historical data for the last month
yield_data = bond_yield.history(period="1mo")

