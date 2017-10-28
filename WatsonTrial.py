import requests, json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
  url= "https://gateway.watsonplatform.net/tone-analyzer/api",
  username= "4e1af779-0c5e-4f65-b0c7-64979b16add3",
  password= "xtY7TjcN2HxW",
  version='2016-05-19')

data = json.dumps(tone_analyzer.tone(text='I am very happy. It is a good day.'))
dicti = json.loads(data)
