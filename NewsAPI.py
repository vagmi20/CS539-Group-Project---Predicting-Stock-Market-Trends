from newsapi import NewsApiClient
import pymongo
from langdetect import detect, LangDetectException

class NewsArticleManager:
    def __init__(self, api_key, mongodb_uri, db_name='new_stocks_news', collection_name='articles'):
        self.newsapi = NewsApiClient(api_key=api_key)
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def is_english(self, text):
        try:
            return detect(text) == 'en'
        except LangDetectException:
            return False

    def fetch_and_save_articles(self, keyword, from_date, to_date):
        query = keyword
        articles = self.newsapi.get_everything(q=query, from_param=from_date, to=to_date, language='en', sort_by='popularity')
        for article in articles['articles']:
            text_to_check = article.get('content') or article.get('description')
            if "[Removed]" not in article.get('title', '') and text_to_check and self.is_english(text_to_check):
                if not self.collection.find_one({'url': article['url']}):
                    self.collection.insert_one(article)

    def cleanup_articles(self):
        articles = self.collection.find()
        for article in articles:
            if "[Removed]" in article.get('title', '') or (not self.is_english(article.get('content') or article.get('description', ''))):
                self.collection.delete_one({'_id': article['_id']})

    def cleanup_duplicate_articles(self):
        pipeline = [
            {"$group": {"_id": "$url", "uniqueIds": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        duplicates = self.collection.aggregate(pipeline)
        for duplicate in duplicates:
            ids_to_remove = duplicate['uniqueIds'][1:]
            for id_to_remove in ids_to_remove:
                self.collection.delete_one({"_id": id_to_remove})

    def print_articles_from_mongodb(self):
        articles = self.collection.find()
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Description: {article.get('description', 'No description available')}")
            print(f"URL: {article['url']}\n")
            print("--------------------------------------------------\n")

if __name__ == '__main__':
    api_key = 'cbaf7f1f50ab40f6915bcb91db00ae1c'
    mongodb_uri = 'mongodb+srv://bsolimanhanna:K123456789@newsapitwoweeks.y1s7pil.mongodb.net/?retryWrites=true&w=majority&appName=NewsAPITwoWeeks'
    manager = NewsArticleManager(api_key, mongodb_uri)

    keywords = ["Apple", "Nvidia", "TikTok"]
    for keyword in keywords:
        manager.fetch_and_save_articles(keyword, '2024-02-23', '2024-03-22')

    print("Finished fetching and saving articles. Now cleaning up...")
    manager.cleanup_articles()
    manager.cleanup_duplicate_articles()

    print("Now printing articles from MongoDB:\n")
    manager.print_articles_from_mongodb()
