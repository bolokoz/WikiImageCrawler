from multiprocessing.pool import ThreadPool
import urllib2

__author__ = 'Yuri'
import requests
import thread
from bs4 import BeautifulSoup
import collections


def get_images_from_soup(soup, min_width=0):
    thumb_img = []
    href = []
    for link in soup.findAll('a', {'class': 'image'}):
        if(int(link.next.get('width')) > min_width):
            thumb_img.append(str('https:' + link.next.get('src')))
            href.append(str(link.get('href')))
    # print ("Found %d images:" % (len(href)))
    # print "\n".join(thumb_img)
    # print "\n".join(href)
    return (dict(zip(thumb_img, href)))


def get_images_from_url(url, min_width=0):
    thumb_img = []
    href = []
    img = {}
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('a', {'class': 'image'}):
        if (int(link.next.get('width')) > min_width):
            thumb_img.append(str('https:' + link.next.get('src')))
            href.append(str(link.get('href')))
    # print ("Found %d images:" % (len(href)))
    # print "\n".join(thumb_img)
    # print "\n".join(href)
    return (dict(zip(thumb_img, href)))


def write_csv(all_lang_dict, wikidata_id, min_width=0):
    # will make the IMAGES_DB
    # csv in the following format:
    # wikidata_id, lang, lang_http, thumb_img, img
    with open('IMAGES_DB.csv', 'w') as f:
        for x in all_lang_dict:
            url = (str(all_lang_dict[x]))
            print url
            thumb_img_dict = get_images_from_url(url, min_width)
            for row in thumb_img_dict:
                id = wikidata_id
                lang = str(x)
                lang_http = str(all_lang_dict[x])
                thumb_img_http = row
                img_http = lang_http.split('/w', 2)[0] + thumb_img_dict[row]
                # print("id", id)
                # print("lang", lang)
                # print("lang_http", lang_http)
                # print('thumb', thumb_img_http)
                # print("img_http",img_http)
                seq = (id, lang, lang_http, thumb_img_http, img_http)
                img = ';'.join(seq)
                # print img

                f.write(img + '\n')
    f.close()


def get_soups_POOL_from(all_lang_dict):
    all_lang_urls = all_lang_dict.values()
    htmls = []
    soups = []
    # Make the Pool of workers
    pool = ThreadPool(4)

    # Open the urls in their own threads
    # and return the results
    results = pool.map((urllib2.urlopen), all_lang_urls)


    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    for link in results:
        htmls.append(link.read())

    for html in htmls:
        soups.append(BeautifulSoup(html, "html.parser"))

    return soups

def get_info_from_soup(soup):
    #gets lang,link to lang, wikidata_id
    lang = ((soup.findAll('html'))[0]).get('lang')
    # lang_http = ((soup.findAll(attrs={"rel":"canonical"})))[0].get('href')
    lang_http = soup.find(rel='canonical').get('href')
    # for id in soup.find(id='t-wikibase'):
    #     wikidata_link = (id.get('href'))
    # wikidata_id = wikidata_link.split('/', 4)[4]
    wikidata_link = soup.find(id='t-wikibase').next.get('href')
    wikidata_id = wikidata_link.split('/', 4)[4]

    return lang,lang_http,wikidata_id

def write_csv_from_soups(soups):
    # will make the IMAGES_DB
    # csv in the following format:
    # wikidata_id, lang, lang_http, thumb_img, img
    with open('IMAGES_DB.csv', 'w') as f:
        for soup in soups:
            thumb_img_dict = get_images_from_soup(soup, 70) #min_width=70
            lang,lang_http,id = get_info_from_soup(soup)
            for row in thumb_img_dict:
                thumb_img_http = row
                img_http = lang_http.split('/w', 2)[0] + thumb_img_dict[row]
                # print("id", id)
                # print("lang", lang)
                # print("lang_http", lang_http)
                # print('thumb', thumb_img_http)
                # print("img_http",img_http)
                seq = (id, lang, lang_http, thumb_img_http, img_http)
                img = ';'.join(seq)
                print img

                f.write(img + '\n')
    f.close()


