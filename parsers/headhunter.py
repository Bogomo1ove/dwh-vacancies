import requests
from datetime import timedelta


class HeadHunter:
    bucket_name = "headhuntervacancies"

    @staticmethod
    def get_response(date_to) -> dict:
        start_date = (date_to - timedelta(hours=12)).isoformat()
        (
            response := requests.get(
                "https://api.hh.ru/vacancies/",
                params={
                    "area": "2",
                    "industry": "7",
                    "date_from": start_date,
                    "date_to": date_to.isoformat(),
                },
            )
        ).raise_for_status()
        return response.json()

    @staticmethod
    def transform_data(data: dict) -> dict:
        return dict(
            salary_from=(data.get("salary") or {}).get("from"),
            salary_to=(data.get("salary") or {}).get("to"),
            title=data["name"],
            location=data["area"]["name"] or None,
            work_format=[dat["name"] for dat in data["work_format"]]
            in data["work_format"]
            or None,
            category=[element["name"] for element in data["professional_roles"]]
            or None,
            description=data["snippet"]["responsibility"] or None,
            experience=data["experience"]["name"] or None,
            url=data["alternate_url"],
        )

    def get_vacancies(self, date_to):
        return [
            self.transform_data(vacancy)
            for vacancy in self.get_response(date_to)["items"]
        ]
