import yfinance as yf
# create ticker for Apple Stock
ticker = yf.Ticker('AAPL')
# get data of the most recent date
todays_data = ticker.history(period='1d')

print(todays_data)


# Specifying the period

import datetime
 
# startDate , as per our convenience we can modify
startDate = datetime.datetime(2023, 1, 1)
 
# endDate , as per our convenience we can modify
endDate = datetime.datetime(2023, 12, 31)
apple_data = yf.Ticker('AAPL')
# pass the parameters as the taken dates for start and end
aapl_df = apple_data.history(start=startDate, end=endDate)
# plot the close price 
aapl_df['Close'].plot(title="APPLE's stock")


# Retrieving mutiple stocks data

import pandas as pd
import matplotlib.pyplot as plt
tickers_list = ['AAPL', 'WMT', 'IBM', 'MU', 'BA', 'AXP']

# Fetch the data
import yfinance as yf
data = yf.download(tickers_list,'2023-1-1')['Adj Close']

# Plot all the close prices
((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))
plt.legend()
plt.title("Close Value", fontsize=16)

# Define the labels
plt.ylabel('Cumulative Close Value', fontsize=14)
plt.xlabel('Time', fontsize=14)

# Plot the grid lines
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()