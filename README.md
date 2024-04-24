# CS539 Group Project - Predicting Stock Market Trends Using News Sentiment Analysis
Given yesterday's stock data and news for a single company, we would like to predict whether the stock will have an uptrend or downtrend **tomorrow**. This will help investors observe how the news may impact the performance of a particular company's stock.

# Dependencies
All code is written in notebooks made from Google Colab. Simply running the pip install cells should be sufficient to download dependencies. Note that there are Google Drive import cells which may be ignored. All necessary files are given in the data folder. A list of dependencies will still be provided below. 
- Pandas
- Numpy
- HuggingFace Transformers library
- Torch for CUDA 12.1
- urllib3
- YFinance
- GNews


# Data
### Stocks
We fetch the last 2 years (2022-01-03 to 2023-12-29) of stock data specifically for Apple, NVIDIA, and Meta. YFinance is used to retrieve stock data for all companies. Outputs are saved in the format `{ticker_name}_stock.csv`.

### News/Sentiment
For sentiment analysis, we use GNews to query relevant articles from the Google News database. We use both the stock ticker name and the full name of each company as search words. Since NewsAPI is limited and can only provide brief sentences from the articles, we manually webscrape the data by querying the links instead and using BeautifulSoup + URLLib3 to parse the HTML into text. News articles for companies are saved as `{ticker_name}_news.csv`. 

For manually generating the stock and news data, run all cells in `datagen/Stock_and_News_Data.ipynb`. Note, we already provide these files in `data`. If you would like to run it yourself, please change the csv paths whenever `.to_csv()' is mentioned. 

To obtain the sentiment for each article for a single company, we feed the scraped content (including the title) of each article into a sentiment analysis model. For the model, we use a distilled version of [RoBERTa-base-model](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis) pretrained on the [financial_phrasebank](https://huggingface.co/datasets/financial_phrasebank) dataset. Sentiment output files are saved as `{ticker_name}_sentiment.csv`. 

For running sentiment analysis, run all cells in `datagen/Sentiment_Analysis.ipynb`. We also provide these files in `data`. Ensure the `csv=` and `.to_csv()` paths are changed accordingly. 


## Feature Engineering
Run all cells in `datagen/Feature_Engineering.ipynb` to combine stock and sentiment features. Again, ensure the `csv=` and `.to_csv()` paths are changed accordingly. Note, this data is already provided in `data/{ticker_name}_stock_with_sentiment.csv`.


## Training and Inference
For training all models and obtaining inference results, run the `Predicting_Stock_Trend_With_Sentiment.ipynb` notebook. Make sure to change the `csv` path with the correct local csv containing both stock and sentiment features. 


## Demo
We provide demo code that uses the `DecisionTreeClassifier` model. The demo shows how performance changes with and without sentiment features and also how different news sentiment affects the model's prediction for one day's worth of stock data. Run `Demo.ipynb` for the demo. Make sure to change `csv` paths for local usage.


## Acknowledgements
1. https://github.com/alisonmitchell/Stock-Prediction