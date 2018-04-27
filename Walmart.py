# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 16:54:15 2018

@author: Jennifer
"""
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# Begin Function Definitions # 

# regular Driver
'''def getDriver(url):
    driver = webdriver.Chrome('C:\\Users\\Jennifer\\Desktop\\PythonProject\\chromedriver.exe')
    driver.get(url)
    return (driver)'''

# headless Driver
def getDriverOld(url):
    
    webDriverLocation = r'C:\\Users\\Jennifer\\Desktop\\PythonProject\\chromedriver.exe'
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=webDriverLocation, chrome_options=options)
    driver.get(url)
    return (driver)

def getDriver():
    
    webDriverLocation = r'C:\\Users\\Jennifer\\Desktop\\PythonProject\\chromedriver.exe'
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=webDriverLocation, chrome_options=options)
#    driver.get(url)
    return (driver)


# inputs: driver
# return: street_address, city, state, zip
def getLocation(driver):
    
    try:
        current_url=driver.current_url
        page = requests.get(current_url)
        data = page.text
        soups = BeautifulSoup(data, 'lxml')
        street = soups.findAll("span",{"class","store-address-line-1"})
        street_address = street[0].string
        citystatezip=soups.findAll("span",{"class","store-address-line-2"})
        city=citystatezip[0].span.text
        state=citystatezip[1].text
        zipcode=citystatezip[2].text
    except IndexError:
        return( 'location unavailable' )
    
    return(street_address, city, state, zipcode)
    
# inputs: driver, item we are searching for
# exception: if the price is not on the initial search page it will throw NoSuchElementException which we handle by clicking on the item. 
# return 0 if item not found or price of the item
def getPrice1(driver, item):
    
    try:
        xpath='//div[@title="'+item+'"]'
        elem = driver.find_element_by_xpath(xpath).text
        time.sleep(1)
        
        if elem == item:
            xpath3=xpath+"/preceding::span[@class='Price-group'][2]"
            time.sleep(1)
            pricer=driver.find_element_by_xpath(xpath3).text
    except NoSuchElementException:
        
        click = clickItem( driver, item )
        if click == 'item not found':
            return( '0' )
        price = getPrice2( driver )    
        return( price )
    return( pricer )

# inputs: driver, item we are searching
# return: if NoSuchElementException will return 'item no found' - to be handled in calling function.  Otherwise returns driver
    
def clickItem(driver, item):
    
    try:
        xpath='//div[@title="'+item+'"]'
        elem = driver.find_element_by_xpath(xpath)
        elem.click()
       
    except NoSuchElementException:
        return ('item not found')
    
    return (driver)

# input: driver
# will get called if the item's price is not listed on the initial search page
# return: '0' if price is not found or price of the item
def getPrice2(driver):
    
   try:
        page = requests.get(driver.current_url)
        time.sleep(1)
        data = page.text
        soups = BeautifulSoup(data, 'lxml')
        time.sleep(1)
        thePrice = soups.find('span' ,itemprop = 'price').get('content')
    except NoSuchElementException:
        return( '0' )
       
    return( total_price )

def isSamsClub( driver ):
    
    try:
        page = requests.get( driver.current_url )
        data = page.text
        soups = BeautifulSoup(data, 'lxml')
        storeName = soups.find("span",{"class","store-name-name"}) 
        if "Sam's Club" in storeName.text: 
            return( True )
        else:
            return( False )
        
        
    except NoSuchElementException:
        return(False)
    
# End of Function Definitions #
    


baseUrl = r'https://www.walmart.com/store/'
searchQuery = '/search?query=' 
stores = 'C:/Users/Jennifer/Desktop/PythonProject/Jennifer.txt'
items = 'C:/Users/Jennifer/Desktop/PythonProject/item.txt'
walmartData = 'C:/Users/Jennifer/Desktop/PythonProject/walmartData.txt'

# read the stores into a list
with open(stores) as stores:
    searchStores = stores.read().splitlines()    

# read the items into a list
with open(items) as items:
    searchItems = items.read().splitlines()    

with open( walmartData, 'a' ) as f:
    myDriver = getDriver()
    for store in searchStores:
        print( store )
        # so the store data only gets populated once
        storeFlag = True
        for item in searchItems:
            key = store + "-" + item
            url = baseUrl + store + searchQuery + urllib.parse.quote_plus(item)
            myDriver.get(url)
            sams = isSamsClub( myDriver )
            if sams == True:
                print( store + " Sam's Club")
                break
            if storeFlag == True:
                address = getLocation(myDriver)
                if( address == 'location unavailable' ):
                    continue
                else:
                    storeData = [store, address[0], address[1], address[2], address[3]]
                    storeFlag = False
            price = getPrice1( myDriver, item )
 #           print(key + '~' + '~'.join( storeData ) + '~' + item + '~' + price)
            f.write(key + '~'+ '~'.join( storeData) + '~' + item + '~' + price + '\n')
    myDriver.close







