import requests
from bs4 import BeautifulSoup
import numpy as np
import json


def scrape():
    '''
    This function will scrape the closing price of NVDA using BeautifulSoup

    Input: None
    Output: Closing price of NVDA as a (1,1) numpy array
    '''
    #Get Content
    url = "https://www.marketwatch.com/investing/stock/nvda"
    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimic a browser request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        price = soup.find("div", class_="region region--intraday").find("td", class_="table__cell u-semi").string
        if price: 
            price = price.replace("$", "")
            price = np.array(float(price))
            price = price.reshape(1,1) #pytorch requires time-series to be in this shape
        else:
            price = np.array([[0]]) #if I see 0 in my database I will know that there was an error
        
        return price

def lambda_handler(event, context):
    price = scrape()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
