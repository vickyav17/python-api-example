import logging
import feedparser
from datetime import datetime
from models import Article, session
from sqlalchemy.exc import IntegrityError
from celery_app import process_article

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def parse_feeds():
    logger.info("Parsing RSS feeds...")
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            publication_date = entry.get('published', None)
            if publication_date is None:
                publication_date = datetime.now().isoformat()  # Use current timestamp as default
            article = {
                'title': entry.title,
                'content': entry.get('summary', 'No summary available'),
                'publication_date': publication_date,
                'source_url': entry.link
            }
            articles.append(article)
    return articles

def store_articles(articles):
    logger.info("Storing articles in the database...")
    for article in articles:
        try:
            process_article.delay(article)  # Assuming it's a Celery task
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")  # Catch specific SQL errors
            session.rollback()  # Rollback transaction if any error
        except Exception as e:
            logger.error(f"Error occurred while storing article: {e}")


