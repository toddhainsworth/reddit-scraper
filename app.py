from bs4 import BeautifulSoup
import requests

import sys

BASE_URL = "http://www.reddit.com/r/{}"
USER_AGENT = "Reddit meme scraper"
DEFAULT_SUB = "politics"
DEFAULT_SORT = "top"

QUERY_STRING_TODAY = "t=day" # equals symbol intentional ;)
QUERY_STRING_SORT = "sort={}"
VALID_SORTS = [
    "hot", "new", "rising", "controversial", "top", "gilded"
]

"""
Get the sub requested from the command-line args or use the default
"""
def get_sub():
  args = sys.argv
  sub = args[1] if len(args) > 1 else DEFAULT_SUB
  return sub

"""
Get the sort field requested from the command-line args or use the default
"""
def get_sort():
  args = sys.argv
  sort = args[2] if len(args) > 2 else DEFAULT_SORT
  sort = sort if sort in VALID_SORTS else DEFAULT_SORT
  return sort

"""
Perform the various formats to generate the url
"""
def format_url(sub, sort):
  url = BASE_URL.format(sub)
  query = "sort={}&{}".format(sort, QUERY_STRING_TODAY)
  url = "{}/{}/?{}".format(url, sort, query)
  print(url)
  return url

"""
Structure and send a request for the given sub
"""
def request(sub, sort):
  url = format_url(sub, sort)
  return requests.get(url, headers={"User-agent": USER_AGENT})

"""
Take the given response and get the anchors titles and hrefs
"""
def translate_response(response):
  soup = BeautifulSoup(response.text, "html.parser")
  links = list(map(get_title_and_url, soup.find_all("a", {"class": "title"})))
  return links

"""
Take the given link and get the title and href
"""
def get_title_and_url(link):
  return {"title": link.string, "link": link.get("href")}

"""
Scrape the given sub for each of it"s entries
"""
def scrape_sub(sub, sort):
  resp = request(sub, sort=sort)
  links = translate_response(resp)
  return links

sub = get_sub()
sort = get_sort()

print("Scraping r/{} - please hold...".format(sub))
print("Sorting by \"{}\"".format(sort))

politics_links = scrape_sub(sub, sort)
print(politics_links[0])