def write_csv_thread(all_lang_dict, wikidata_id, min_width=0):
    # will make the IMAGES_DB
    # csv in the following format:
    # wikidata_id, lang, lang_http, thumb_img, img
    img = []
    with open('IMAGES_DB.csv', 'w') as f:
        thumb_img_dict = get_images_from_dict_thread(all_lang_dict, wikidata_id, min_width)
        f.write(img + '\n')
    f.close()


def get_images_from_dict_thread(all_lang_dict, wikidata_id, min_width=0, ):
    for x in all_lang_dict:
        url = (str(all_lang_dict[x]))
        print "url acquired from dict"
        try:
            thumb_img_dict = thread.start_new_thread(get_images_from_url, (url, min_width))
            print "thread started"
            for row in thumb_img_dict:
                id = wikidata_id
                lang = str(x)
                lang_http = str(all_lang_dict[x])
                thumb_img_http = row
                img_http = lang_http.split('/w', 2)[0] + thumb_img_dict[row]
                # print("id", id)
                # print("lang", lang)
                # print("lang_http", lang_http)
                # print('thumb', thumb_img_http)
                # print("img_http",img_http)
                seq = (id, lang, lang_http, thumb_img_http, img_http)
                img = ';'.join(seq)
                # print img
        except:
            print "Error starting thread"


def get_wikidata_item_id(soup):
    for id in soup.find(id='t-wikibase'):
        wikidata_link = (id.get('href'))
    wikidata_id = wikidata_link.split('/', 4)[4]
    # print(wikidata_id)
    return (wikidata_id)


def get_languages_links(soup):
    language = []
    link = []
    language.append(((soup.findAll('html'))[0]).get('lang'))
    # lang_http = ((soup.findAll(attrs={"rel":"canonical"})))[0].get('href')
    link.append(soup.find(rel='canonical').get('href'))
    for row in soup.findAll('li', {'class': 'interlanguage-link'}):
        language.append(row.next.get('lang'))
        link.append('https:' + row.next.get('href'))
    # print(language)
    # print(link)
    all_lang_dict = collections.OrderedDict(sorted(dict(zip(language, link)).items()))

    return all_lang_dict


    # def get_languages(url):
    #    language = []
    #    link = []
    #    source_code = requests.get(url)
    #    plain_text = source_code.text
    #    soup = BeautifulSoup(plain_text, "html.parser")
    #    for row in soup.findAll('li', {'class': 'interlanguage-link'}):
    #        language.append(row.next.get('lang'))
    #        link.append('https:' + row.next.get('href'))
    #    # print(language)
    #    # print(link)
    #    return (dict(zip(language, link)))


def get_data(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    # print('Wikidata id'+ get_wikidata_item_id(soup))
    # print('images'+ (str(get_images(soup))))
    return (get_languages_links(soup))

def get_dict_lang_from_wikidata(wikidata_id):
    soup = get_soup_from_url("https://www.wikidata.org/wiki/Q" + str(wikidata_id))
    lang = []
    lang_http = []
    for link in soup.findAll('span', {"class": "wikibase-sitelinkview-page"}):
        lang.append(link.next.get('hreflang'))
        lang_http.append('https:' + link.next.get('href'))
    print(lang)
    print(lang_http)
    all_lang_dict = collections.OrderedDict(sorted(dict(zip(lang, lang_http)).items()))

    return all_lang_dict

def get_soup_from_url(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    return BeautifulSoup(plain_text, "html.parser")

# url="www.pudim.com.br"
# soup=get_soup_from_url(url)
# languages_dict = get_languages_links(soup)
# wikidata_id = get_wikidata_item_id(soup)
# write_csv(languages_dict, wikidata_id, 80)
# soups = get_soups_POOL_from(languages_dict)
# write_csv_from_soups(soups)
get_dict_lang_from_wikidata(1)
