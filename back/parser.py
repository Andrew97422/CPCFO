from time import sleep, time

from parse_hh_data import download, parse
import requests
from bs4 import BeautifulSoup
import threading
import json

start = time()


class Parser:
    def __init__(self):
        self.url = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36'
        }
        self.st_accept = "text/html"
        self.st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) " \
                            "Version/15.4 " \
                            "Safari/605.1.15"

        self.headers = {
            "Accept": self.st_accept,
            "User-Agent": self.st_useragent
        }

    def get_text(self, url):
        self.url = url
        req = requests.get(self.url, self.headers)
        src = req.text
        return src


class Course:
    def __init__(self):
        self.title = None
        self.description = None
        self.price = None
        self.url = None

    def print(self):
        print(self.title)
        print(self.description)
        print(self.price)
        print(self.url)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "url": self.url
        }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)


def parse_text(url):
    courses = []
    parser = Parser()
    src = parser.get_text(url)
    threads = []

    soup = BeautifulSoup(src, 'html.parser')
    for result in soup.find_all('div', 'direction-card ui-col-md-6 {[ui_col_xxxl]}'):
        course = Course()

        def parse(result, course_parse):
            # global courses
            # sleep(100)
            for child in result.find_all('span', 'direction-card__title-text ui-text-body--1 ui-text--medium'):
                course_parse.title = child.text.strip()

            for child in result.find_all('a', 'card_full_link'):
                url1 = child.attrs['href']
                course_parse.url = url1
                parse_ref = Parser()
                src_ref = parse_ref.get_text(url1)
                soup_ref = BeautifulSoup(src_ref, 'html.parser')

                result_ref = soup_ref.select('body > div:nth-child(23) > div > '
                                             'div.gkb-promo__content-container.ui-grid-container.ui-grid-gap > '
                                             'div.gkb-promo__description > '
                                             'div.gkb-promo__price.ui-col-md-6.ui-col-lg-12.ui-col-xl-6 > div > '
                                             'div.gkb-promo__price-current > span.ui-text-heading--2.ui-text--medium')

                if len(result_ref) > 0:
                    course_parse.price = result_ref[0].text.strip()
                    break

                result_ref = soup_ref.find_all('span', 'price__format')
                if len(result_ref) > 0:
                    course_parse.price = result_ref[0].text.strip()
                    break

                result_ref = soup_ref.find_all('span', 'ui-text-heading--2 ui-text--medium')
                if len(result_ref) > 0:
                    course_parse.price = result_ref[0].text.strip()
                    break

                result_ref = soup_ref.select('#form-bottom > div.ui-grid-container.ui-grid-gap > div > '
                                             'div.enroll-banner__price-container > div.enroll-banner__price-current >'
                                             ' span')
                if len(result_ref) > 0:
                    course_parse.price = result_ref[0].text.strip()
                    break

                resul_ref = soup_ref.select('#form-bottom > div > div.ui-grid-container.ui-grid-gap > div > '
                                            'div.enroll-banner__price-container > div.enroll-banner__price-current > '
                                            'span')
                if len(resul_ref) > 0:
                    course_parse.price = resul_ref[0].text.strip()
                    break

            for child in result.find_all('div', 'direction-card__text'):
                course_parse.description = child.text.strip()

            courses.append(course_parse)

        t = threading.Thread(target=parse, args=(result, course,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    return courses


class ParseHH:
    def __init__(self, url):
        self.url = url

    def extract_id(self):
        self.id = self.url.split('vacancy/')[1].split('/')[0]

    def parse(self):
        self.extract_id()
        return download.vacancy(self.id)

    def description(self):
        self.extract_id()
        soup = BeautifulSoup(download.vacancy(self.id)['description'], 'html.parser')
        return soup.text

    def title(self):
        self.extract_id()
        soup = BeautifulSoup(download.vacancy(self.id)['name'], 'html.parser')
        return soup.text

# courses = parse_text('https://gb.ru/courses/all')
# print(courses[0].to_dict())
# print(courses)
# courses = [course.to_dict() for course in courses]
# data = json.dumps(courses, indent=4, ensure_ascii=False)
# with open("courses.json", "w", encoding='utf-8') as file:
#     file.write(data)
#    json.dump([ob.__dict__ for ob in courses], file, default=lambda o: o.__dict__,
#              sort_keys=True, indent=4, ensure_ascii=False)
