import requests

file_url = 'https://wildbox.ru/api/wb_dynamic/products/243184361'
params = {
        "date_from": "2025-06-25",
        "date_to": "2025-07-23",
        "limit": "1",
        "offset": "0",
        "ordering": "-rating",
        "extra_fields": "wh_avg_position_dynamic,count_keywords_dynamic,visibility_dynamic,frequency_dynamic,adverts_dynamic,damping_coefficient_dynamic"
        }


headers = {
    "Authorization": "Token bd7ecea7790cb43bf1dd720a9b6745f172004944",
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(file_url, headers=headers, params=params)
data = response.json()

print(data["name"])
print(data["image"])
print(data["rating"])
print(data["id"])
