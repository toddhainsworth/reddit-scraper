from bs4 import BeautifulSoup
import requests

BASE_URL = "http://www.reddit.com/{}"
USER_AGENT = 'Reddit meme scraper'

"""
Structure and send a request for the given URL
"""
def request(url):
  return requests.get(url, headers={'User-agent': USER_AGENT})

"""
Take the given response and get the anchors titles and hrefs
"""
def translate_response(response):
  soup = BeautifulSoup(response.text, 'html.parser')
  links = list(map(get_title_and_url, soup.find_all('a', {'class': 'title'})))
  return links

"""
Take the given link and get the title and href
"""
def get_title_and_url(link):
  return {'title': link.string, 'link': link.get('href')}

"""
Scrape the given sub for each of it's entries
"""
def scrape_sub(sub):
  resp = request(BASE_URL.format(sub))
  links = translate_response(resp)
  return links

politics_links = scrape_sub("r/politics")
