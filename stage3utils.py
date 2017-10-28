import requests
from bs4 import BeautifulSoup
import re
from collections import deque
import urllib2

article_title = ""


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

#Checking if the URL is legit

#Getting all links from the URL then seeing if there are any sources/if
#any credible sources -- Note that this very inefficient

#Getting credibility of sources

#Reliability: 0 = No sources on each side; 1 = Ligit sources; 2 = https with unreal sources
#             3 = no https unreal sources; 4 = has both real and unreal sources

def getAllLinks (url):
    reliability = 0
    website = urllib2.urlopen(url)
    html = website.read()
    allLinks = re.findall('"((http|ftp)s?://.*?)"', html)
    links = [seq[0] for seq in allLinks ]
    print links

    if sourcesReliable(url, links) == True and unReliableSources(url, links) == True:
        reliability = 4
    elif sourcesReliable(url, links) == True:
        reliability = 1
    elif unReliableSources(url, links) == True:
        if "https" in url:
            reliability = 2
        else:
            reliability = 3
    else:
        reliability = 0

    print reliability
#Refined for empty set rtee, needs to be its own func as other url must have protocols!
def url_summariseR(headline):
    headline = re.split(r"[- |, /]", headline) #Removes -'s and /'s from URL
    if len(headline) == 1:
        return headline
    for i in range(2):
        headline.pop(0) # removes blank list entry and http
        if len(headline) == 1:
            return headline
    if ".html" or ".htm" or ".php" in headline[0,-1]: # removes file endings if there are any
        headline.pop(-1)
    for i in headline:
        i = i.lower()
    return headline

def sourcesReliable (url, links):
    hasReliableSources = False
    reliableSites = []

    # Load the list of reliable news sites from file
    with open("ReliableNewsWebsites.txt") as in_file:
        for site in in_file.readlines():
            reliableSites.append(site.strip())

    for link in links:
        for site in reliableSites:
            if site.contains(url_summariseR(link)[0].replace("www.","")):
        print

    """

    for i in range(len(links)):
        thing = url_summariseR(links[i-1])
        newThing = thing[0]
        if "www." in newThing:
            newThing = newThing[4:]
        if newThing not in url:
            for line in file('ReliableNewsWebsites.txt'):
                if newThing in line:
                    reliableSources = True
    return reliableSources

    """

def unReliableSources (url, links):
    unreliable = False
    for i in range(len(links)):
        thing = url_summariseR(links[i-1])
        newThing = thing[0]
        if "www." in newThing:
            newThing = newThing[4:]
        if newThing not in url:
            for line in file('FakeNewsWebsite.txt'):
                if newThing in line:
                    unreliable = True
    return unreliable

getAllLinks("http://www.independent.co.uk/news/business/google-amazon-profits-latest-earning-reports-billions-a8022286.html")
#website("http://www.independent.co.uk/news/uk/politics/jeremy-corbyn-sexual-assault-is-parliament-thrives-mps-politicians-a8024026.html")
#website("https://www.infowars.com/joy-villa-for-congress-trump-approves/")
#website("http://www.bbc.co.uk/news/world-europe-41785292")
