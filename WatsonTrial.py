import requests, json, pprint
from watson_developer_cloud import ToneAnalyzerV3
from bs4 import BeautifulSoup

tone_analyzer = ToneAnalyzerV3(
  url= "https://gateway.watsonplatform.net/tone-analyzer/api",
  username= "4e1af779-0c5e-4f65-b0c7-64979b16add3",
  password= "xtY7TjcN2HxW",
  version='2016-05-19')

def getwebsitebody(url):
    dict = {}
    res = requests.get(url)
    res.raise_for_status()
    content = BeautifulSoup(res.text, "html.parser")
    body_text = str(content.find('body'))
    body_text = BeautifulSoup(body_text, "html.parser")
    ptag = str(body_text.select('p'))
    ptag = BeautifulSoup(''.join(ptag), "html.parser").getText()
    data = tone_analyzer.tone(ptag)
    pp = pprint.PrettyPrinter(indent=4)
    data1 = data['document_tone']['tone_categories'][0]['tones']
    data2 = data['document_tone']['tone_categories'][1]['tones']
    for i in data1:
        dict.update({str(i['tone_name']):i['score']})
    for i in data2:
        dict.update({str(i['tone_name']):i['score']})
    print dict



getwebsitebody("http://www.breitbart.com/tech/2017/10/27/guardian-rise-lgbt-conservatives-troubling/")
