import time
import sys
import csv
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

def scrape(search):
    url = "https://www.cettire.com/pages/search?type=product&q=" + search.lower().replace(" ", "+")
    driver = webdriver.Chrome()
    driver.get(url)
    links = []
    while True:
        try:
            products = driver.find_elements_by_class_name("product-card")
            for product in products:
                link = product.get_attribute("href")
                if link and link.startswith("https://www.cettire.com/products/"):
                    links.append(link)
            button = driver.find_element_by_css_selector("li[data-page='next']")
            button.click()
            time.sleep(1)
        except StaleElementReferenceException:
            continue   
        except Exception as e:
            print(e)
            break
    lines = []
    lines.append(["brand", "name", "price", "description", "gender", "category", "image_links"])
    for link in links:
        #print(link)
        driver.get(link)
        brand = driver.find_element_by_css_selector("p[itemprop='brand']").text
        #print(brand)
        name = driver.find_element_by_css_selector("h1[itemprop='name']").text
        #print(name)
        price = driver.find_element_by_css_selector("span[itemprop='price']").text[1:].replace(",","")
        #print(price)
        description = driver.find_element_by_css_selector("div[itemprop='description']").text.replace("\n", "")
        #print(description)
        directory = driver.find_elements_by_class_name("product-breadcrumb")[0]
        gender = directory.find_elements_by_class_name("product-breadcrumb__item")[1].text
        #print(gender)
        category = directory.find_elements_by_class_name("product-breadcrumb__item")[4].text
        #print(category)
        num_images = len(driver.find_elements_by_class_name("swiper-product-thumbs__img"))
        s = {*()}
        images = driver.find_elements_by_class_name("swiper-product-pc__img")
        for image in images:
            s.add(image.get_attribute("src"))
        #print(s)
        image_links = ""
        for image_link in s:
            image_links += image_link + ";"
        image_links = image_links[:-1]
        lines.append([brand, name, price, description, gender, category, image_links])
    with open("Cettire" + brand.replace(" ", "_") + ".csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for line in lines:
            writer.writerow(line)
    driver.close()

if __name__ == "__main__":
    scrape(sys.argv[1])
