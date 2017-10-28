import requests
from bs4 import BeautifulSoup
import re
from collections import deque

def Website(url):
    res = requests.get(url)
    res.raise_for_status()
    content = BeautifulSoup(res.text, "html.parser")
    elems = content.select('h1')
    value = longestValue(elems)
    URLCheck(url, value)

def longestValue(elems):
    longest = ""
    for i in elems:
        i = i.getText()
        if len(i) > len(longest):
            longest = i
    return longest

def summarise(headline):
    """given a headline in a string, returns a list containing the main words in that headline.
    Useful for doing things such as finding the headline on other websites."""
    head_words = headline.split(" ") # get each word individually
    headline_summary = []
    with open("stopwords.csv") as s:
        stop = s.read()
        for word in head_words:
            word = re.sub('\W', '', word)  # strip non-alphanumeric characters from word
            if word not in stop:  # don't include any stopwords
                headline_summary.append(word)
    return headline_summary

def urlsummarise(headline):
    headline = re.split(r"[- |, /]", headline)
    for i in range(2):
        headline.pop(0)
    if ".html" or ".htm" or ".php" in headline[0,-1]:
        headline.pop(-1)
    return headline

def URLCheck(url, longest):
    value = summarise(longest)
    urlSum = urlsummarise(url)
    domain = urlSum[0]
    urlSum.pop(0)
    if value == urlSum:
        print "True"
    else:
        print "False"


Website("http://www.independent.co.uk/news/business/google-amazon-profits-latest-earning-reports-billions-a8022286.html")
Website("http://www.independent.co.uk/news/uk/politics/jeremy-corbyn-sexual-assault-is-parliament-thrives-mps-politicians-a8024026.html")
Website("https://www.infowars.com/joy-villa-for-congress-trump-approves/")
Website("http://www.milngavieherald.co.uk/news/could-you-give-bruiser-his-forever-home-1-4598319")
