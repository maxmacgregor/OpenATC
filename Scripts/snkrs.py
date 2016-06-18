# from __future__ import print_function

#!/usr/bin/python

#####
# THIS SNKRS SCRIPT IS PROBABLY OUT OF DATE AT THIS MOMENT. I HAVENT USED IT TO PURCHASE ANYTHING SINCE JAN 2016 OR EARLIER.
# 
#####

import os
import sys
import requests
import uuid
import re
import ast
import json
import xmltodict
import time

# Find the productId of the shoe you are looking for. This can be found either through nike tweets or from nike website.
# Jordan 7 Hare 10265132
productId="10265132"

#URL for request
url="https://unite.nikeapp.com/login"
#Replace with your nikestore.com login email
ndcEmail=""
#Replace with your nikestore.com login password
ndcPassword=""

###### Header variables
# Headers for sku POST request
sku_headers = {
    'Host': 'secure-store.nike.com',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Referer':'https://s3.nikecdn.com/unite/mobile.html?iOSSDKVersion=1.0.0&uxId=com.nike.valiant.ios&view=login&locale=en_US&backendEnvironment=prd',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate'
}

# Headers for Access Token POST request
access_token_headers = {
    'Host': 'unite.nikeapp.com',
    'Content-Type':'application/x-www-form-urlencoded',
    'Origin':'https://s3.nikecdn.com',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12B466',
    'Referer':'https://s3.nikecdn.com/unite/mobile.html?iOSSDKVersion=1.0.0&uxId=com.nike.valiant.ios&view=login&locale=en_US&backendEnvironment=prd',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate'
}

# Access Token POST request payload
access_token_data = {
    '_registrationSiteId': '1023',
    'emailAddress': ndcEmail,
    'password': ndcPassword,
    '_rememberMe': 'false',
    '_locale': 'en_US',
    'client_id': '0239a00434d37e14e8644b9821d1322c',
    'ux_id': 'com.nike.valiant.ios',
    'transactionId': str(uuid.uuid1()),
    '_backendEnvironment': 'prd'
}

# SNKRS Headers
snkrs_headers = {
    'Content-type': 'application/json',
}

def get_size():
    size = None
    print("A number was not supplied in the arguments")
    while size is None:
        input = raw_input("Enter a size: ")
        try:
            size = str(input)
            break
        except ValueError:
            print("Not a number.")
    return size

def get_skuId(size):
    #productId URL
    sku_url="https://secure-store.nike.com/us/services/catalogService?action=loadSkus&productId="+productId
    #A request session
    sku_session=requests.Session()

    #Clear the session
    sku_session.cookies.clear()
    #POST request to retrieve skuId
    response=sku_session.post(sku_url,headers=sku_headers)
    print("This is the response to the sku POST: ", response)

    #Store the response in a string
    sku_string=response.text.encode("utf-8")
    print('this is the sku string: ', sku_string)

    #convert our xml string to a dictionary
    try:
        dictionary=xmltodict.parse(sku_string)
        print('dictionary: ', dictionary)
        print('THIS IS HARDGOODFULFILLER: ',  dictionary['response']['p']['is'])
    except:
        print('unable to convert response string to a dictionary')
        print('string         : ',  sku_string)
        sys.exit(1)

    my_regex=r"\<id\>\d*\<\/id\>\<s\>" + str(size) + r"\<\/s\>"
    print('MY REGEX PATTERN: ', my_regex)
    try:
        if "false" in dictionary['response']['p']['is']:
            print('NO SIZES AVAILABLE')
        else:
            try:
                dictionary['response']['p']['cs']['s'][size]
            except:
                print('THIS SIZE IS NOT AVAILABLE: ', size)
            pid_m=re.search(my_regex,sku_string)
            print('PID AND SKU SEARCH RESULTS: ', pid_m.group())
            x=re.search('\d.\d*', pid_m.group())
            skuId=x.group()
            print('THE SIZE SKUID IS: ', skuId)
            return skuId
    except:
        print('SOMETHING WENT WRONG')

def generate_access_token():
    #A request session
    session=requests.Session()
    #Clear the session
    session.cookies.clear()
    #POST request
    response=session.post(url,data=access_token_data,headers=access_token_headers)
    # print('Unite.nikeapp.com response:', response)
    #Store the response in a string
    string=response.text.encode("utf-8")
    print('RESPONSE CONTENT TYPE', response.headers['content-type'])
    print('RESPONSE STRING: ', string)
    #Parse the response string for the line that we need
    m=re.search('nike.unite.on.login.success.fire\((.+)\);',string)
    #String replacement withing a string to dictionary evaluation
    dictionary=ast.literal_eval(m.string[m.start():m.end()].replace("nike.unite.on.login.success.fire(","").replace(");",""))
    #Print out our dictionary
    # print 'expires_in : ' + dictionary['expires_in']
    # print 'refresh_token : ' + dictionary['refresh_token']
    # print 'uuid : ' + dictionary['uuid']
    # print 'access_token : ' + dictionary['access_token']
    access_token=dictionary['access_token']
    return access_token

