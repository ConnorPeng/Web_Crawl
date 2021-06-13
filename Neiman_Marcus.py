import requests
from bs4 import BeautifulSoup
import xlwt
import re
from pprint import pprint
import csv
from selenium import webdriver


def one_page_crawl(url, lis, gender):
    info_list = []
    info_list.append('')

    PATH = "/Users/jasonqi/Desktop/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    url = 'https://www.neimanmarcus.com/'+url

    driver.get(url)

    #print(driver.title)
    r_t = driver.page_source
    #print(r_t)


    soup = BeautifulSoup(r_t,'lxml')

    #getting gender
    
    info_list.append(gender)
    
    #getting brands
    
    brds = soup.find_all('span',{'class':'product-designer'})
    
    brd = brds[0].string
    
    print("brd:" + brd)
    
    info_list.append(brd)
    
    #print(soup.title.string)
    nmes = soup.find_all('span',{'class':'prodDisplayName'})
    #info_list.append(soup.title.string.split(' | ')[0])
    #getting name
    nme = nmes[0].string
    #print(att)

    #print(att)
    info_list.append(nme)
    print(nme)


    #getting color
    '''
    colors = soup.find_all('div',{'class':'tablet-grid-100 grid-parent colorButtonOptions'})
    print(str(colors[0]))
    '''
    color = re.findall('Select Color: <span>(.*?)</span>',str(r_t))
    print(color[0])
    info_list.append(gender)
    
    #getting discreptions
    
    '''
    dis = soup.find_all("div", {"class":"product-description__content__cutline-standard"})
    dis_str = str(dis[0])
    #print(dis_str)
    dis_content = re.findall('<li>(...)</li>',dis_str,re.S)
    #print(dis_content)
    att = ''
    for cnt in dis_content:
        att +=  '*' + cnt 
    print(att)
    info_list.append(att)
    '''
    dis = soup.find_all("div", {"class":"productCutline"})
    #print(dis)
    bullets = dis[0].find_all("li",)
    description = ""
    for b in bullets:
        description += "*" + b.string
    print(description)

    
    #getting price
    
    '''
    prce = soup.find_all('span',{'class':'retailPrice'})
    if prce == []:
        prce = soup.find_all('div',{'class':'product-heading__price'})
        #print(prce)
        prce = prce[0].find_all('span',{'class':'price'})
    att = prce[0].string[1:]

    att = str(att)
    #print(att)
    info_list.append(att)
    '''
    prces = soup.find_all('p',{'class':'lbl_ItemPriceSingleItem product-price'})
    print("price:" + prces[0].string)
    print(type(str(prces[0].string)))
    info_list.append(prces[0].string[6:])

    #get shipping & return
    ships = soup.find_all('span',{'class':'freeBlitzContainer'})
    ship = ships[0].string
    info_list.append(ship)

    #get path
    info_list.append(url)

    #get img
    slick = soup.find_all("div", {"class":"images"})
    print("images length:")
    print(len(slick))
    slick_str = str(slick[0])
    #print(slick[0])
    #img_content = slick.findall('src=\"(.*?)"alt',slick_str,re.S)
    img_content = slick[0].find_all('img')
    #print(img_content)
    img_complex = ''
    count = 0
    for lnk in img_content:
        img_str = str(lnk.attrs['src'])
        if img_str not in img_complex and img_str[0:6] == "https:":
            img_complex += img_str + ';'
            count += 1
    print("img length:" + str(count))
    #print(info_list)
    info_list.append(img_complex)
    
    lis.append(info_list)



item_list = []
titl = ['id', 'brand', 'name', 'price', 'gender', 'description', 'path', 'image']
item_list.append(titl)

url = 'https://www.neimanmarcus.com/s/?filterOptions=%7B%22Category%22%3A%5B%22Shoes%22%5D%7D&fl=&from=brSearch&l=Saint%20laurent&page=1&q=Saint%20laurent&request_type=search&responsive=true&search_type=keyword'

PATH = "/Users/jasonqi/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get(url)

#print(driver.title)
src = driver.page_source

soup = BeautifulSoup(src, 'lxml')

# print(soup.title.string)
# get different products

grids = soup.find_all("div",{'class':'product-thumbnail grid-33 tablet-grid-33 mobile-grid-50 grid-1600 enhancement'})
#links = grid[0].find_all('a')

#print(len(links))
page_links = []
for grid in grids:
    link = grid.find_all('a')
    l = str(link[0].attrs['href'])
    page_links.append(l)
    
print(page_links)


for i in page_links:
    one_page_crawl(i,item_list,'Men')
    #print(len(item_list))


print(len(item_list))
#pprint(item_list)


url = 'https://www.neimanmarcus.com/s/?filterOptions=%7B%22Category%22%3A%5B%22Shoes%22%5D%7D&fl=&from=brSearch&l=Saint%20laurent&page=2&q=Saint%20laurent&request_type=search&responsive=true&search_type=keyword'

PATH = "/Users/jasonqi/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get(url)

#print(driver.title)
src = driver.page_source

soup = BeautifulSoup(src, 'lxml')

# print(soup.title.string)
# get different products

grids = soup.find_all("div",{'class':'product-thumbnail grid-33 tablet-grid-33 mobile-grid-50 grid-1600 enhancement'})
#links = grid[0].find_all('a')

#print(len(links))
page_links = []
for grid in grids:
    link = grid.find_all('a')
    l = str(link[0].attrs['href'])
    page_links.append(l)
    
#print(page_links)


for i in page_links:
    one_page_crawl(i,item_list,'Women')
    #print(len(item_list))


print(len(item_list))
#pprint(item_list)




with open('NM_Givenchy_sneakers_scrape.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(item_list)