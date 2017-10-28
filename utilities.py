import validators

def is_url_valid(url):
    if validators.url(url): return True
    else: return False
