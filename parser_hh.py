import requests
from datetime import datetime, timedelta
import json


def get_vacancies() -> dict:
    date_from = (datetime.now() - timedelta(hours=12)).isoformat() # todo: сделать идемпотентным (передавать в эту функцию определенное время-начало таски)
    date_to = datetime.now().isoformat()
    response = requests.get('https://api.hh.ru/vacancies/',
            params = {'area': '2', 'industry': '7',
                      'date_from': date_from, 'date_to': date_to}
                      )
    return response.json()



def transform_data(data: dict) -> dict:
    print(f"Сбор данных из вакансии: {data['name']}, ссылка на вакансию: {data['url']}")
    if data['salary']:
        if data['salary']['from'] is None:
            salary = f'{str(data['salary']['to'])}RUB'
        elif data['salary']['to'] is None:
            salary = f'{str(data['salary']['from'])}RUB'
        else:
            salary = f'{str(data['salary']['from'])} - {str(data['salary']['to'])}RUB'
    else:
        salary = 'Не указано'
    return dict(title=data['name'],
                salary = salary,
                location = data['area']['name'] if data['area']['name'] else 'Не указано',
                work_format = [dat['name'] for dat in data['work_format']] if [dat['name'] for dat in data['work_format']] else 'Не указано',
                category = [dat['name'] for dat in data['professional_roles']] if [dat['name'] for dat in data['professional_roles']] else 'Не указано',
                description = data['snippet']['responsibility'] if data['snippet']['responsibility'] else 'Не указано',
                experience = data['experience']['name'] if data['experience']['name'] else 'Не указано',
                url = data['alternate_url']
                )


def dump_response(data):
    if data:
        with open(f'{datetime.now().replace(microsecond=0).isoformat()}.json', "w") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)
                    # print(f'Файл hh_parsed_vacancies: {datetime.now().replace(microsecond=0).isoformat()} сохранен.')
    else:
        raise Exception("Отсутсвует файл для записи!")
    return f'{datetime.now().replace(microsecond=0).isoformat()}.json'


def get_vacancies_hh(start_from):
    return dump_response([transform_data(vacancy) for vacancy in get_vacancies()['items']])

