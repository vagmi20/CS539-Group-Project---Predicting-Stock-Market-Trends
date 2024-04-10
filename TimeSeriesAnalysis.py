import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from pymongo import MongoClient
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import seaborn as sns


# Load stock data from CSV
stock_data_path = 'D:/PyCharm/CS539_groupProject/src/data/stocks.csv'
stock_df = pd.read_csv(stock_data_path)

# Connect to MongoDB and fetch sentiment data
client = MongoClient('mongodb+srv://bsolimanhanna:K123456789@newsapitwoweeks.y1s7pil.mongodb.net/?retryWrites=true&w=majority&appName=NewsAPITwoWeeks')
db = client['stocks_news']
collection = db['articles']
sentiment_data = list(collection.find({}, {'publishedAt': 1, 'sentiment_score': 1}))
sentiment_df = pd.DataFrame(sentiment_data)
# Normalize sentiment scores
sentiment_score_mapping = {'positive': 1, 'neutral': 0, 'negative': -1}
sentiment_df['normalized_score'] = sentiment_df['sentiment_score'].map(sentiment_score_mapping)

# Convert 'publishedAt' to datetime and set index
sentiment_df['publishedAt'] = pd.to_datetime(sentiment_df['publishedAt']).dt.tz_localize(None)
daily_sentiment = sentiment_df.groupby('publishedAt')['normalized_score'].mean()

# Prepare stock data
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
stock_df.set_index('Date', inplace=True)
numeric_cols = stock_df.select_dtypes(include='number').columns
stock_df = stock_df[numeric_cols]
stock_df = stock_df.groupby(stock_df.index).mean()

# Combine data
combined_df = pd.merge(stock_df, daily_sentiment, left_index=True, right_index=True, how='left')
combined_df['normalized_score'].fillna(0, inplace=True)
combined_df.sort_index(inplace=True)
combined_df = combined_df.asfreq('D')

# Stationarity check
adf_result = adfuller(combined_df['Adj Close'].dropna())
print(f'ADF Statistic: {adf_result[0]}')
print(f'p-value: {adf_result[1]}')

# Data split
time_series_data = combined_df['Adj Close']
sentiment_exog = combined_df['normalized_score'].to_frame()
split_point = int(0.8 * len(time_series_data))
train_data, test_data = time_series_data[:split_point], time_series_data[split_point:]
train_sentiment, test_sentiment = sentiment_exog[:split_point], sentiment_exog[split_point:]

# Drop NaN values from the time series and ensure lengths match
train_data.dropna(inplace=True)
train_sentiment.dropna(inplace=True)
assert len(train_data) == len(train_sentiment), "Training data and sentiment lengths do not match."

# Before forecasting, ensure there are no NaN values in the test_sentiment
test_sentiment.fillna(0, inplace=True)

# Model fitting
model_arima = auto_arima(train_data, exogenous=train_sentiment, seasonal=False, m=1, trace=True, error_action='ignore', suppress_warnings=True)
print(model_arima.summary())
sarimax_model = SARIMAX(train_data, exog=train_sentiment, order=model_arima.order, enforce_stationarity=False, enforce_invertibility=False)
sarimax_result = sarimax_model.fit()

# Forecasting
sarimax_forecast = sarimax_result.get_forecast(steps=len(test_data), exog=test_sentiment)
forecast_index = test_data.index
forecast_series = pd.Series(sarimax_forecast.predicted_mean, index=forecast_index)
sarimax_forecast_conf_int = sarimax_forecast.conf_int()

# Check the range of forecasted values
print(forecast_series.describe())

# Styling
sns.set(style="whitegrid", palette="pastel", color_codes=True)
plt.rcParams['figure.figsize'] = (15, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16

# Assuming sns is already imported and matplotlib.pyplot as plt
sns.set(style="whitegrid", palette="pastel", color_codes=True)
plt.rcParams['figure.figsize'] = (15, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16

# Ensure forecast index is correct
forecast_index = pd.date_range(start=train_data.index[-1], periods=len(test_data)+1, freq='B')[1:]
forecast_series = pd.Series(sarimax_forecast.predicted_mean, index=forecast_index)

# Check the range of forecasted values
print(forecast_series.describe())

## Create the plot
fig, ax = plt.subplots()

# Plot the training data series for context
ax.plot(train_data.index, train_data, label='Training Data', linewidth=2, alpha=0.6)

# Plot the actual test data
ax.plot(test_data.index, test_data, label='Actual Data', color='orange', linewidth=2)

# Plot the forecast
ax.plot(forecast_series.index, forecast_series, label='SARIMAX Forecast with Sentiment', color='green', linewidth=2)

# Highlighting the forecast area
ax.fill_between(forecast_series.index, sarimax_forecast_conf_int.iloc[:, 0], sarimax_forecast_conf_int.iloc[:, 1], color='green', alpha=0.2, label='Confidence Interval')

# Annotations and labels
ax.set_title('Stock Price Forecast with Sentiment Analysis Influence')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted Close Price')
ax.legend(loc='upper left')

# Dynamically adjust the y-axis limits based on the forecasted values
ylim_lower = min(train_data.min(), forecast_series.min()) - (train_data.std() * 3)
ylim_upper = max(train_data.max(), forecast_series.max()) + (train_data.std() * 3)
ax.set_ylim(ylim_lower, ylim_upper)

# Adjust layout to fit all elements
plt.tight_layout()

# Show the plot
plt.show()