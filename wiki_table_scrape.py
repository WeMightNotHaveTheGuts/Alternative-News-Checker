import requests
from bs4 import BeautifulSoup
import re


url = "https://en.wikipedia.org/wiki/List_of_fake_news_websites"

res = requests.get(url)
res.raise_for_status() #raises an exception for error codes#
wikiPage = BeautifulSoup(res.text, "html.parser")
websites = wikiPage.select('.wikitable')
rows = websites[0].select('td')
rows_text= []
fake_wiki_data= []
for i in range(len(rows)):
    if i % 3 != 2:
        rows_text.append(rows[i].getText()) # implement re.sub before this to get rid of references
for j in range(0, len(rows_text), 2):
     fake_wiki_data.append([rows_text[j], rows_text[j+1]])

print fake_wiki_data[1]

