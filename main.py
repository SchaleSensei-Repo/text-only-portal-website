import requests
import feedparser
import datetime
import time
import os
import json
import base64

# Import Google Cloud Storage client library
from google.cloud import storage

# --- Configuration ---
# List of RSS feed URLs
RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://www.theguardian.com/world/rss",
    "https://time.com/feed/",
    "https://arstechnica.com/feed/",
    "https://www.techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://www.engadget.com/rss.xml",
    "https://www.cnet.com/rss/news/",
    "https://www.zdnet.com/news/rss.xml",
    "https://www.antaranews.com/rss/terkini",
    "https://www.japantimes.co.jp/feed/",
    "https://mainichi.jp/rss/etc/mainichi-e.rss",
    "https://feeds.feedburner.com/TechCrunch/startups",
    "http://rss.tempo.co/nasional",
    "https://www.republika.co.id/rss/",
    "https://news.detik.com/berita/rss",
    "https://www.tribunnews.com/rss"
]

# IMPORTANT: Replace with the actual name of your Cloud Storage bucket
# This is where the static HTML files will be stored.
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'schale-text-only-portal-cache')

# Initialize GCS client (outside the function for efficiency in warm starts)
storage_client = storage.Client()
gcs_bucket = storage_client.bucket(GCS_BUCKET_NAME)

# --- Static Links from Original Homepage ---
# This content is hardcoded as it's static and comes from your provided homepage.html
STATIC_LINKS_CONTENT = """
    <div class="section">
        <h2>News and Community/Forum Aggregators</h2>
        <ul>
            <li><a href="https://news.lenexia.com/">Lenexia News (Customizable News Aggregator)</a></li>
            <li><a href="https://www.newsminimalist.com/">Newsminimalist (Text-Only Aggregator)</a></li>
            <li><a href="https://hckrnews.com/">Hckr News (Condensed Hacker News)</a></li>
            <li><a href="https://hackerweb.app/">HackerWeb (Accessible Hacker News)</a></li>
            <li><a href="https://lobste.rs/">Lobsters (Computing Topics, Link Collection & Discussion)</a></li>
            <li><a href="https://brutalist.report/">Brutalist Report (Text-Only News Compilation)</a></li>
            <li><a href="https://skimfeed.com/">SkimFeed (News Aggregator for various topics)</a></li>
            <li><a href="https://lite.pbs.org/">PBS Lite (Low-bandwidth PBS)</a></li>
            <li><a href="https://www.csmonitor.com/layout/set/text/textedition">Christian Science Monitor Text Edition</a></li>
            <li><a href="https://www.npr.org/text/">NPR News Text Only</a></li>
            <li><a href="https://www.cbc.ca/lite/">CBC Low Bandwidth (Canadian News)</a></li>
            <li><a href="https://www.reuters.com/news/archive/textonly">Reuters Text-Only</a></li>
            <li><a href="https://plaintextsports.com/">PlainTextSports (Sports News)</a></li>
            <li><a href="https://libreddit.pussthecat.org/">LibReddit (Lightweight Reddit Frontend)</a></li>
            <li><a href="https://newsasfacts.com/">News As Facts (Concise World News)</a></li>
            <li><a href="https://currentevents.email/">Current Events (Wikipedia's Current Events)</a></li>
            <li><a href="https://www.kompas.com/">Kompas.com (Indonesian General News)</a></li>
            <li><a href="https://www.detik.com/">Detik.com (Indonesian Breaking News)</a></li>
        </ul>
    </div>

    <div class="section">
        <h2>News and Community/Forum Aggregators in Indonesia</h2>
        <ul>
            <li><a href="https://en.antaranews.com/">ANTARA News (Official Indonesian News Agency)</a></li>
            <li><a href="https://jakartaglobe.id/">Jakarta Globe (English News from Indonesia)</a></li>
        </ul>
    </div>

    <div class="section">
        <h2>News and Community/Forum Aggregators in Japan (English)</h2>
        <ul>
            <li><a href="https://www.japantimes.co.jp/">The Japan Times (English News on Japan)</a></li>
            <li><a href="https://www.aljazeera.com/topics/country/japan.html">Al Jazeera - Japan (English News on Japan from Al Jazeera)</a></li>
        </ul>
    </div>

    <div class="section">
        <h2>Weather and Disaster Information/Forecasts (Static Links)</h2>
        <h3>Japan</h3>
        <ul>
            <li><a href="https://www.jma.go.jp/jma/en/Emergency_Warning/ew_index.html">Japan Meteorological Agency (JMA) Emergency Warning System</a></li>
            <li><a href="https://www.jma.go.jp/jma/en/Activities/tsunami.html">JMA Tsunami Warnings/Advisories</a></li>
            <li><a href="https://www.jma.go.jp/jma/en/Activities/earthquake.html">JMA Earthquake Information</a></li>
            <li><a href="https://www.jma.go.jp/jma/en/Activities/volcano.html">JMA Volcanic Warnings/Forecasts</a></li>
            <li><a href="https://www.jnto.go.jp/safety-tips/eng/">JNTO Safety Tips for Travelers (General Disaster Info)</a></li>
            <li><a href="https://wttr.in/Tokyo">Wttr.in (Text-only weather for Tokyo)</a></li>
        </ul>
        <h3>Jakarta, Indonesia</h3>
        <ul>
            <li><a href="https://pantaubanjir.jakarta.go.id/">Pantau Banjir Jakarta (Flood Monitoring Dashboard)</a></li>
            <li><a href="https://bpbd.jakarta.go.id/waterlevel">BPBD DKI Jakarta (Water Level Monitoring)</a></li>
            <li><a href="https://smartcity.jakarta.go.id/en/blog/gampang-cari-informasi-hujan-di-jakarta/">Jakarta Smart City - Rain Information Channels</a></li>
            <li><a href="https://wttr.in/Jakarta">Wttr.in (Text-only weather for Jakarta)</a></li>
        </ul>
    </div>

    <div class="section">
        <h2>Finding Stuff / Search Engines</h2>
        <ul>
            <li><a href="https://frogfind.com/">FrogFind (Search engine for vintage computers/text-only browsers)</a></li>
            <li><a href="https://68k.news/">68k.news (Simplified HTML news aggregator for retro computers)</a></li>
            <li><a href="https://www.google.com/search?q=">Google Search (Basic Interface)</a></li>
            <li><a href="https://duckduckgo.com/">DuckDuckGo (Privacy-focused search)</a></li>
            <li><a href="https://www.bing.com/">Bing (Microsoft Search Engine)</a></li>
            <li><a href="https://search.brave.com/">Brave Search (Independent, privacy-preserving search)</a></li>
            <li><a href="https://www.startpage.com/">Startpage (Google results with privacy)</a></li>
            <li><a href="https://www.mojeek.com/">Mojeek (Independent search engine)</a></li>
            <li><a href="https://searx.be/">SearXNG (Privacy-respecting metasearch engine)</a></li>
            <li><a href="https://www.dogpile.com/">Dogpile (Metasearch engine)</a></li>
            <li><a href="https://www.ask.com/">Ask.com (Question-and-answer focused search)</a></li>
            <li><a href="https://www.wolframalpha.com/">WolframAlpha (Computational knowledge engine)</a></li>
            <li><a href="https://archive.org/web/">Wayback Machine (Internet Archive)</a></li>
            <li><a href="https://theoldnet.com/">The Old Net (Browse the web as it was in the past)</a></li>
        </ul>
    </div>
"""

