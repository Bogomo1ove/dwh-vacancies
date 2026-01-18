import requests
from datetime import datetime, timedelta
import json


class HeadHunter:

    @staticmethod
    def get_response(date_to) -> dict:
        start_date = (date_to - timedelta(hours=12)).isoformat()
        response = requests.get('https://api.hh.ru/vacancies/',
                params = {'area': '2', 'industry': '7',
                          'date_from': start_date, 'date_to': date_to.isoformat()}
                          )
        return response.json()


    @staticmethod
    def transform_data(data: dict) -> dict:
        return dict(salary_from = (data.get("salary") or {}).get("from"),
                    salary_to = (data.get("salary") or {}).get("to"),
                    title=data['name'],
                    location = data['area']['name'] or None,
                    work_format = [dat['name'] for dat in data['work_format']] in data['work_format'] or None,
                    category = [element["name"] for element in data["professional_roles"]] or None,
                    description = data['snippet']['responsibility'] or None,
                    experience = data['experience']['name'] or None,
                    url = data['alternate_url']
                    )

    @staticmethod
    def dump_response(data):
        if data:
            with open(f'{datetime.now().replace(microsecond=0).isoformat()}.json', "w") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            raise Exception("Отсутсвует файл для записи!")
        return f'{datetime.today().isoformat()}.json'

    @staticmethod
    def get_vacancies(date_to):
        return HeadHunter.dump_response(
            [HeadHunter.transform_data(vacancy) for vacancy in HeadHunter.get_response(date_to)['items']])
