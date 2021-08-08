import requests
from bs4 import BeautifulSoup
import xlwt
import re
from pprint import pprint
import csv


def one_page_crawl(url, lis):
    
    info_list = []
    info_list.append('')

    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)

    r_t = r.text

    #getting name

    soup = BeautifulSoup(r_t,'lxml')

    #print(soup.title.string)
    info_list.append('Givenchy')
    info_list.append(soup.title.string.split(' | ')[0])

    #getting price

    prce = soup.find_all('span',{'itemprop':'price'})
    att = prce[0].attrs['content']

    att = str(att)
    #print(att)
    info_list.append(att)

    #getting gender
    info_list.append('Women')


    #getting discreptions

    dis = soup.find_all("meta", {"property":"og:description"})
    #print(dis)
    att = dis[0].attrs['content']
    att = str(att)
    info_list.append(att)

    #get path
    info_list.append(url)

    #getting images

    img = soup.find_all("li", {"class":"ImageCarousel83__slide"})

    #print('LEN', len(img))

    img_complex = ''
    for im in img:
        st = str(im)
        img_link = re.findall('srcset="(.*?)2000w',st,re.S)
        #print(img_link)
        if img_link != []:
            img_string = str(img_link[0])
            img_string = 'https://cache' + img_string
            if img_string not in img_complex:
                img_complex += img_string + ';'
    
    info_list.append(img_complex)

    #print(info_list)

    
    lis.append(info_list)
        
    #$print(img_complex)
    
    #print(info_list)
item_list = []
titl = ['id','brand','name','price','gender','description','path','image']
item_list.append(titl)

url_source = 'https://www.net-a-porter.com/en-us/shop/search/givenchy?categoryId=1283'
url = ''
for i in range(1,2):
    print('i=' + str(i))
    if i == 1:
        url = url_source
    else:
        url = url_source + '?pageNumber=' + str(i)
    
    print(url)


    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(url, headers=headers)

    r_t = r.text

    soup = BeautifulSoup(r_t,'lxml')
    grid = soup.find_all('div',{'class':'ProductGrid51 ProductListWithLoadMore51__listingGrid'})
    links = grid[0].find_all('a')

    print(len(links))
    page_links = []
    for link in links:
    
        l = str(link.attrs['href'])
        page_links.append('https://www.net-a-porter.com'+l)
    
    #print(page_links)


    for url in page_links:
        one_page_crawl(url,item_list)

    print(len(item_list))
#pprint(item_list)



with open('netaporter_Givenchy_shoes_scrape.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(item_list)