import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Загрузка данных
df = pd.read_csv("brand_new.csv")

# Определяем признаки и города
features = [
    "delivery_efficiency_wh_avg_pos", "discount", "product_rating", "seller_rating",
    "proceeds", "orders", "price", "quantity"
]
city_columns = [col for col in df.columns if col.startswith("position_")]

# Создаём словарь для хранения моделей
city_models = {}

# Обучаем модель для каждого города
for city in city_columns:
    # Убираем пропуски
    city_data = df[[city] + features].dropna()

    # Делим данные
    X = city_data[features]
    y = city_data[city]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Pipeline: заполнение пропусков → масштабирование → модель
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler()),
        ("gbr", GradientBoostingRegressor(random_state=42))
    ])

    # Обучение
    model.fit(X_train, y_train)

    # Сохраняем модель
    city_models[city] = model

# Локализация названий городов
city_names = {
    "position_msk": "Москва",
    "position_spb": "Санкт-Петербург",
    "position_nvsb": "Новосибирск",
    "position_hab": "Хабаровск",
    "position_ekb": "Екатеринбург",
    "position_kaz": "Казань",
    "position_kras": "Краснодар"
}

def get_recommendations(product_id, verbose=True):
    product = df[df["product_id"] == product_id]
    if product.empty:
        return f"❌ product_id {product_id} не найден в датасете"

    recommendations = []
    X = product[features].copy()

    for city in city_columns:
        if pd.isna(product[city].values[0]):
            recommendations.append(f"⚠️ В городе {city_names[city]} нет позиции — не могу дать рекомендацию.")
            continue

        model = city_models[city]
        base_pred = model.predict(X)[0]
        city_recs = []

        # 🔽 Приоритетные параметры
        # 1. Доставка (уменьшаем на 10%)
        if not pd.isna(X["delivery_efficiency_wh_avg_pos"].values[0]):
            new_X = X.copy()
            new_X["delivery_efficiency_wh_avg_pos"] *= 0.9
            new_pred = model.predict(new_X)[0]
            delta = base_pred - new_pred
            if delta > 3:
                city_recs.append(f"📦 Улучшите доставку на 10% → ~{int(delta)} позиций вверх")

        # 2. Скидка (увеличиваем на 10%)
        if not pd.isna(X["discount"].values[0]):
            new_X = X.copy()
            new_X["discount"] *= 1.1
            new_pred = model.predict(new_X)[0]
            delta = base_pred - new_pred
            if delta > 3:
                city_recs.append(f"💸 Увеличьте скидку на 10% → ~{int(delta)} позиций вверх")

        # 3. Рейтинги (на +0.2)
        for rating_col in ["seller_rating", "product_rating"]:
            if not pd.isna(X[rating_col].values[0]) and X[rating_col].values[0] <= 4.8:
                new_X = X.copy()
                new_X[rating_col] += 0.2
                new_pred = model.predict(new_X)[0]
                delta = base_pred - new_pred
                if delta > 3:
                    label = "рейтинг продавца" if rating_col == "seller_rating" else "рейтинг товара"
                    city_recs.append(f"⭐ Повышение {label} на 0.2 → ~{int(delta)} позиций вверх")

        # ➕ Дополнительные параметры (увеличиваем на 10%)
        other_params = ["proceeds", "orders", "price", "quantity"]
        for param in other_params:
            if not pd.isna(X[param].values[0]):
                new_X = X.copy()
                new_X[param] *= 1.1
                new_pred = model.predict(new_X)[0]
                delta = base_pred - new_pred
                if delta > 3:
                    name_map = {
                        "proceeds": "выручка",
                        "orders": "число заказов",
                        "price": "цену",
                        "quantity": "остатки"
                    }
                    city_recs.append(f"📊 Увеличьте {name_map[param]} на 10% → ~{int(delta)} позиций вверх")

        if city_recs:
            city_block = f"\n📍 {city_names[city]}:\n" + "\n".join(" - " + rec for rec in city_recs)
            recommendations.append(city_block)

    if verbose:
        print(f"Рекомендации для product_id {product_id}:\n" + "\n".join(recommendations))
    return recommendations


get_recommendations(210586552)