def snkrs_buy(skuId):
    # SNKRS Post Request payload
    snkrs_data = {
        "action": "purchaseItem",
        "catalog": "1",
        "country": "US",
        "login": ndcEmail,
        "password": ndcPassword,
        "productId": productId,
        "qty": "1",
        "rt": "json",
        "siteId": "1000",
        "skuId": skuId
        # "shopper_token": "LwZBVAGxTSc69JBTO0EufiVU7SkFuJgb"
    }

    shopper_token="LwZBVAGxTSc69JBTO0EufiVU7SkFuJgb"
    session=requests.Session()
    url="https://buy.nike.com/commerce/us/buy?access_token="+access_token
    print('snkrs request url   : ', url)
    response=session.post(url,data=json.dumps(snkrs_data),headers=snkrs_headers)
    print('snkrs_buy response: ', response)
    print('response text: ', response.headers['content-type'])
    string=response.text.encode("utf-8")
    print('string', string)
    # obj = json.loads(string.encode('utf-8'))
    # numpil = obj['pil'].encode('utf-8')


    # print('JSON :', obj)
    # print('NUMBER PIL: ', numpil)
    #convert our xml string to a dictionary
    try:
        dictionary=xmltodict.parse(string)
        #list = json.loads(string.encode('utf-8'))
        print('foo00000')
        print('DICTIONARY : ', dictionary)
    except:
        print('foo11111')
        print('unable to convert response string to a dictionary')
        print('url            : ', response.url)
        print('string         : ', string)
        # sys.exit(1)
        ewt="25"
        if "ewt":
            sleep_time = dictionary['rootNode']['ewt']
            time.sleep(sleep_time)
            #Replace with your pil from dstryr-buy.py
            pil=dictionary['rootNode']['pil']
            #Replace with your psh from dstryr-buy.py
            psh=dictionary['rootNode']['psh']
            data2={"action": "purchaseItem",
                  "catalog": "1",
                  "country": "US",
                  "login": ndcEmail,
                  "password": ndcPassword,
                  "pil": pil,
                  "productId": productId,
                  "psh": psh,
                  "qty": "1",
                  "rt": "json",
                  "siteId": "1000",
                  "skuId": skuId
                  }
            ewt_response=session.post(url,data=json.dumps(data2),headers=headers2)
            string=ewt_response.text.encode("utf-8")
            try:
              #Lets see if we can convert response string from XML to dictionary
              dictionary2=xmltodict.parse(string)
            except:
                print('foo2')
                print('unable to convert xml to dictionary2')


            try:
              #If we cant print a purchase url then we likely are still in line
                print('purchase url  : ', dictionary['rootNode']['redirectURL'])
            except:
                print('No redirect URL in the response. So you might be in line still:')
                print('Response : ', string)
                print('URL      : ', response.url)
                print('status   : ', dictionary2['rootNode']['status'])
                print('pil      : ', dictionary2['rootNode']['pil'])
                print('psh      : ', dictionary2['rootNode']['psh'])
                print('ewt      : ', dictionary2['rootNode']['ewt'])
                try:
                    time.sleep(int(dictionary2['rootNode']['ewt']))
                    print('foo')
                except:
                    sys.stdout.flush()
                finally:
                    sys.stdout.flush()

    #print out the redirect URL which is the one-time click life URL to purchase the shoe
    #if your NDC account does not have a shipping information or billing information stored it will
    #take you to the shipping info page then the billing info page.
    #if shipping information is stored for the NDC account then it will take you to the billing info page.
    #if the billing information is stored fort he NDC account then it will likely auto-checkout
    try:
        print('Looks like they added directly to your cart: \n')
        print('purchase url  : ', dictionary['rootNode']['redirectURL'])
    except:
        print('No purchase url in response \n')
        try:
            if "wait" in dictionary['rootNode']['status']:
                print('You got status wait. Looks like you are in line: \n')
                print('status : ', dictionary['rootNode']['status'])
                print('pil    : ', dictionary['rootNode']['pil'])
                print('ewt    : ', dictionary['rootNode']['ewt'])
                print('psh    : ', dictionary['rootNode']['psh'])
            else:
                print
                print('You did not get status wait. Looks like you are no longer in line: ')
                print('status : ', dictionary['rootNode']['status'])
        except:
            print('exiting here')
            #if you reached this point - then that means you avoided the sys.exit
            #but have something in your response that does not contain a redirectURL
            #nor a status. so lets just flush the buffer and call it a day.
            sys.stdout.flush()



if __name__ == '__main__':
    size = get_size()
    while True:
        sku = get_skuId(size)
        #sku = 11566088
        if sku:
            print('SUCCESS. THE SIZE SKU WAS FOUND')
            access_token = generate_access_token()
            print('THE ACCESS TOKEN IS: ', access_token)
            snkrs_buy(sku)
            break
        else:
            # If the size is not found, lets loop back and keep trying to find the size. Either run this a few minutes before shoes become available OR
            # when other user carts are being emptied out and sizes start re-appearing
            time.sleep(5)
            print('LOOPING TO LOOK FOR SIZE', size)
            print('##########################################')
            print('##########################################')
            print
            time.sleep(2)