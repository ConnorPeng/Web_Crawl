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

    r_t = driver.page_source

    soup = BeautifulSoup(r_t,'lxml')
    
    #getting brands
    
    brds = soup.find_all('span',{'class':'product-designer'})
    brd = brds[0].string
    print("brd:" + brd)
    info_list.append(brd)
    nmes = soup.find_all('span',{'class':'prodDisplayName'})
    
    #getting name
    
    nme = nmes[0].string
    info_list.append(nme)
    print(nme)


    #getting color
    
    color = re.findall('Select Color: <span>(.*?)</span>',str(r_t))
    print(color[0])
    info_list.append(gender)
    
    #getting discreptions
    
    dis = soup.find_all("div", {"class":"productCutline"})
    #print(dis)
    bullets = dis[0].find_all("li",)
    description = ""
    for b in bullets:
        description += "*" + b.string
    print(description)

    
    #getting price
    
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
    img_content = slick[0].find_all('img')
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

url = 'https://www.bloomingdales.com/shop/saint-laurent?id=1100159&edge=hybrid&cm_kws=saint+laurent'

PATH = "/Users/jasonqi/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get(url)

#print(driver.title)
src = driver.page_source

soup = BeautifulSoup(src, 'lxml')

# print(soup.title.string)
# get different products

grids = soup.find_all("li",{'class':'small-6 medium-4 large-4 cell'})
#links = grid[0].find_all('a')

#print(len(links))
page_links = []
for grid in grids:
    link = grid.find_all('a')
    #
    l = "https://www.bloomingdales.com" + str(link[0].attrs['href'])
    page_links.append(l)
    
print(page_links)


for i in page_links:
    one_page_crawl(i,item_list,'Men')
    #print(len(item_list))


print(len(item_list))
#pprint(item_list)




with open('NM_Givenchy_sneakers_scrape.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(item_list)