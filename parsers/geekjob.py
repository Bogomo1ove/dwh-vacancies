import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import logging
from functools import wraps


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
URL = "https://geekjob.ru"


class GeekJob:
    bucket_name = "geekjobvacancies"

    @staticmethod
    def logger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(__name__)
            logger.info(
                "Start function: {func_name}, args: {arguments}".format(
                    func_name=func.__name__, arguments=",".join(args)
                )
            )
            result = func(*args, **kwargs)
            logger.info("Successfully end: {func_name}".format(func_name=func.__name__))
            return result

        return wrapper

    @staticmethod
    @logger
    def get_pages_count(url: str) -> int:
        (response := requests.get(f"{url}/vacancies/", verify=False)).raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        pages_number = soup.find("section", {"id": "paginator"}).find("small")
        return int(pages_number.text.strip().split()[-1])

    @staticmethod
    @logger
    def get_vacancies_links(page_url: str) -> List:
        soup = BeautifulSoup(requests.get(page_url, verify=False).text, "lxml")
        links_list = [
            f"{URL}/{link.find('a')['href']}"
            for link in soup.find(
                "ul", id="serplist", class_="collection serp-list"
            ).find_all("li", class_="collection-item avatar")
        ]
        return links_list

    @staticmethod
    @logger
    def parse_page(link: str) -> Dict:
        soup = BeautifulSoup(requests.get(link, verify=False).text, "lxml")
        common_block = (
            soup.find("body")
            .find("main", id="body", class_="container")
            .find("section", class_="section nhr-mcontent")
            .find("section", class_="col s12 m12 main")
            .find("header")
        )
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
            stack=category,
            description=description,
            experience=experience,
            url=link,
        )

    def get_vacancies(self):
        vacancies_links = [
            page_link
            for page_number in range(1, self.get_pages_count(URL) + 1)
            for page_link in self.get_vacancies_links(f"{URL}/vacancies/{page_number}")
        ]
        return [self.parse_page(link) for link in vacancies_links]
