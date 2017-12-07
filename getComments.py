from bs4 import BeautifulSoup
import time
import re
from urllib.request import urlretrieve
import requests

def get_restaurants(url_cuisine):
    restaurant = []
    count = []
    for i in range(0,50,10):
        try:
            pageLink = url_cuisine + str(i)
            print(pageLink)
            # use the browser to access the url
            response = requests.get(pageLink, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: print("inside response")
            html = response.content  # get the html
            if not html: continue  # couldnt get the page, ignore
            if html: print("inside html")
            soup = BeautifulSoup(html, 'html.parser')  # parse the html
            if soup: print("got soup")
            res =soup.findAll('a', {'href': re.compile('/biz/')})
            cnt = soup.findAll('span',{'class':'review-count rating-qualifier'})
            for c in range(2,len(cnt)-1):
                count.append(int(cnt[c].text.strip().split()[0]))
            for r in range(0,len(res)-1,3):
                    restaurant.append(res[r]['href'])  # .encode('ascii','ignore')
        except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
            print('failed attempt', i)
            time.sleep(2)  # wait 2 secs
    return restaurant , count
def run(url, formatedCC, restaurant_name):
    pagenumber = 0
    print (url)
    for p in range(0,formatedCC+1,20):
        pagenumber = pagenumber + 1
        html=None
        pageLink=url+'?start='+str(p) # make the page url
        for i in range(5): # try 5 times
            try:
                reviewName = restaurant_name+'_review_pg'+ str(pagenumber) + '.html'
                urlretrieve(pageLink,reviewName)
                print(pageLink)
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
        if not html:continue # couldnt get the page, ignore


if __name__ == '__main__':
    cuisine = input("Enter Cuisine: ")
    start = 'start=0'
    url_cuisine = 'https://www.yelp.com/search?find_desc='+cuisine+'&find_loc=New+York,+NY&start='

    lst_restaurants, lst_count = get_restaurants(url_cuisine)
    for i in range(len(lst_restaurants)):
        lst_restaurants[i] = lst_restaurants[i].strip().split("?")[0]
    #print(len(lst_count))
    restaurant_names = []
    for i in range(len(lst_restaurants)):
        restaurant_names.append(lst_restaurants[i].strip().split("/")[2])
    formatedCC = []
    for i in lst_count:
        formatedCC.append(i - (i%20))
    for i in range(len(lst_restaurants)):
        url='https://www.yelp.com'+lst_restaurants[i]
        run(url,formatedCC[i],restaurant_names[i])
