import yfinance as yf
from stock_constants import ticker_symbol

stock = yf.Ticker(ticker_symbol)
company_info = stock.info
stock_data = stock.history(period="1y")['Close']  # possible period: 5d, 1mo, 1y

print(f"\nCompany info: {company_info}")
print(stock_data)
print("\nHistorical stock data for the last month:")
print(f"Stock data saved to {ticker_symbol}_stock_data.csv")
