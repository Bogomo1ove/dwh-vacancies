import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import logging
from functools import wraps

months_to_numeric = {'января': '01',
                'февраля': '02',
                'марта': '03',
                'апреля': '04',
                'мая': '05',
                'июня': '06',
                'июля': '07',
                'августа': '08',
                'сентября': '09',
                'октября': '10',
                'ноября': '11',
                'декабря': '12'}

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
URL = "https://geekjob.ru/vacancies?sort=1"

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info(
            "Start function: {func_name}, args: {arguments}".format(
                func_name=func.__name__, arguments=list(args)
            )
        )
        result = func(*args, **kwargs)
        logger.info("Successfully end: {func_name}".format(func_name=func.__name__))
        return result
    return wrapper

class GeekJob:
    bucket_name = "geekjobvacancies"

    @staticmethod
    @logger
    def get_pages_count(url: str) -> int:
        (response := requests.get(f"{url}/vacancies/", verify=False)).raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        pages_number = soup.find("section", {"id": "paginator"}).find("small")
        return int(pages_number.text.strip().split()[-1])

    @staticmethod
    @logger
    def get_vacancies_links(page_url: str, date) -> List:
        soup = BeautifulSoup(requests.get(page_url, verify=False).text, "lxml")
        return [
            f"https://geekjob.ru{link.find('a')['href']}"
            for link in soup.find(
                "ul", id="serplist", class_="collection serp-list"
            ).find_all("li", class_="collection-item avatar")
            if (f"{link.find('time', class_='truncate datetime-info').text.split(' ')[0]}"
                f".{months_to_numeric[link.find('time', class_='truncate datetime-info').text.split(' ')[1].strip('\n')]}"
                f".{link.find('time', class_='truncate datetime-info').text.split(' ')[2] 
                if link.find('time', class_='truncate datetime-info').text.split(' ') == date.strftime('%Y')
            else date.strftime('%Y')}") == date.strftime('%d.%m.%Y')
        ]

    @staticmethod
    @logger
    def parse_page(date_to, link: str) -> Dict:
        soup = BeautifulSoup(requests.get(link, verify=False).text, "lxml")
        common_block = (
            soup.find("body")
            .find("main", id="body", class_="container")
            .find("section", class_="section nhr-mcontent")
            .find("section", class_="col s12 m12 main")
            .find("header")
        )
        creation_date = (f"{common_block.find('div', class_='time').text.split(' ')[0]}"
                         f".{months_to_numeric[common_block.find('div', class_='time').text.split(' ')[1]]}"
                         f".{date_to.strftime('%Y')}")
        vacancy_name = f"{common_block.find('h1').text}"
        location = common_block.find("div", class_="location")
        category = common_block.find("div", class_="category").text.split(" • ")
        work_type, experience = (
            common_block.find("div", class_="jobinfo")
            .find("span", class_="jobformat")
            .text.split("\n")
        )
        salary = common_block.find("div", class_="jobinfo").find(
            "span", class_="salary"
        )
        description = (
            soup.find("body")
            .find("main", id="body", class_="container")
            .find("section", class_="section nhr-mcontent")
            .find("section", class_="col s12 m12 main")
            .find("div", id="vacancy-description")
            .text
        )
        return dict(
            title=vacancy_name,
            salary=salary.text if salary else None,
            location=location.text if location else None,
            work_format=work_type,
            category=category,
            description=description,
            experience=experience,
            url=link,
            creation_date=creation_date
        )

    def get_vacancies(self, date_to):
        vacancies_links = [
            page_link
            for page_number in range(1, self.get_pages_count(URL) + 1)
            for page_link in self.get_vacancies_links(f"https://geekjob.ru/vacancies/{page_number}", date_to)
        ]
        return [self.parse_page(date_to, link) for link in vacancies_links]