# --- Helper Functions ---

def fetch_url_with_retry(url, retries=3, delay=1):
    """Fetches a URL with exponential backoff."""
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            if i < retries - 1:
                time.sleep(delay * (2 ** i)) # Exponential backoff
            else:
                return None
    return None

def get_weather(city):
    """Fetches text-only weather from wttr.in for a given city."""
    url = f"https://wttr.in/{city}?T" # ?T for text-only output
    print(f"Fetching weather for {city} from {url}")
    # Using a more robust retry logic here to handle the specific wttr.in issues
    max_retries = 5
    base_retry_delay_seconds = 2  # Start with a 2-second delay
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            
            # Check for the specific concurrency error message
            if "This query is already being processed" in response.text:
                print(f"Attempt {attempt + 1}: Query is already being processed. Retrying.")
            elif response.status_code == 200:
                # If we get a good response, return the content
                import re
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                return ansi_escape.sub('', response.text).strip()
            else:
                # Handle other non-200 responses
                print(f"Attempt {attempt + 1}: Received status code {response.status_code}. Retrying.")

        except requests.exceptions.RequestException as e:
            # Handle connection errors and timeouts
            print(f"Attempt {attempt + 1}: An error occurred: {e}")
        
        # If we're not on the last attempt, calculate the delay and wait
        if attempt < max_retries - 1:
            retry_delay = base_retry_delay_seconds * (2 ** attempt)
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Giving up.")
            break
            
    return "Weather data not available."


def parse_rss_feed(url):
    """Fetches and parses an RSS feed."""
    print(f"Starting parse for RSS feed: {url} at {datetime.datetime.now()}")
    articles = []
    feed_content = fetch_url_with_retry(url)
    if feed_content:
        feed = feedparser.parse(feed_content)
        for entry in feed.entries:
            title = getattr(entry, 'title', 'No Title').strip()
            link = getattr(entry, 'link', '#').strip()
            published_parsed = getattr(entry, 'published_parsed', None)
            published_date = None
            if published_parsed:
                published_date = datetime.datetime(*published_parsed[:6], tzinfo=datetime.timezone.utc)
            
            articles.append({
                'title': title,
                'link': link,
                'published': published_date,
                'source': feed.feed.title if hasattr(feed.feed, 'title') else url
            })
        print(f"Finished parse for RSS feed: {url} at {datetime.datetime.now()}")
    else:
        print(f"Skipping parse for RSS feed: {url} due to fetch error.")
    return articles

