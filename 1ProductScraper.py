#%% import dependencies
import requests
from bs4 import BeautifulSoup

# keeping for reach products with links
productLinks = []

#%% go amazon foods, fetch the page
def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url':url ,'wait':2})    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup

#%% find products
def get_products(soup):
    
    # get product info from a tag
    products = soup.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    try:
        # define a dictionary that contains product name and link
        for product in products:
            
            product = {
                'name' : product.text,
                'link' : 'www.amazon.com'+product['href']
            }
        
            print(product)
            productLinks.append(product)
            
    except:
        pass

    
#%% run for different pages. 400 pages exist
for p in range(1,250):
    
    # link for amazon/Grocery & Gourmet Food/Snacks & Sweets
    soup = get_soup(f'https://www.amazon.com/s?rh=n%3A23759921011&fs=true&page={p}&ref=lp_23759921011_sar')
    get_products(soup)
    
    # check for last page
    if not soup.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
        pass
    else:
        pass
    
#%% export to csv file
# we have products. let's export this data to file
import csv

csvColumns = ['name','link']
csvFile = "productLinks.csv"

try:
    with open(csvFile, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csvColumns)
        writer.writeheader()
        for link in productLinks:
            writer.writerow(link)
except IOError:
    print("I/O error")
    
    
    
    
    