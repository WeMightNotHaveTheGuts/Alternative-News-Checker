from goose import Goose

def get_article_text(url):
    g = Goose()
    article = g.extract(url=url)
    print article.meta_keywords
    return article.cleaned_text

def get_article_headline(url):
    g = Goose()
    article = g.extract(url=url)
    return article.title

def get_article_links(url):
    g = Goose()
    article = g.extract(url=url)
    return article.links