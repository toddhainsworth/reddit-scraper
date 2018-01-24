from bs4 import BeautifulSoup
import requests

BASE_URL = "http://www.reddit.com/{}"
USER_AGENT = 'Reddit meme scraper'

def get_title_and_url(link):
  return {'title': link.string, 'link': link.get('href')}

def scrape_sub(sub):
  url = BASE_URL.format(sub)
  resp = requests.get(url, headers={'User-agent': USER_AGENT})
  soup = BeautifulSoup(resp.text, 'html.parser')
  links = list(map(get_title_and_url, soup.find_all('a', {'class': 'title'})))
  return links

politics_links = scrape_sub("r/politics")
