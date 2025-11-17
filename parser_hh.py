import requests
from datetime import datetime, timedelta

start_date = datetime.now().isoformat()
end_date = (datetime.now() - timedelta(hours=1)).isoformat()

def get_vacancies(date_to):
    date_from = (datetime.fromisoformat(date_to)-timedelta(hours=1)).isoformat()
    response = requests.get(
        'https://api.hh.ru/vacancies/',
        params={'area': '2', 'industry': '7',
                'date_from': date_from, 'date_to': date_to}
    )
    return response.json()


if __name__=="__main__":
    print(get_vacancies(start_date))
