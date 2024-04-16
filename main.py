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
        print("current page = ", page)
        url = f'https://www.mrandmrssmith.com/luxury-hotels?page={page}'
        resp = scraper.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        tree = html.fromstring(resp.content)
        
        hotel_infos = tree.xpath('//div[@class="hotelcard__content"]')
        if len(hotel_infos) == 0:
            break
        for hotel_info in hotel_infos:
            hotel_name_h2 = hotel_info.xpath('.//h2[@class="hotelcard__content-hotelname"]/a')[0].text
            city_elements = hotel_info.xpath('.//span[@class="location"]')
            city_name = city_elements[0].text if city_elements else "N/A"
            country_elements = hotel_info.xpath('.//span[@class="country"]')
            country_name = country_elements[0].text.replace(',', '') if country_elements else city_name

            csvwriter.writerow([hotel_name_h2, city_name, country_name])

        page += 1
