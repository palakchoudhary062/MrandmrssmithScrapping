import csv
import cloudscraper
from bs4 import BeautifulSoup
from lxml import html

scraper = cloudscraper.create_scraper()

with open('hotels_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(['Hotel Name', 'City', 'Country'])

    page = 1
    while page < 203:
        url = f'https://www.mrandmrssmith.com/luxury-hotels?page={page}'
        resp = scraper.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        tree = html.fromstring(resp.content)
        
        hotel_infos = tree.xpath('//div[@class="hotelcard__content"]')
        for hotel_info in hotel_infos:
            hotel_name_h2 = hotel_info.xpath('.//h2[@class="hotelcard__content-hotelname"]/a')[0].text
            city_name = hotel_info.xpath('.//span[@class="location"]')[0].text
            country_name = hotel_info.xpath('.//span[@class="country"]')[0].text

            csvwriter.writerow([hotel_name_h2, city_name, country_name])

        page += 1
