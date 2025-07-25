import requests

file_url = 'https://wildbox.ru/api/wb_dynamic/products/'
params = {
        "product_id": "243184361",
        "phrase": "Карандаш",
        "pages_max": "30",
        "extra_fields" : "city, verbose, page, position"
        }


headers = {
    "Authorization": "Token bd7ecea7790cb43bf1dd720a9b6745f172004944",
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(file_url, headers=headers, params=params)
data = response.json()

# needed_ids = []
# for item in data['results']:
#     if 'id' in item:
#         needed_ids.append(item['id'])

print(data)