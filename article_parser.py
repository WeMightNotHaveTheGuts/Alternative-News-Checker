from goose import Goose

def get_article_text(url):
    g = Goose()
    article = g.extract(url=url)
    return article.cleaned_text

def get_article_headline(url):
    g = Goose()
    article = g.extract(url=url)
    return article.title