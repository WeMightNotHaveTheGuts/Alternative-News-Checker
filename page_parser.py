import requests
from bs4 import BeautifulSoup
import re
from collections import deque
from BeautifulSoup import BeautifulSoup
import urllib2

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
    x = getAllLinks(url)
    y = isURLCredible(url)
    
    while switch(x):
        if case(1):
            print "The sources of this webpage are credible"
            break
        if case(2):
            print "The sources of this page are unreliable"
            break
        if case(3):
            print "The sources of this page are not only unreliable but this webpage isn't even secure"
            break
        if case(4):
            print "Thi webpage contains some credible and fake news websites as its references"
            break
        break
    
    while switch(y):
        if case(1):
            print "This webpage belongs to a website that produces fake news"
            break
        if case(2):
            print "This webpage belongs to a website that produces highly credible information"
            break
        break

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

#isLigitURL: 0 = Neither; 1 = Unreliable; 2 = Reliable

def isURLCredible(URL):
    substrl = url_summarise(URL)
    substrll = substrl[0]
    if "www." in substrll:
        substr = substrll[4:]
    isLigitURL = 0
    fakeURLList = file('FakeNewsWebsite.txt')
    ligitURLList = file('ReliableNewsWebsites.txt')
    for line in fakeURLList:
        if substr in line:
            isLigitURL = 1
    for line in ligitURLList:
        if substr in line:
            isLigitURL = 2
    return isLigitURL

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
    reliableSources = False
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

#website("http://www.independent.co.uk/news/business/google-amazon-profits-latest-earning-reports-billions-a8022286.html")
#website("http://www.independent.co.uk/news/uk/politics/jeremy-corbyn-sexual-assault-is-parliament-thrives-mps-politicians-a8024026.html")
#website("https://www.infowars.com/joy-villa-for-congress-trump-approves/")
#website("http://www.bbc.co.uk/news/world-europe-41785292")