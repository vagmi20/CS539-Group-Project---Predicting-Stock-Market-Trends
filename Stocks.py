import yfinance as yf  # Import yfinance module


# Define the list of desired stock symbols
stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "IBM", "NVDA",
    "BIDU", "CRM", "TSLA", "TWLO", "PLTR", "AI", "INTC",
    "QCOM", "AMD", "ORCL", "SAP", "SIEGY", "HON",
    "GE", "MU", "ROBO", "PATH", "ZM", "DOCU", "SQ", "SHOP",
    "SPLK", "TTD", "CRWD", "ZS", "SNOW", "FTNT", "ADSK",
    "ADBE", "ASML", "SNPS", "CDNS", "ANSS", "TER", "KYCCF",
    "OMRNY", "0020.HK", "002230.SZ"
]

# Define the time period
start_date = "2024-03-03"  # Start date for fetching data
end_date = "2024-04-02"  # End date for fetching data

# Fetch historical data
data = yf.download(stocks, start=start_date, end=end_date)  # Download stock data

# Structure the data for easier analysis
summary_df = data.stack(level=1).reset_index(level=1).rename(columns={"level_1": "Ticker"})  # Stack and reset index

# Calculate average closing prices by date and add it as a new column
average_closing_by_date = data['Close'].mean(axis=1)  # Calculate average closing price
summary_df['Avg Closing Price'] = summary_df.index.map(average_closing_by_date)  # Map average closing price to new column

# Define the short and long windows for moving averages
short_window = 12  # Short window for moving average
long_window = 26  # Long window for moving average

# Calculate the short and long window moving averages
summary_df['SMA_12'] = summary_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=short_window).mean())  # Calculate short window moving average
summary_df['SMA_26'] = summary_df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=long_window).mean())  # Calculate long window moving average

# Calculate MACD and MACD Signal
summary_df['MACD'] = summary_df['SMA_12'] - summary_df['SMA_26']  # Calculate MACD
summary_df['MACD_Signal'] = summary_df.groupby('Ticker')['MACD'].transform(lambda x: x.rolling(window=9).mean())  # Calculate MACD Signal

# Calculate RSI for each stock
change = summary_df.groupby('Ticker')['Close'].transform(lambda x: x.diff())  # Calculate price change
gain = change.where(change > 0, 0)  # Separate gains
loss = -change.where(change < 0, 0)  # Separate losses
avg_gain = gain.rolling(window=14).mean()  # Calculate average gain
avg_loss = loss.rolling(window=14).mean()  # Calculate average loss
rs = avg_gain / avg_loss  # Calculate relative strength
summary_df['RSI'] = 100 - (100 / (1 + rs))  # Calculate RSI

# Print the data types
print(summary_df.dtypes)  # Print data types of DataFrame

# Print the summary dataframe
print(summary_df)  # Print DataFrame

#Moving Averages: Help identify trends. A rising moving average indicates an uptrend,
# while a falling moving average indicates a downtrend.

#MACD: Used to catch trends early and can also indicate the end of a trend.
# A crossover of the MACD line above the signal line is a bullish signal, while a crossover below is a bearish signal.

#RSI: Identifies overbought or oversold conditions.
# Values over 70 suggest an overbought condition (potentially overvalued),
# and values under 30 suggest an oversold condition (potentially undervalued).