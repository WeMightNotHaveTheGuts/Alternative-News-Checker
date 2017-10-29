from urlparse import urlparse, re


"""
In the second stage we extract the website domain name and compare it to our databases of Fake/Real news websites.
If there is a match, we can say that the article is real/fake news with reasonably high confidence.
"""

def isolate_domain_name(url):
    if "http" in url or "https" in url:
        if urlparse(url[url.index("http"):]).hostname != None:
            return urlparse(url[url.index("http"):]).hostname.replace("www.","")
        else:
            return ""
    else:
        if urlparse(url).hostname != None:
            return urlparse(url).hostname.replace("www.","")
        else:
            return ""



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

def satire_news_sites_match(site_name):
    satire_news_sites = []
    with open("SatireNewsWebsites.txt") as file:
        for site in file.readlines():
            satire_news_sites.append(site.strip().lower())

    return site_name in satire_news_sites