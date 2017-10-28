import requests
from bs4 import BeautifulSoup
from headline_summarise import summarise
def snope_search(headline_summary):
    """
    takes a list of main words (from summarise()), joins them with + in between, searches it on Snopes,
    check if there are any sufficiently relevant results (contains most of searched words). If so,
    go to the page and get the verdict.

    Eventually display rating and link to article for the user.
    """
    search_terms = "+".join(headline_summary)
    search_url = "https://www.snopes.com/?s=" + search_terms
    res = requests.get(search_url)
    res.raise_for_status()
    snopes_page = BeautifulSoup(res.text, "html-parser")
    snopes_page_results = snopes_page.select(.search-result-post)
    



snope_search(summarise("Flight Crew Takes A Knee And Walks Off, Leaving New Orleans Saints Stranded On Runway"))
