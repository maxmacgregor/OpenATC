#!/usr/bin/env python3
import requests
import re
import timeit
import json
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from getconf import *

size = '11'
hasLink = True
link = 'https://www.size.co.uk/product/grey-nike-flyknit-free-mercurial/030099/'
accEmail = 'maxmacgregor1996@gmail.com'
accPass = 'bruern770'
deliveryMethod = 'S' #can be 'S', 'ND', or 'NDE'; standard, next day, next day evening

#Functions
def checkout():
    payload = {
        'username' : accEmail,
        'password' : accPass
    }
    response = session.post('https://www.size.co.uk/myaccount/login/', data=json.dumps(payload))
    soup = bs(response.text, 'html.parser')
    print(soup)

    response = session.get('https://www.size.co.uk/checkout/delivery/')
    soup = bs(response.text, 'html.parser')
    if deliveryMethod.upper() == 'S':
        payload = {
            'editMethodID' : '5F6610A86122457F870E1DAD6DBCA4B2'
        }
    elif deliveryMethod.upper() == 'ND':
        payload = {
            'editMethodID' : '76839FD1D75E4A1F8A35AFF521FFCB54'
        }
    elif deliveryMethod.upper() == 'NDE':
        payload = {
            'editMethodID' : '7F8FFF94016F4FDF82AC6C88DBA03A6A'
        }
    response = session.post('https://www.size.co.uk/checkout/updateDeliveryMethod/ajax/', data=json.dumps(payload))
    soup = bs(response.text, 'html.parser')
    print(soup)

    response = session.post('https://www.size.co.uk/checkout/billing/')
    soup = bs(response.text, 'html.parser')
    payload = {
        'card_number' : card_number,
        'exp_month' : card_exp_month,
        'exp_year' : '20' + card_exp_year,
        'cv2_number' : card_cvv,
        'issue_number' : '',
        'HPS_SessionID' : soup.find('input', {'name' : 'HPS_SessionID'})['value'],
        'action' : 'confirm'
    }
    response = session.post('https://hps.datacash.com/hps/?', data=json.dumps(payload))
    soup = bs(response.text, 'html.parser')
    print(soup)

#Main
start = timeit.default_timer()

session = requests.session()

if hasLink:
    response = session.get(link)
    soup = bs(response.text, 'html.parser')
    
    sizeCodes = soup.find_all('button', 'bb level2 ')
    sizeCode = ''
    for code in sizeCodes:
        if size in code.getText():
            sizeCode = code["data-sku"]
            continue

    payload = {
        'quantityToAdd' : '1',
        'customisations' : [],
        'cartPosition' : None
    }

    response = session.post('https://www.size.co.uk/cart/' + sizeCode + '/', data=json.dumps(payload))
    checkout()

stop = timeit.default_timer()
print(stop - start) # Get the runtime
