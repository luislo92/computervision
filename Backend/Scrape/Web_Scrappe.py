from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import ssl
import pandas as pd
import re
from numpy import mean

url = "https://fastfoodnutrition.org/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
gcontext = ssl.SSLContext()
webpage = urlopen(req,context=gcontext).read()
page_soup = soup(webpage, "html.parser")

restaurants = []
for s in page_soup.find_all("ul",class_="list divider restaurant_list"):
    for tit in s.find_all('a',class_='c_t'):
        restaurants.append(tit.get('href'))

def getter(url):
    url = url
    restaurant = url.split("https://fastfoodnutrition.org/")[1]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    gcontext = ssl.SSLContext()
    webpage = urlopen(req,context=gcontext).read()
    page_soup = soup(webpage, "html.parser")
    noodle = page_soup.find_all("a",class_="listlink item_link active_item_link")
    clean_noodle = [noodle[i].text.split(" Nutrition Facts") for i in range(len(noodle))]
    #print(clean_noodle)
    name = []
    min_value = []
    max_value = []
    rest = []
    for nood in clean_noodle:
        name.append(nood[0])
        rest.append(restaurant)
        v = nood[1].split(' calories')[0].split('-')
        if len(re.findall(r'[0-9]+',v[0])) >= 1:
            if len(v)>1:
                min_value.append(int(v[0]))
                max_value.append(int(v[1]))
            else:
                min_value.append(int(v[0]))
                max_value.append(int(v[0]))
        else:
            min_value.append(0)
            max_value.append(0)
    return pd.DataFrame({'name':name,'restaurant': rest,
                         'min_value':min_value,
                         'max_value':max_value,
                         'mean_value':[mean([min_value[i],max_value[i]]) for i in range(len(min_value))]})
df = pd.DataFrame()
for rest in restaurants:
    url = "https://fastfoodnutrition.org"+rest   #"baskin-robbins"
    df = pd.concat([df,getter(url)])

df.reset_index(drop=True).to_csv('nutrition_scrappe.csv')
