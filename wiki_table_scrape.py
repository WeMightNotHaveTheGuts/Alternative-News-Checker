import requests
from bs4 import BeautifulSoup
import re


url = "https://en.wikipedia.org/wiki/List_of_fake_news_websites"

res = requests.get(url)
res.raise_for_status()  # raises an exception for error codes
wikiPage = BeautifulSoup(res.text, "html.parser")
websites = wikiPage.select('.wikitable')
rows = websites[0].select('td')
rows_text = []
fake_wiki_data = []
for i in range(len(rows)):
    if i % 3 != 2:  # only get rows that aren't in the sources column
        rows_text.append(re.sub("\[\d*\]", "", rows[i].getText()))  # implement re.sub before this to get rid of references
for j in range(0, len(rows_text), 2):
    fake_wiki_data.append([rows_text[j], rows_text[j+1]])

url = "https://en.wikipedia.org/wiki/List_of_satirical_news_websites"

res = requests.get(url)
res.raise_for_status()
wikiPage = BeautifulSoup(res.text, "html.parser")
websites = wikiPage.select('.wikitable')
rows = websites[0].select('td')
joke_wiki_data = []
for i in range(len(rows)):
    if i % 3 == 0:
        joke_wiki_data.append(rows[i].getText())

# fake_wiki_data - list of fake sites with some notes for each site, in a list of 2-element lists.
# joke_wiki_data - list of known satirical sites
