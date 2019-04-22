import csv
import requests
from bs4 import BeautifulSoup
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')
# Create a file to write to, add headers row
os.remove('bestbuy-products.csv')
file = csv.writer(open('bestbuy-products.csv', 'a'))
file.writerow(['ID', 'Name', 'Link', 'Image', 'Price', 'Category'])

def scrape_single_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    l = []
    all_product = soup.find_all("li", class_="listing-item")
    for item in all_product:
        # print(item)
        d = { }
        product_name = item.find("h4", {"class":"prod-title"}).find("a")
        product_link = 'https://www.bestbuy.ca' + str(product_name.get("href"))
        # print(product_link)
        product_name = product_name.get_text()
        # print(product_name)
        product_price = item.find("span", {"class":"amount"}).get_text()
        # print(product_price)
        product_image = item.find("div", {"class":"prod-image"}).find("img").get("src")
        # print(product_image)
        d["product_link"] = product_link
        d["product_name"] = product_name
        d["product_image"] = product_image
        d["product_price"] = product_price

        prod_page = requests.get(product_link)
        prod_soup = BeautifulSoup(prod_page.content, 'html.parser')

        product_id = prod_soup.find("ul", {"class": "list-sub-text"}).find("span", {"id":"ctl00_CP_ctl00_PD_lblSku"}).get_text()
        # print(product_id)
        d["product_id"] = product_id
        product_category = prod_soup.find("div", {"class":"breadcrumb-row"}).find_all("span", {"property":"name"})[len(prod_soup.find("div", {"class":"breadcrumb-row"}).find_all("span", {"property":"name"})) - 2].get_text()
        d["product_category"] = product_category
        # print(product_category)
        file.writerow([product_id, product_name, product_link, product_image, product_price, product_category])
        l.append(d)
    # print(l)


if __name__ == '__main__':
    scrape_single_page("https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?type=product&filter=brandName%253aALIENWARE&fromBrandStore=alienware&page=1&pageSize=96")
    scrape_single_page("https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?type=product&filter=brandName%253aASUS&fromBrandStore=asus&page=1&pageSize=96")