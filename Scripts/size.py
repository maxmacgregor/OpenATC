#!/usr/bin/env python3
import requests
import re
import timeit
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
from getconf import *

size = '11'
hasLink = True
link = 'https://www.size.co.uk/product/grey-nike-flyknit-free-mercurial/030099/'
accEmail = 'testemail@gmail.com'
accPass = 'testpass'

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
        'customisations' : '[]',
        'cartPosition' : 'null'
    }

    response = session.post('https://www.size.co.uk/cart/' + sizeCode + '/', data=payload)
    test = bs(response.text, 'html.parser')
    print(test)
    data=json.dumps(payload)
    print(data)
##    checkout()

stop = timeit.default_timer()
print(stop - start) # Get the runtime


##def checkout():
##response = session.get('https://www.size.co.uk/checkout/login/')
##    soup = bs(response.text, 'html.parser')
##
##    form = soup.find('form', {'action' : '/checkout'})
##    
##    payload = {
##       form.find('input', {'name' : re.compile('(?<=updates\[)(.*)(?=])')})['name'] : form.find('input', {'name' : re.compile('(?<=updates\[)(.*)(?=])')})['value'],
##       'checkout' : 'Checkout',
##       'note' : form.find('input', {'name' : 'note'})['value']
##    }
##    
##    response = session.post('http://shop-usa.palaceskateboards.com/cart', data=payload)
##    soup = bs(response.text, 'html.parser')



    
