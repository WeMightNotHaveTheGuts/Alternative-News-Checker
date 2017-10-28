import requests
from bs4 import BeautifulSoup

def getwebsitebody(url):
    res = requests.get(url)
    res.raise_for_status()
    content = BeautifulSoup(res.text, "html.parser")
    body_text = str(content.find('body'))
    body_text = BeautifulSoup(body_text)
    ptag = str(body_text.select('p'))
    ptag = BeautifulSoup(''.join(ptag))
    print(ptag.getText())


getwebsitebody("http://www.independent.co.uk/sport/football/international/england-win-under-17-world-cup-vs-spain-phil-foden-rhian-brewster-gibbs-white-a8025086.html")
