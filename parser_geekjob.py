import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
URL = "https://geekjob.ru"


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info("Start function: {func_name}, args: {arguments}".format(func_name=func.__name__, arguments=",".join(args)))
        result = func(*args, **kwargs)
        logger.info("Successfully end: {func_name}".format(func_name=func.__name__))
        return result
    return wrapper


@logger
def get_pages_count(url: str) -> int:
    (response := requests.get(f"{url}/vacancies/")).raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    pages_number = soup.find("section", {"id": "paginator"}).find("small")

    return int(pages_number.text.strip().split()[-1])

@logger
def get_vacancies_links(page_url: str) -> List:
    soup = BeautifulSoup(requests.get(page_url).text, "lxml")
    links_list = [
        f"{URL}{link.find('a')['href']}"
        for link in soup.find(
            "ul", id="serplist", class_="collection serp-list"
        ).find_all("li", class_="collection-item avatar")
    ]
    return links_list

@logger
def parse_page(link: str) -> Dict:
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    common_block = (
        soup.find("body")
        .find("main", id="body", class_="container")
        .find("section", class_="section nhr-mcontent")
        .find("section", class_="col s12 m12 main")
        .find("header")
    )
    vacancy_name = (
        f"{common_block.find('h1').text}в {common_block.find('h5').find('a').text}"
    )
    location = common_block.find("div", class_="location")
    category = common_block.find("div", class_="category").text.split(" • ")
    tags = common_block.find("div", class_="tags").text.split(" • ")
    work_type,experience = common_block.find("div", class_="jobinfo").find("span", class_="jobformat").text.split("\n")
    salary = common_block.find("div", class_="jobinfo").find("span", class_="salary")
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
        tags=tags,
        salary=salary.text if salary else None,
        location=location.text if location else None,
        work_format=work_type,
        stack=category,
        description=description,
        experience=experience,
        url=link
    )


def main(url) -> List:
    vacancies_links = [
        page_link
        for page_number in range(1, get_pages_count(url) + 1)
        for page_link in get_vacancies_links(f"{URL}/vacancies/{page_number}")
    ]
    parsed_vacancies = [parse_page(link) for link in vacancies_links[:10]]
    with open("parsed_vacancies_geekjob.json", "w", encoding="utf-8") as file:
        json.dump(parsed_vacancies, file, ensure_ascii=False, indent=4 ,sort_keys=True)

    return parsed_vacancies


if __name__ == "__main__":
    main(URL)
