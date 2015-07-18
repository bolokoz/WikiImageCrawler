from bs4 import BeautifulSoup
import requests

import urllib2

url = urllib2.urlopen("https://de.wikipedia.org/wiki/Kategorie:Ort_auf_Usedom")

content = url.read()

soup = BeautifulSoup(content, "html.parser")

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
thumb_img=[]
href=[]
for link in soup.findAll('a', {'class': 'image'}):
    if (int(link.next.get('width')) > 70):
        thumb_img.append(str('https:' + link.next.get('src')))
        href.append(str(link.get('href')))
# print ("Found %d images:" % (len(href)))
# print "\n".join(thumb_img)
# print "\n".join(href)
print (dict(zip(thumb_img, href)))


