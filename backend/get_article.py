import requests
import pandas as pd

def get_article_metrics(article_id):
    file_url = 'https://wildbox.ru/api/wb_dynamic/products'
    params = {
        "product_ids": str(article_id),
        "period": "7",
        "limit": "1",
        "extra_fields": "proceeds,orders,price,quantity,discount,rating,reviews"
    }

    headers = {
        "Authorization": "Token bd7ecea7790cb43bf1dd720a9b6745f172004944",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(file_url, headers=headers, params=params)
        data = response.json()['results'][0]

        metrics = {
            'product_id': data['id'],
            'discount': data['discount'],
            'product_rating': data['rating'],
            'price': data['price'],
            'quantity': data['quantity'],
            'proceeds': data['proceeds'],
            'orders': data['orders'],
            'reviews_count': data['reviews']
        }

        return metrics

    except Exception as e:
        print(f"Error getting metrics: {e}")
        return None

file_url = 'https://wildbox.ru/api/wb_dynamic/products'
params = {
        "product_ids": "243184361",
        "period": "7",
        "limit": "1",
        "extra_fields": "proceeds,proceeds_dynamic,orders,orders_dynamic,price,sales_percent,price_dynamic,quantity,quantity_dynamic,in_stock_days,out_of_stock_days,in_stock_percent,in_stock_orders_avg,in_stock_proceeds,lost_proceeds,lost_proceeds_dynamic,lost_orders,lost_orders_dynamic,discount,discount_dynamic,orders_failed,orders_failed_dynamic,proceeds_failed,proceeds_failed_dynamic,sales,sales_dynamic,sales_proceeds,sales_proceeds_dynamic,reviews,rating_dynamic,reviews_dynamic,rating,last_price"
        }


headers = {
    "Authorization": "Token bd7ecea7790cb43bf1dd720a9b6745f172004944",
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(file_url, headers=headers, params=params)
data = response.json()

print(data)



