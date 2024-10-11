import psycopg2
from celery import Celery

# Initialize Celery
app = Celery('submit_task', broker='redis://localhost:6379/0')

# Function to fetch URLs from the database
def fetch_urls():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="newsdb",  # Use the correct database name
            user="admin",
            password="admin",  # Replace with your actual password
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Execute SQL query to fetch URLs
        cursor.execute("SELECT url FROM urls;")
        urls = cursor.fetchall()

        # Close database connection
        cursor.close()
        conn.close()

        # Return fetched URLs
        return [url[0] for url in urls]  # Extracting URLs from tuples
    except Exception as e:
        print(f"Error fetching URLs: {e}")
        return []

# Celery task to process articles
@app.task
def process_article(url):
    print(f"Processing article at {url}")
    # Your article processing logic goes here

# Main block to submit tasks to the Celery worker
if __name__ == "__main__":
    urls = fetch_urls()
    if urls:
        for url in urls:
            process_article.delay(url)  # Submit tasks asynchronously
    else:
        print("No article URLs found.")
