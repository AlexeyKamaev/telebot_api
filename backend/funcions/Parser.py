import cloudscraper
from math import ceil
import re
import json
import random
from bs4 import BeautifulSoup
import time
from fake_headers import Headers

def get_headers():

    """
    Generate headers for HTTP requests.

    Returns:
        dict[str, str]: Dictionary of headers.
    """

    headers = {
        'authority': 'cian.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'refer': 'https://www.google.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"115.0.5790.110"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.110", "Chromium";v="115.0.5790.110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': 'Windows',
        'sec-ch-ua-platform-version': '15.0.0',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': Headers(browser='chrome', os='win').generate()['User-Agent'],
        'x-client-data': '#..',
    }
    return headers

class Parser():

    def __init__(self, proxy=None, url=None):
        if url == None:
            self.url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&offer_type=flat&region=1&totime=-2'
        else:
            self.url = url
            
        self.proxy = proxy
        self.scraper = cloudscraper.create_scraper()

    def build_url(self, rooms, min_price, max_price, p):
        rooms = "".join([f"&room{room}=1" for room in rooms])
        price = f"&minprice={min_price}&maxprice={max_price}"
        url = self.url + f"&p={p}"+ rooms + price
        return url

    def get_offers(self, rooms, min_price, max_price, pages=54):
        urls = set()

        find_n_pages = True

        page_counter = 1

        while page_counter <= pages:
            
            print(f"Parsing page {page_counter} out of {pages} pages")
            print(f"{len(urls)} urls found already")
            url = self.build_url(rooms, min_price, max_price, page_counter)
            print(f"Scraping {url}")
            random_proxy = random.choice(self.proxy)
            headers = get_headers()
            
            n_attempts = 0

            while n_attempts < 3:
                try:
                    response = self.scraper.get(url, headers=headers, proxies=random_proxy)
                    html = response.text
                    if find_n_pages:
                        try:
                            pages = self.get_n_pages(html)
                            find_n_pages = False
                        except Exception as e:
                            print(f"Failed to get number of pages because of : {e}")

                    if response.status_code == 429:
                        time.sleep(15)

                    
                    elif response.status_code == 200:
                        bs = BeautifulSoup(html, 'html.parser')
                        url_tags = bs.find_all('div', {'data-name': 'GeneralInfoSectionRowComponent'})
                        for tag in url_tags:
                            url_tag = tag.find('a')
                            if url_tag:
                                try:
                                    link = url_tag['href']
                                    if 'www.cian.ru/sale' in link:
                                        urls.add(link)
                                        n_attempts = 3
                                except KeyError:
                                    pass
                    n_attempts += 1

                except Exception as e:
                    print('Error: ', e)
                    n_attempts += 1
                                
            page_counter += 1
        print(f"Collected {len(urls)} urls to parse")
        return urls           

    def get_n_pages(self, html):
        bs = BeautifulSoup(html, "html.parser")
        n_adds = bs.find_all('div', {'data-name': 'SummaryHeader'})[0].find('h5').text
        n_pages = min(54, ceil(int(re.sub(r'\D', '', n_adds))/28))
        return n_pages


    def extract_data(self, data, keys):
        try:
            value = data
            for key in keys:
                value = value[key]
            return value
        except (KeyError, IndexError):
            return None


    def get_data(self, urls, max_tries=3):
        scraped_data = []
        for url in urls:
            n_attempts = 0
            while n_attempts < max_tries:
                try:
                    # proxy = random.choice(self.proxy)
                    headers = get_headers()
                    response = self.scraper.get(url=url, headers=headers)#, proxies=proxy)
                    print(f"Trying to parse {url}, response status: {response.status_code}")
                    if response.status_code == 429:
                            time.sleep(15)
                    elif response.status_code == 200:
                            html = response.text
                            data = self.parse_data(html)
                            scraped_data.append(data)
                            break
                except Exception as e:
                    print("Failed attempt to get data because of : ", e)
                n_attempts += 1
        print(f"Amount of aquired data: {len(scraped_data)}")
        return scraped_data

    def parse_data(self, html):
        bs = BeautifulSoup(html, "html.parser")
        scripts = bs.find_all("script")

        for script in scripts:
            if "window._cianConfig['frontend-offer-card']" in script.text:
                start_index = script.text.find('concat([') + 7
                end_index = script.text.rfind(']') + 1
                json_data = script.text[start_index:end_index]
                parsed_json = json.loads(json_data)
                data_index = len(parsed_json) - 1
                while data_index >= 0:
                    try:
                        parsed_json[data_index]['value']['offerData']
                        break
                    except (TypeError, KeyError):
                        data_index -= 1

                data = {}

                data['offer_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'offerType']) or 'Нет данных'
                data['city'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'address', 0, 'fullName']) or 'Нет данных'
                data['okrug'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'address', 1, 'fullName']) or 'Нет данных'
                data['raion'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'address', 2, 'fullName']) or 'Нет данных'
                data['street'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'address', 3, 'fullName']) or 'Нет данных'
                data['house'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'address', 4, 'fullName']) or 'Нет данных'
                data['room_count'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'roomsCount']) or 0
                data['room_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'roomType']) or 'Нет данных'
                data['loggiasCount'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'loggiasCount']) or 0
                data['latitude'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'coordinates', 'lat']) or 0.0
                data['longitude'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'coordinates', 'lng']) or 0.0
                data['id'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'id']) or 0
                data['phone'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'phones', 0, 'countryCode']) + self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'phones', 0, 'number']) or 0
                data['flat_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'flatType']) or 'Нет данных'
                data['is_apartment'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'isApartments']) or False
                data['is_penthause'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'isPenthouse']) or False
                data['total_area'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'totalArea']) or 0
                data['living_area'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'livingArea']) or 0
                data['kitchen_area'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'kitchenArea']) or 0
                data['all_rooms_area'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'allRoomsArea']) or 0
                data['combined_wcs_count'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'combinedWcsCount']) or 0
                data['repair_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'repairType']) or 'Нет данных'
                data['floor'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'floorNumber']) or 0
                data['price'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'bargainTerms', 'price']) or 0
                data['currency'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'bargainTerms', 'currency']) or 'Нет данных'
                data['material_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'building', 'materialType']) or 'Нет данных'
                data['floors_count'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'building', 'floorsCount']) or 0
                data['build_year'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'building', 'buildYear']) or 0
                data['ceiling_height'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'building', 'ceilingHeight']) or 0
                data['house_material_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'building', 'houseMaterialType']) or 'Нет данных'
                data['edit_time'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'editDate']) or 0
                data['publication_date'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'publicationDate']) or 0
                data['house_material_bti'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'bti', 'houseData', 'houseMaterialType']) or 'Нет данных'
                data['house_heating_supply'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'bti', 'houseData', 'houseHeatSupplyType']) or 'Нет данных'
                data['is_emergency'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'bti', 'houseData', 'isEmergency']) or False
                data['house_overlap_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'bti', 'houseData', 'houseOverlapType']) or 'Нет данных'
                data['metro'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'undergrounds', 0, 'name']) or 'Нет данных'
                data['metro_time'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'undergrounds', 0, 'travelTime']) or 0
                data['travel_type'] = self.extract_data(parsed_json, [data_index, 'value', 'offerData', 'offer', 'geo', 'undergrounds', 0, 'travelType']) or 'Нет данных'

        return data

    def parse(self, rooms, min_price, max_price):
        urls = self.get_offers(rooms, min_price, max_price)
        data = self.get_data(urls)
        print(f"Collected {len(data)} real estate adds data")
        return data