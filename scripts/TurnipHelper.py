import matplotlib.pyplot as pyplot
import cv2 as cv
import pandas as pd
import urllib.request
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from lxml import html

turnip_calculator_url = 'https://ac-turnip.com/#'
turnip_prophet_url = 'https://turnipprophet.io?prices='
def get_turnip_profit_link():
    return 'https://turnipprophet.io/'

def generate_turnip_prophet_link(arg, is_buying_price):
    prophetlink = _replace_zeros_with_delimiter(arg, '.', is_buying_price=is_buying_price)
    prophet_link = turnip_prophet_url+prophetlink+'.....'
    # generate_table(prophet_link)
    
    return prophet_link

def generate_turnip_ac_turnip_link(arg, is_buying_price):
    acturnip_link = _replace_zeros_with_delimiter(arg, is_buying_price=is_buying_price)
    ac_turnip_link = turnip_calculator_url+acturnip_link
    
    return ac_turnip_link
    

def generate_table(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)
    table = tree.xpath("//tbody[@id='output']//tr")
    print(len(table))
    
    
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
