import requests
from bs4 import BeautifulSoup

def Website(url):
    res = requests.get(url)
    res.raise_for_status()
    content = BeautifulSoup(res.text, "html.parser")
    elems = content.select('h1')
    value = longestValue(elems)

def longestValue(elems):
    longest = ""
    for i in elems:
        i = i.getText()
        if len(i) > len(longest):
            longest = i
    print longest


Website("http://www.independent.co.uk/news/business/google-amazon-profits-latest-earning-reports-billions-a8022286.html")
Website("http://www.independent.co.uk/news/uk/politics/jeremy-corbyn-sexual-assault-is-parliament-thrives-mps-politicians-a8024026.html")
Website("https://www.infowars.com/joy-villa-for-congress-trump-approves/")
Website("http://www.milngavieherald.co.uk/news/could-you-give-bruiser-his-forever-home-1-4598319")