def get_all_news():
    """Fetches and aggregates news from all configured RSS feeds."""
    all_articles = []
    for feed_url in RSS_FEEDS:
        articles = parse_rss_feed(feed_url)
        all_articles.extend(articles)
    
    all_articles = [a for a in all_articles if a['published']]
    all_articles.sort(key=lambda x: x['published'], reverse=True)
    return all_articles

def convert_utc_to_jakarta(dt_utc):
    if dt_utc is None:
        return None
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=datetime.timezone.utc)
    
    jakarta_offset = datetime.timedelta(hours=7)
    return dt_utc + jakarta_offset

def generate_homepage_html(jakarta_weather, tokyo_weather, news_articles):
    """Generates the HTML content for the main homepage."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text-Only Portal</title>
    <style>
        body {{ font-family: monospace; line-height: 1.6; margin: 20px; background-color: #f0f0f0; color: #333; }}
        h1, h2 {{ color: #000; border-bottom: 1px solid #999; padding-bottom: 5px; margin-top: 20px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 5px; }}
        a {{ color: #0000ee; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .section {{ margin-bottom: 30px; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <h1>Welcome to Your Text-Only Portal</h1>
    <p>This page provides dynamic content optimized for text-based browsers like Lynx.</p>

    <div class="section">
        <h2>Current Weather</h2>
        <h3>Jakarta, Indonesia</h3>
        <pre>{jakarta_weather}</pre>
        <h3>Tokyo, Japan</h3>
        <pre>{tokyo_weather}</pre>
    </div>

    <div class="section">
        <h2>Latest 10 News</h2>
        <ul>
    """.format(jakarta_weather=jakarta_weather, tokyo_weather=tokyo_weather)

    for i, article in enumerate(news_articles[:10]):
        display_date = "N/A"
        if article['published']:
            jakarta_time = convert_utc_to_jakarta(article['published'])
            if jakarta_time:
                display_date = jakarta_time.strftime('%Y-%m-%d %H:%M')
        html_content += f"            <li>[{display_date}] <a href=\"{article['link']}\">{article['title']}</a> (Source: {article['source']})</li>\n"
    
    html_content += """        </ul>
        <p><a href="/news_archive.html">View All News (Last 72 Hours)</a></p>
    </div>

    """ + STATIC_LINKS_CONTENT + """
</body>
</html>"""
    return html_content

def generate_news_archive_html(news_articles):
    """Generates the HTML content for the news archive page."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All News (Last 72 Hours)</title>
    <style>
        body {{ font-family: monospace; line-height: 1.6; margin: 20px; background-color: #f0f0f0; color: #333; }}
        h1, h2 {{ color: #000; border-bottom: 1px solid #999; padding-bottom: 5px; margin-top: 20px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 5px; }}
        a {{ color: #0000ee; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .section {{ margin-bottom: 30px; }}
    </style>
</head>
<body>
    <h1>All News from the Last 72 Hours</h1>
    <p>This page lists all aggregated news articles from the past 72 hours.</p>
    <p><a href="/index.html">Back to Homepage</a></p>

    <div class="section">
        <ul>
    """
    
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    seventy_two_hours_ago = now - datetime.timedelta(hours=72)

    recent_news = [
        article for article in news_articles 
        if article['published'] and article['published'] >= seventy_two_hours_ago
    ]

    if not recent_news:
        html_content += "            <li>No news found for the last 72 hours.</li>\n"
    else:
        for article in recent_news:
            display_date = "N/A"
            if article['published']:
                jakarta_time = convert_utc_to_jakarta(article['published'])
                if jakarta_time:
                    display_date = jakarta_time.strftime('%Y-%m-%d %H:%M')
            html_content += f"            <li>[{display_date}] <a href=\"{article['link']}\">{article['title']}</a> (Source: {article['source']})</li>\n"
    
    html_content += """        </ul>
        <p><a href="/index.html">Back to Homepage</a></p>
    </div>
</body>
</html>"""
    return html_content

def update_static_site(event, context):
    """
    Background Cloud Function to generate and upload static HTML files to a GCS bucket.
    This function is triggered by a Pub/Sub message from a Cloud Scheduler cron job.
    """
    print("Starting static site generation and upload...")
    try:
        # Fetch data
        jakarta_weather = get_weather("Jakarta")
        tokyo_weather = get_weather("Tokyo")
        all_news = get_all_news()

        # Generate HTML content
        homepage_html = generate_homepage_html(jakarta_weather, tokyo_weather, all_news)
        news_archive_html = generate_news_archive_html(all_news)

        # Upload files to GCS
        print(f"Uploading files to GCS bucket: {GCS_BUCKET_NAME}")

        homepage_blob = gcs_bucket.blob('index.html')
        homepage_blob.upload_from_string(homepage_html, content_type='text/html')
        print("Uploaded index.html successfully.")

        news_archive_blob = gcs_bucket.blob('news_archive.html')
        news_archive_blob.upload_from_string(news_archive_html, content_type='text/html')
        print("Uploaded news_archive.html successfully.")
        
        return 'Success!', 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Error!', 500
