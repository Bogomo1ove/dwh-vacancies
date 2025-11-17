import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, List


URL = "https://getmatch.ru/vacancies"


def get_pages_count(url: str) -> int:
    (response := requests.get(url, params={"p": "1"})).raise_for_status()
    pages_count = (
        BeautifulSoup(response.text, "lxml")
        .find("div", class_="b-pagination")
        .find("div", class_="b-pagination-pages d-none d-md-flex")
    )
    return max(
        int(page) for page in pages_count.text.strip().split("  ") if page.isdigit()
    )


def get_vacancy_list(page_number: int) -> List:
    (response := requests.get(URL, params={"p": f"{page_number}"})).raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    vacancies_block = soup.find("div", class_="col-md-8 col-sm-12").find_all(
        "div", class_="ng-star-inserted"
    )
    return list(
        set(vacancy.find("div", class_="b-vacancy-card") for vacancy in vacancies_block)
        - set(
            vacancy.find("div", class_="b-vacancy-card vacancy-one-day-offer")
            for vacancy in vacancies_block
        )
    )


def get_vacancies_links(list_vacancies: List) -> List:
    return [
        "https://getmatch.ru{uri}".format(
            uri=vacancy.find("div", class_="b-vacancy-card-title").find("a")["href"]
        )
        for vacancy in list_vacancies
    ]


def parse_link(url: str) -> Dict:
    (response := requests.get(url)).raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    common_block = soup.find("div", class_="col-md-8 col-sm-12")
    vacancy_name = common_block.find("section", class_="b-header")
    vacancy_tags = vacancy_name.find("div", class_="b-breadcrumbs").find_all(
        "span", class_="b-breadcrumbs__item"
    )
    tags_list = [vacancy_tag.text for vacancy_tag in vacancy_tags][1:]
    vacancy_title = f"{vacancy_name.find('h1').text}{vacancy_name.find('h2').text}"
    salary = vacancy_name.find("h3")
    spam_location = common_block.find("div", class_="b-vacancy-locations").find(
        "span", class_="g-label b-vacancy-locations--first g-label-secondary"
    )
    spam_work_type = common_block.find("div", class_="b-vacancy-locations").find(
        "span", class_="g-label g-label-zanah"
    )
    div_specs = common_block.find("div", class_="section b-specs").find_all(
        "div", class_="row"
    )
    spec_dict = {
        spec.find("div", class_="col b-term").text: spec.find(
            "div", class_="col b-value"
        ).text
        for spec in div_specs
    }
    stack_list = (
        [
            tech.text
            for tech in common_block.find("section", class_="b-vacancy-stack").find(
                "div", class_="b-vacancy-stack-container"
            )
            if tech.text != ""
        ]
        if common_block.find("section", class_="b-vacancy-stack")
        else []
    )
    description = common_block.find(
        "section", class_="b-vacancy-description markdown"
    ).text

    return dict(
        title=vacancy_title,
        tags=tags_list,
        salary=salary.text if salary else None,
        location=spam_location.text if spam_location else None,
        work_format=spam_work_type.text if spam_work_type else None,
        specifications=spec_dict,
        stack=stack_list,
        description=description,
    )


def parse_vacancies(url: str) -> List:
    return [
        parse_link(link)
        for page in range(1, get_pages_count(url) + 1)
        for link in get_vacancies_links(get_vacancy_list(page))
    ]


if __name__ == "__main__":
    with open("vacancies.json", "w") as file:
        json.dump(parse_vacancies(URL), file)
