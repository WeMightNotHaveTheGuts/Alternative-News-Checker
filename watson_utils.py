import requests, json, pprint
from watson_developer_cloud import ToneAnalyzerV3
from bs4 import BeautifulSoup
import article_parser

tone_analyzer = ToneAnalyzerV3(
  url= "https://gateway.watsonplatform.net/tone-analyzer/api",
  username= "4e1af779-0c5e-4f65-b0c7-64979b16add3",
  password= "xtY7TjcN2HxW",
  version='2016-05-19')

def get_article_emotions(url):
    dict = {}

    article_text = article_parser.get_article_text(url)
    if not article_text: return None
    data = tone_analyzer.tone(article_text)
    pp = pprint.PrettyPrinter(indent=4)
    data1 = data['document_tone']['tone_categories'][0]['tones']
    data2 = data['document_tone']['tone_categories'][1]['tones']
    for i in data1:
        dict.update({str(i['tone_name']):i['score']})
    for i in data2:
        dict.update({str(i['tone_name']):i['score']})
    return dict
