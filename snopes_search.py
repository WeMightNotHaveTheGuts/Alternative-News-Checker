import platform
from bs4 import BeautifulSoup
from selenium import webdriver

def search_for_factchecks(headline_keywords):
    """
    takes a list of article headline keywords, joins them with + in between, searches it on Snopes,
    check if there are any sufficiently relevant results (contains most of searched words). If so,
    go to the page and get the verdict.

    Eventually display rating and link to article for the user.
    """

    # String together the search url + the search query consisting of keywords in the original article
    search_terms = "+".join(headline_keywords)
    search_url = "https://www.snopes.com/?s=" + search_terms
    print search_url

    # Checking for platform to use the appropriate phantomjs browser path
    if platform.system() == 'Windows':
        PHANTOMJS_PATH = './phantomjs.exe'
    else:
        PHANTOMJS_PATH = './phantomjs'

    # Create a new browser, go to the search url, get the contents
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    browser.get(search_url)

    # Load the contents to BS, first find all search results
    soup = BeautifulSoup(browser.page_source, "html.parser")
    most_relevant_result = soup.select("#result-list .ais-hits--item a")[0]

    # The first result in the search is always the most relevant one
    mrr_soup = BeautifulSoup(str(most_relevant_result), "html.parser")
    factchecking_url = mrr_soup.find("a")["href"]
    matching_words = mrr_soup.find_all("em")

    # How many words in the most relevant search result match the headline keywords?
    # If it is more than half, the search result is likely related to the article we are fact checking
    relevance = len(matching_words) / float(len(headline_keywords))
    if relevance > 0.5:
        return(truth_rating_fetch(browser, factchecking_url))

def truth_rating_fetch(browser, url):
    # The dictionary of all possible truth ratings
    ratings = {"claim false" : "FALSE",
               "claim true" : "TRUE",
               "claim mixture" : "MIXTURE"}
    browser.get(url)

    # Fetch the fact checking page
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # If we find any of the possible ratings on that page then that story has to be rated in that way
    for rating in ratings:
        if soup.find(class_=rating) != None: return ratings[rating]

#snopes_search(['Delingpole', '400', 'Scientific', 'Papers', '2017', 'Global', 'Warming', 'Myth'])
#snope_search(["global", "warming"])