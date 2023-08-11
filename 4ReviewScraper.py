#%% import dependencies
import requests
import pandas as pd
from bs4 import BeautifulSoup

# keeping for reviews and score
productLinks = []
productInfo = []

#%% import product links
productLinks = pd.read_csv('D:\\Study\\4.2\\BitirmeÖdevi\\code\\3productLinksPrepared.csv').iloc[:,1]

#%% go product link
def getSoup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url':url ,'wait':2, 'timeout':60})    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup


#%% get review page
def getReviewPage(soup):
    reviewPage = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
    reviewUrl = 'http://www.amazon.com'+reviewPage['href']
    
    return reviewUrl

#%% sort reviews by recent
def getRecentReviewsTag(url):
    
    return url+'&sortBy=recent&pageNumber=1'

#%% fetch score and review
def getInfo(url):
    soup = getSoup(url)
    
    # get product info from a tag
    scores = soup.find_all('i', {'data-hook': 'review-star-rating'})
    reviews = soup.find_all('span', {'data-hook': 'review-body'})
    
    # define a dictionary that contains product name and link  
    for i in range (0, len(reviews)):
        if not reviews[i] == None:
            info = {
                'review' : reviews[i].span.text,
                'score' : scores[i].span.text[:3]
            }
            productInfo.append(info)
            print(info)
        else:
            pass


#%% run all process
for i in range(0, len(productLinks)):
    print("--------"+str(i)+"----------")
    productUrl = 'http://'+str(productLinks[i])
    print(productUrl)
    print("-------------")
    
    soup = getSoup(productUrl)
    reviewsUrl = getReviewPage(soup)
    print(reviewsUrl)
    print("-----------")
    
    recentReviewsUrl = getRecentReviewsTag(reviewsUrl)
    print(recentReviewsUrl)
    print("-----------")
    
    getInfo(recentReviewsUrl)
    
    print()
    print()
    print()

#%% export to csv
p = productInfo
p = pd.DataFrame(p)
#p.to_csv(r'5reviews1.csv', index=False, header=True)

#%% add on existing csv
p.to_csv('5reviews.csv', mode='a', index=False, header=False)
