import matplotlib.pyplot as pyplot
import cv2 as cv
import pandas as pd
import urllib.request
import requests
import re

from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from lxml import html

turnip_calculator_url = 'https://ac-turnip.com/share?f='
turnip_prophet_url = 'https://turnipprophet.io?prices='

def generate_turnip_prophet_link(arg, is_buying_price):
    prophetlink = _replace_zeros_with_delimiter(arg, '.', is_buying_price=is_buying_price)
    prophet_link = turnip_prophet_url+prophetlink
    
    return prophet_link

def generate_turnip_ac_turnip_link(arg, is_buying_price):
    acturnip_link = _replace_zeros_with_delimiter(arg, delimiter='-', is_buying_price=is_buying_price)
    img_link = 'https://ac-turnip.com/p-'+acturnip_link+'.png'
    ac_turnip_link = turnip_calculator_url+acturnip_link
    return ac_turnip_link, img_link
    

def generate_img(link):
    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    soup = bs(html, features="html.parser")
    img_tags = soup.find_all('img')

    # urls = [img['content'] for img in img_tags]
    # results = soup.findAll('img')
    print(img_tags)
        
    
def _replace_zeros_with_delimiter(arg, delimiter=',', is_buying_price=False):
    if is_buying_price:
        ret = '{}'.format(arg[0])
        arg = arg[1:]
    else:
        ret = ''
        
    for num in arg:
        if num == 0:
            ret += delimiter
        else:
            ret += '{}{}'.format(delimiter, str(num))
            
    return ret

# generate_img('https://ac-turnip.com/share?f=99--84')