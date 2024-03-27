import yfinance as yf

# List of desired stock symbols
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "IBM", "NVDA"]

# Define the time period
start_date = "2024-02-26"
end_date = "2024-03-26"



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

# # Define the file path where you want to save the CSV file
# file_path = 'D:/Datasets/stock_summary.csv'
#
# # Export the summary DataFrame to a CSV file
# summary_df.to_csv(file_path, index=True)
#
# print(f"File saved to {file_path}")

# print(summary_df)


