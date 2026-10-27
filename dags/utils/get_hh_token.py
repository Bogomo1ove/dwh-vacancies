# import os
# import requests


# CLIENT_ID = os.getenv("HH_CLIENT_ID")
# CLIENT_SECRET = os.getenv("HH_CLIENT_SECRET")

# AUTHORIZATION_CODE = "KK9PE4EQHUD1DKD3P7RME5DN028G912BKV36M6VO6P47TN860QOS1NBC1T8SL7V8"

# response = requests.post(
#     "https://hh.ru/oauth/token",
#     data={
#         "grant_type": "authorization_code",
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "code": AUTHORIZATION_CODE,
#         "redirect_uri": "http://localhost:8000/callback",
#     },
# )

# print("Статус:", response.status_code)
# print("Ответ HH:", response.text)