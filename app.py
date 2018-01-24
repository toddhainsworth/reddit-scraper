from bs4 import BeautifulSoup
import requests

import sys

BASE_URL = "http://www.reddit.com/{}"
USER_AGENT = 'Reddit meme scraper'
DEFAULT_SUB = "politics"

"""
Get the sub requested from the command-line args or use the default
"""
def get_args_sub():
  args = sys.argv
  sub = args[1] if len(args) > 1 else DEFAULT_SUB
  return sub

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

sub = get_args_sub()
print("Scraping r/{} - please hold...".format(sub))
politics_links = scrape_sub("r/{}".format(sub))
print(politics_links[0])
