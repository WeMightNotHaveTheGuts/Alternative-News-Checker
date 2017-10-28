from urlparse import urlparse


"""
In the second stage we extract the website domain name and compare it to our databases of Fake/Real news websites.
If there is a match, we can say that the article is real/fake news with reasonably high confidence.
"""

def isolate_domain_name(url):
    return urlparse(url).hostname.replace("www.","")

def fake_news_sites_match(site_name):
    fake_news_sites = []
    with open("FakeNewsWebsite.txt") as file:
        for site in file.readlines():
            fake_news_sites.append(site.strip().lower())

    return site_name in fake_news_sites

def real_news_sites_match(site_name):
    real_news_sites = []
    with open("ReliableNewsWebsites.txt") as file:
        for site in file.readlines():
            real_news_sites.append(site.strip().lower())

    return site_name in real_news_sites