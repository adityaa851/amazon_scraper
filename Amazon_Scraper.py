from requests_html import HTMLSession
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

s = HTMLSession()
# First we need to write the functions to get 
# 1. Title
# 2. Price
# 3. Ratings
# 4. Availability
# 5. Number of ratings

def getTitle(soup): 
    try:
        title = soup.find('span', attrs = {'id' : "productTitle"}).text.strip()

    except:
        title = ''
        
    return title

def getPrice(soup):
    try:
        price = soup.find('span', attrs = {'class': "a-offscreen"}).text.strip()
    except:
        price = 'NULL'
        
    return price

def getRatings(soup):
    try:
        ratings = soup.find('span', attrs = {'class': "a-icon-alt"}).text.strip()
    except:
        ratings = 'NULL'
    
    return ratings

def NumRatings(soup):
    try:
        numRatings = soup.find('span', attrs = {'id' : "acrCustomerReviewText"}).text.strip()
    except:
        numRatings = 'NULL'
    
    return numRatings

def Availibility(soup):
    try:
        availibility = soup.find('span', attrs = {'class': "a-size-medium a-color-success"}).text.strip()
    except:
        availibility = 'NULL'
    
    return availibility 

def nextPage(soup) :
    page = soup.find('span', attrs = {'class' : "s-pagination-strip"})
    if not page.find('span', attrs = {'class' : "s-pagination-item s-pagination-next s-pagination-disabled "}):
        url1 = "https://amazon.in" + str(page.find('a', attrs = {'class' : "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"}).get('href'))
        return url1
    else:
        return

def getData(url):
    r = s.get(url, headers = headers)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    return soup
# Now we will start web scraping 

if __name__ == '__main__' :
    
    dict1 = {"Title":[], "Price":[], "Availibility":[], "Rating":[], "Number of Ratings":[], "Amazon Link": []} 

    url = "https://www.amazon.in/s?k=ps5+games&crid=1F4U7VKBOI7UU&qid=1686845666&sprefix=ps5+game%2Caps%2C216&ref=sr_pg_1"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 9_6_5) AppleWebKit/535.3 (KHTML, like Gecko) Chrome/55.0.1500.172 Safari/533'}

    soup = getData(url)

    links = soup.find_all('a', attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_List = []
    for link in links:
        listing = "https://amazon.in" + link.get('href')
        links_List.append(listing)

    for newLink in links_List:
        newRequest = s.get(newLink, headers = headers)
        newRequest.html.render(sleep=1)
        soup2 = BeautifulSoup(newRequest.html.html, "html.parser")
            
        dict1['Title'].append(getTitle(soup2))
        dict1['Price'].append(getPrice(soup2))
        dict1['Availibility'].append(Availibility(soup2))
        dict1['Rating'].append(getRatings(soup2))
        dict1['Number of Ratings'].append(NumRatings(soup2))
        
    
    i = 0
    for i in range(10): 
        url_next = nextPage(soup)
        if not url_next:
            break
        
        soup = getData(url_next)

        links = soup.find_all('a', attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        links_List = []
        for link in links:
            listing = "https://amazon.in" + link.get('href')
            links_List.append(listing)

        for newLink in links_List:
            newRequest = s.get(newLink, headers = headers)
            newRequest.html.render(sleep=1)
            soup2 = BeautifulSoup(newRequest.html.html, "html.parser")
             
            dict1['Title'].append(getTitle(soup2))
            dict1['Price'].append(getPrice(soup2))
            dict1['Availibility'].append(Availibility(soup2))
            dict1['Rating'].append(getRatings(soup2))
            dict1['Number of Ratings'].append(NumRatings(soup2))
        

        

    amazon_df = pd.DataFrame.from_dict(dict1)
    amazon_df['Title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

    print(dict1)