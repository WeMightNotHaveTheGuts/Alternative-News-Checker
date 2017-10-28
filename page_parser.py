import requests
from bs4 import BeautifulSoup
import re
from collections import deque

article_title = ""

def website(url): # Runs other functions
    global article_title
    res = requests.get(url)
    res.raise_for_status()
    content = BeautifulSoup(res.text, "html.parser")
    elems = content.select('h1')
    value = longest_value(elems)
    article_title = ''.join(value)
    URL_check(url, value)

def longest_value(elems): # Finds the longest h1 tag in the webpage.
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
                headline_summary.append(str(word).lower())
    return headline_summary

def url_summarise(headline):
    headline = re.split(r"[- |, /]", headline) #Removes -'s and /'s from URL
    for i in range(2):
        headline.pop(0) # removes blank list entry and http
    if ".html" or ".htm" or ".php" in headline[0,-1]: # removes file endings if there are any
        headline.pop(-1)
    for i in headline:
        i = i.lower()
    return headline

def URL_check(url, longest):
    global article_title
    occurences = 0
    value = summarise(longest)
    urlSum = url_summarise(url)
    domain = urlSum[0]
    urlSum.pop(0)
    for i in value:
        if i in urlSum:
            occurences += 1
    if occurences > len(value)/4:
        print "Article title is " + article_title
    else:
        print "Article title might be " + article_title


#website("http://www.independent.co.uk/news/business/google-amazon-profits-latest-earning-reports-billions-a8022286.html")
#website("http://www.independent.co.uk/news/uk/politics/jeremy-corbyn-sexual-assault-is-parliament-thrives-mps-politicians-a8024026.html")
#website("https://www.infowars.com/joy-villa-for-congress-trump-approves/")
#website("http://www.bbc.co.uk/news/world-europe-41785292")
