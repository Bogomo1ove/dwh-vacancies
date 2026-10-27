# import os

# import requests

# from datetime import timedelta


# class HeadHunter:
#     bucket_name = "headhuntervacancies"

#     @staticmethod
#     def get_response(date_to) -> dict:
#         access_token = os.getenv(
#             "HH_ACCESS_TOKEN"
#         )

#         if not access_token:
#             raise ValueError(
#                 "Переменная HH_ACCESS_TOKEN "
#                 "не найдена в контейнере"
#             )

#         headers = {
#             "HH-User-Agent": (
#                 "MyAirflowBot/1.0 "
#                 "(vladbogenka@yandex.ru)"
#             ),
#             "Authorization": (
#                 f"Bearer {access_token}"
#             ),
#         }

#         start_date = (
#             date_to - timedelta(hours=24)
#         ).isoformat()

#         response = requests.get(
#             "https://api.hh.ru/vacancies/",
#             params={
#                 "area": "2",
#                 "industry": "7",
#                 "date_from": start_date,
#                 "date_to": date_to.isoformat(),
#             },
#             headers=headers,
#             timeout=30,
#         )

#         print(
#             "Статус ответа HH:",
#             response.status_code,
#         )

#         if response.status_code != 200:
#             print(response.text)
#             print(response.headers)

#         response.raise_for_status()

#         return response.json()

#     @staticmethod
#     def transform_data(data: dict) -> dict:
#         salary_data = data.get("salary")

#         if salary_data:
#             salary_from = salary_data.get("from")
#             salary_to = salary_data.get("to")
#             currency = salary_data.get("currency")

#             if (
#                 salary_from is not None
#                 and salary_to is not None
#             ):
#                 salary = (
#                     f"от {salary_from} "
#                     f"до {salary_to} "
#                     f"{currency}"
#                 )

#             elif salary_from is not None:
#                 salary = (
#                     f"от {salary_from} "
#                     f"{currency}"
#                 )

#             elif salary_to is not None:
#                 salary = (
#                     f"до {salary_to} "
#                     f"{currency}"
#                 )

#             else:
#                 salary = None

#         else:
#             salary = None

#         work_format = ", ".join(
#             item["name"]
#             for item in data.get(
#                 "work_format",
#                 [],
#             )
#         )

#         category = ", ".join(
#             item["name"]
#             for item in data.get(
#                 "professional_roles",
#                 [],
#             )
#         )

#         return {
#             "source": "headhunter",

#             "title": data["name"],

#             "salary": salary,

#             "location": (
#                 data.get("area") or {}
#             ).get("name"),

#             "work_format": (
#                 work_format or None
#             ),

#             "category": (
#                 category or None
#             ),

#             "description": (
#                 data.get("snippet") or {}
#             ).get("responsibility"),

#             "experience": (
#                 data.get("experience") or {}
#             ).get("name"),

#             "url": data["alternate_url"],

#             "creation_date": (
#                 data["created_at"][:10]
#             ),
#         }

#     def get_vacancies(self, date_to):
#         response_data = self.get_response(
#             date_to
#         )

#         vacancies = [
#             self.transform_data(vacancy)
#             for vacancy
#             in response_data["items"]
#         ]

#         print(
#             "Получено вакансий с HH: "
#             f"{len(vacancies)}"
#         )

#         return vacancies