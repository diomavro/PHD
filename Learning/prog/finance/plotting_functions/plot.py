import matplotlib.pyplot as plt

def plot_stock_data(stock_data):
    # Plot stock data
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index, stock_data.values)
    plt.xlabel('Date')
    plt.ylabel('Stock price ($)')
    plt.title('Stock price over time')
    plt.show()