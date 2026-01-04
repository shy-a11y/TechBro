import requests
import sys
from bs4 import BeautifulSoup


sys.stdout.reconfigure(encoding='utf-8')
def get_tech_news():
    """
    Crawls the latest tech news from Hacker News.
    Returns a list of dictionaries containing title, link, and content.
    """
    url = "https://news.ycombinator.com/"
    headers = {
        # User-Agent header to mimic a real browser request
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send GET request to the URL
    response = requests.get(url, headers=headers)
    
    # Set encoding to utf-8 explicitly to handle special characters correctly
    response.encoding = 'utf-8'
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # In Hacker News, articles are contained in <tr> tags with class 'athing'
    articles = soup.find_all('tr', class_='athing')
    
    print(f"DEBUG: Found {len(articles)} articles from Hacker News.")

    news_list = []

    for i, article in enumerate(articles):
        try:
            # 1. Find the tag containing the title and link (.titleline > a)
            # The structure involves a span with class 'titleline' which contains the anchor tag
            title_line = article.find('span', class_='titleline')
            if not title_line:
                continue
                
            link_tag = title_line.find('a')
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            
            # 2. Store the extracted data
            # Hacker News main page doesn't provide summaries, so we set content to "Link Only"
            news_data = {
                "title": title,
                "link": link,
                "content": "Link Only" 
            }
            news_list.append(news_data)

        except Exception as e:
            # Print error message with index if extraction fails
            print(f"[{i}] Error: {e}")

    return news_list

if __name__ == "__main__":
    # Execute the crawler
    latest_news = get_tech_news()
    
    print(f"\n--- Collected {len(latest_news)} Articles from Hacker News ---")
    
    if len(latest_news) == 0:
        print("No data collected.")
    else:
        # Print the top 5 collected news items to verify
        for news in latest_news[:5]:
            print(f"Title: {news['title']}")
            print(f"Link: {news['link']}")
            print("-" * 30)