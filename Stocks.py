import yfinance as yf

# List of desired stock symbols
stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "IBM", "NVDA",
    "BIDU", "CRM", "TSLA", "TWLO", "PLTR", "AI", "INTC",
    "QCOM", "AMD", "ORCL", "SAP", "SIEGY", "HON",
    "GE", "MU", "ROBO", "PATH", "ZM", "DOCU", "SQ", "SHOP",
    "SPLK", "CRWD", "ZS", "SNOW", "FTNT", "ADSK",
    "ADBE", "ASML", "SNPS", "CDNS", "ANSS", "TER", "KYCCF",
    "OMRNY", "0020.HK", "002230.SZ",
]

# Define the time period
start_date = "2024-02-23"
end_date = "2024-03-22"



# Fetch historical data
data = yf.download(stocks, start=start_date, end=end_date)

# Assuming `data` is the DataFrame returned by yfinance
summary_df = data.stack(level=1).reset_index(level=1).rename(columns={"level_1": "Ticker"})
print(summary_df)

# Calculate average closing prices by date
average_closing_by_date = data['Close'].mean(axis=1)

# Add this as a new column to the summary_df
summary_df['Avg Closing Price'] = summary_df.index.map(average_closing_by_date)
# Check current data types
print(summary_df.dtypes)


print(summary_df)



