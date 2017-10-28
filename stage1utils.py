import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from main import *

"""
In the first stage we take the keywords from the headline of the checked article and we try to figure out whether
the article has been fact checked at Snopes.com
If so, we try to get to the Snopes reference and fetch its truth rating
"""

def initialize_browser():
    if platform.system() == 'Windows':
        PHANTOMJS_PATH = './phantomjs.exe'
    else:
        PHANTOMJS_PATH = './phantomjs'

    # Create a new browser that will be used to scrape pages
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    return browser

def find_snopes_reference(browser, search_url):
    browser.get(search_url)
    # Load the contents to BS, first find all search results
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # The first result in the search is always the most relevant one
    try:
        most_relevant_result = soup.select("#result-list .ais-hits--item a")[0]
    except IndexError:
        return None

    return most_relevant_result

def find_factchecking_url(result):
    mrr_soup = BeautifulSoup(str(result), "html.parser")
    factchecking_url = mrr_soup.find("a")["href"]
    return factchecking_url

def find_matching_search_result_words(result):
    mrr_soup = BeautifulSoup(str(result), "html.parser")
    matching_words = mrr_soup.find_all("em")
    return matching_words

def calculate_relevance(keywords, matched_words):
    return len(matched_words) / float(len(keywords))

def fetch_rating(browser, factchecking_url):
    ratings = {"claim false": "FALSE",
               "claim true": "TRUE",
               "claim mixture": "MIXTURE",
               "claim mtrue" : "MOSTLY TRUE",
               "claim mfalse": "MOSTLY FALSE"}
    browser.get(factchecking_url)

    # Fetch the fact checking page
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # If we find any of the possible ratings on that page then that story has to be rated in that way
    for rating in ratings:
        if soup.find(class_=rating) != None: return ratings[rating]
    return "UNKNOWN"
