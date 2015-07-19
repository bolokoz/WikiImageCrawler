from bs4 import BeautifulSoup
import re
import requests

__author__ = 'Yuri'


def get_data_from_url(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def get_string_description_from_soup(soup):
    raw_description = soup.p
    links_in_description = raw_description.findAll('a')
    for link in links_in_description:
        print link.get('title')


def get_positive(soup):
    for text in soup.findAll('p'):
        print text(string=re.compile('able'))


def change_a_tag(html):
    a_tag = html.a
    print a_tag
    print ("decompose", html.a.decompose())
    print ("extract", html.string)
    # print ("unwrap",html.a.unwrap())
    # html.a.name = "aasa"
    # html.a['href'] = ""
    print(html)


url = "https://en.wikipedia.org/wiki/Bucket-wheel_excavator"
soup = get_data_from_url(url)
html_description = soup.p
print html_description
get_positive(soup)
