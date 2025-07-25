import pandas as pd
import os
from datetime import datetime
from get_article import get_article_metrics  # Теперь этот импорт должен работать

CITY_MAPPING = {
    'москва': 'position_msk',
    'санкт-петербург': 'position_spb',
    'новосибирск': 'position_nvsb',
    'хабаровск': 'position_hab',
    'екатеринбург': 'position_ekb',
    'казань': 'position_kaz',
    'краснодар': 'position_kras'
}

def process_excel_file(file_path):
    df = pd.read_excel(file_path, skiprows=7)
    
    df = df[df['Тип рекламы'] != 'c']
    
    column_mapping = {
        'Артикул': 'product_id',
        'Выручка': 'proceeds',
        'Заказы': 'orders',
        'Средняя цена без СПП': 'price',
        'Общая скидка без СПП': 'discount',
        'Остатки на конец периода': 'quantity',
        'Позиция в выдаче': 'position',
        'Рейтинг товара': 'product_rating',
        'Рейтинг продавца': 'seller_rating',
        'Количество отзывов': 'reviews_count',
        'ID бренда': 'brand_id',
        'Эффективность доставки': 'delivery_efficiency_wh_avg_pos'
    }
    
    df = df.rename(columns=column_mapping)
    return df

def merge_city_data(data_folder, search_id=None):
    print(f"Starting merge with search_id: {search_id}")  
    date_str = datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join(data_folder, date_str)
    
    try:
        print("Processing files in folder:", folder_path)  
        all_products = set()
        city_data = {}
        metrics_data = {} 
        
        for filename in os.listdir(folder_path):
            if filename.startswith('main_data_') and filename.endswith('.xlsx'):
                print(f"Processing file: {filename}")  # Debug log
                file_path = os.path.join(folder_path, filename)
                df = process_excel_file(file_path)
                city = filename.replace('main_data_', '').replace('.xlsx', '')
                city_data[city] = df
                all_products.update(df['product_id'].tolist())
                
                for _, row in df.iterrows():
                    product_id = row['product_id']
                    if product_id not in metrics_data:
                        metrics_data[product_id] = {
                            'delivery_efficiency_wh_avg_pos': row.get('delivery_efficiency_wh_avg_pos', 0),
                            'discount': row.get('discount', 0),
                            'product_rating': row.get('product_rating', 0),
                            'seller_rating': row.get('seller_rating', 0),
                            'price': row.get('price', 0),
                            'quantity': row.get('quantity', 0),
                            'proceeds': row.get('proceeds', 0),
                            'orders': row.get('orders', 0)
                        }
        
        if search_id and search_id not in all_products:
            print(f"Adding search_id {search_id} to products")  # Debug log
            all_products.add(search_id)
            metrics = get_article_metrics(search_id)
            if metrics:
                metrics_data[search_id] = metrics
        
        # Create final dataframe structure with all required columns
        product_ids = sorted(list(all_products))
        final_data = {
            'product_id': product_ids,
            'position_msk': [None] * len(product_ids),
            'position_spb': [None] * len(product_ids),
            'position_nvsb': [None] * len(product_ids),
            'position_hab': [None] * len(product_ids),
            'position_ekb': [None] * len(product_ids),
            'position_kaz': [None] * len(product_ids),
            'position_kras': [None] * len(product_ids),
            # Добавляем колонки для метрик
            'delivery_efficiency_wh_avg_pos': [0] * len(product_ids),
            'discount': [0] * len(product_ids),
            'product_rating': [0] * len(product_ids),
            'seller_rating': [0] * len(product_ids),
            'price': [0] * len(product_ids),
            'quantity': [0] * len(product_ids),
            'proceeds': [0] * len(product_ids),
            'orders': [0] * len(product_ids)
        }
        
        # Заполняем данные
        for i, product_id in enumerate(product_ids):
            # Заполняем метрики
            if product_id in metrics_data:
                for feature in ['delivery_efficiency_wh_avg_pos', 'discount', 'product_rating', 
                              'seller_rating', 'price', 'quantity', 'proceeds', 'orders']:
                    final_data[feature][i] = metrics_data[product_id].get(feature, 0)
            
            # Заполняем позиции
            for city, df in city_data.items():
                city_pos = df[df['product_id'] == product_id]['position'].values
                if len(city_pos) > 0:
                    final_data[CITY_MAPPING[city]][i] = city_pos[0]
        
        # Create DataFrame
        final_df = pd.DataFrame(final_data)
        
        # Save merged file
        output_path = os.path.join(data_folder, f'{date_str}_merged.csv')
        print(f"Saving merged file to: {output_path}")  # Debug log
        
        final_df.to_csv(output_path, index=False)
        print("Merge completed successfully")  # Debug log
        
        return final_df
        
    except Exception as e:
        print(f"Error in merge_city_data: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        raise  # Re-raise the exception to be caught by the caller

if __name__ == "__main__":
    merge_city_data('data')
