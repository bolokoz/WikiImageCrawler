from bs4 import BeautifulSoup

import urllib2 
url = urllib2.urlopen("https://zh-yue.wikipedia.org/wiki/%E5%B8%83%E7%94%B8")

content = url.read()

soup = BeautifulSoup(content,"html.parser")

link = soup.findAll("html")

lang = ((soup.findAll('html'))[0]).get('lang')
# lang_http = ((soup.findAll(attrs={"rel":"canonical"})))[0].get('href')
lang_http = soup.find(rel='canonical').get('href')
print lang_http


# for id in soup.find(id='t-wikibase'):
#     wikidata_link = (id.get('href'))
# wikidata_id = wikidata_link.split('/', 4)[4]
wikidata_link = soup.find(id='t-wikibase').next.get('href')
wikidata_id = wikidata_link.split('/', 4)[4]

print("lang", lang)
print("lang_http", lang_http)
print("wikidata", wikidata_id)
