import requests
import os
from datetime import datetime

def download_data_for_city(city, headers, search_query="Футболка", articul=None):
    # Direct product URL if articul is provided
    if articul:
        file_url = f'https://wildbox.ru/api/wb_dynamic/products/{articul}/'
        params = {
            "date_from": "2025-06-25",
            "date_to": "2025-07-23",
            "limit": "1",
            "offset": "0",
            "ordering": "-rating",
            "extra_fields": "wh_avg_position_dynamic,count_keywords_dynamic,visibility_dynamic,frequency_dynamic,adverts_dynamic,damping_coefficient_dynamic"
        }
    else:
        # Original search URL
        file_url = 'https://wildbox.ru/api/wb_dynamic/products/'
        params = {
            "city": city,
            "wb_search": search_query,
            "period": "30",
            "limit": "200",
            "ordering": "product_ids",
            "extra_fields": "id,auto_adv,cpm,color_groups,position_dynamic"
        }
    
    try:
        response = requests.get(file_url, headers=headers, params=params)
        data = response.json()
        
        # If using articul, we already have the data
        if articul:
            needed_ids = [articul]
        else:
            needed_ids = [item['id'] for item in data['results'] if 'id' in item]
        
        new_down_url = 'https://wildbox.ru/api/wb_dynamic/products/export/'
        params_down = {
            "product_ids": ",".join(map(str, needed_ids)),
            "product_ads_min": "500",
            "short_price_sigment": "false",
            "city": city,
            "wb_search": search_query,
            "date_from": "2025-06-24",
            "date_to": "2025-07-23",
            "limit": "200",
            "offset": "0",
            "ordering": "product_ids",
            "extra_fields": "product,subject,id,brand,seller,auto_adv,page_wb,product_ads,color_groups,cpm,create_date,proceeds,price,weighted_price,damping_coefficient,discount,orders,quantity,lost_proceeds,lost_orders,in_stock_percent,in_stock_days,out_of_stock_days,in_stock_orders_avg,in_stock_proceeds,category_count,proceeds,color_groups,images,auto_adv"
        }
        
        down_response = requests.get(new_down_url, headers=headers, params=params_down)
        
        if down_response.status_code == 200:
            content_type = down_response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = down_response.json()
                file_url = data['url']
                final_response = requests.get(file_url)
                
                date_str = datetime.now().strftime('%Y-%m-%d')
                os.makedirs(f'data/{date_str}', exist_ok=True)
                
                filename = f'data/{date_str}/main_data_{city.lower()}.xlsx'
                with open(filename, 'wb') as f:
                    f.write(final_response.content)
                print(f"Сохранен файл для города {city}: {filename}")
            else:
                print(f"Неверный тип контента для города {city}")
        else:
            print(f"Ошибка запроса для города {city}: {down_response.status_code}")
            
    except Exception as e:
        print(f"Ошибка при обработке города {city}: {str(e)}")

def main():
    cities = [
        "Москва",
        "Санкт-Петербург",
        "Новосибирск",
        "Хабаровск",
        "Екатеринбург",
        "Казань",
        "Краснодар"
    ]
    
    headers = {
        "Authorization": "Token bd7ecea7790cb43bf1dd720a9b6745f172004944",
        "User-Agent": "Mozilla/5.0"
    }
    
    for city in cities:
        print(f"\nЗагрузка данных для города: {city}")
        download_data_for_city(city, headers)
    
    from jformating import merge_city_data
    merged_df = merge_city_data('data')
    print("All data has been downloaded and merged successfully!")

if __name__ == "__main__":
    main()


