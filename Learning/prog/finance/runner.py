import yfinance as yf

from data_sourcing.stock_constants import ticker_symbol
from plotting_functions.plot import plot_stock_data

stock = yf.Ticker(ticker_symbol)
company_info = stock.info
stock_data = stock.history(period="1y")['Close']  # possible period: 5d, 1mo, 1y

plot_stock_data(stock_data)
