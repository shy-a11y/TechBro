import requests
from bs4 import BeautifulSoup

def get_tech_news():
    url = "https://news.hada.io/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('div', class_='topic_row')
    print(f"DEBUG: Found {len(articles)} article blocks.") 

    news_list = []

    for i, article in enumerate(articles):
        try:
            
            title_div = article.find('div', class_='topictitle')
            if title_div is None:
                print(f"[{i}] Error: Could not find a div with the class 'topictitle'.")
                continue
            
            
            link_tag = title_div.find('a')
            if link_tag is None:
                print(f"[{i}] Error: There is no <a> tag inside 'topictitle'")
                continue

            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            
            if link.startswith('/'):
                link = "https://news.hada.io" + link
            
            desc_tag = article.find('div', class_='topicdesc')
            content = desc_tag.get_text(strip=True) if desc_tag else "No summary"
            
            news_data = {
                "title": title,
                "link": link,
                "content": content
            }
            news_list.append(news_data)

        except Exception as e:
            print(f"[{i}] Critical Error: {e}")

    return news_list

if __name__ == "__main__":
    latest_news = get_tech_news()
    
    print(f"\n--- Final Collection Results: {len(latest_news)}---")
    if len(latest_news) == 0:
        print("No data was collected. Please check the DEBUG messages above.")
    else:
        for news in latest_news[:3]:
            print(f"Title: {news['title']}")
            print(f"Link: {news['link']}")
            print("-" * 30)