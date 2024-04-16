# CS539 Group Project - Predicting Upward and Downward Trends in Daily Stock Prices using News Sentiment Analysis

# Data
## Stocks
We fetch the last 30 days (2024-03-03 to 2024-04-02) of stock data specifically for 45 companies related to AI technology. A list of all companies used can be viewed [here](https://github.com/vagmi20/CS539_groupProject/blob/main/data/AI_Companies_Stock_List.csv).

We use FinnHub to retrieve the data and save the output to [stocks.csv](https://github.com/vagmi20/CS539_groupProject/blob/main/data/stocks.csv). 

## News/Sentiment
For sentiment analysis, we use NewsAPI to query relevant articles from various news sources. We use both the stock ticker name and the full name of each company as search words. Since NewsAPI is limited and can only provide brief sentences from the articles, we manually webscrape the data by querying the links instead and using BeautifulSoup + URLLib3 to parse the HTML into text.

Because multiple companies may be mentioned in a single article, we observe the frequency of each ticker/company name throughout an article and take the most frequently mentioned company/stock as the main target of the article sentiment. 

To obtain the sentiment for each article for a single company, we feed the scraped content (including the title) of each article into a sentiment analysis model. For the model, we use a distilled version of [RoBERTa-base-model](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis) pretrained on the [financial_phrasebank](https://huggingface.co/datasets/financial_phrasebank) dataset.


# Preprocessing


# Training


# Inference

