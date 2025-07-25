from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from get_article import get_article_metrics
import model

app = Flask(__name__)
CORS(app)

def update_last_row_in_dataset(article_metrics):
    """Update the last row in brand_new.csv with new metrics"""
    try:
        df = pd.read_csv('data/brand_new.csv')
        # Update the last row with new metrics
        for key, value in article_metrics.items():
            if key in df.columns:
                df.iloc[-1, df.columns.get_loc(key)] = value
        
        # Save back to CSV
        df.to_csv('data/brand_new.csv', index=False)
        return True
    except Exception as e:
        print(f"Error updating dataset: {e}")
        return False

@app.route('/api/recommendations/<int:articul>')
def get_product_recommendations(articul):
    try:
        # Get metrics for the article
        metrics = get_article_metrics(articul)
        if metrics:
            # Update the last row in dataset
            update_last_row_in_dataset(metrics)
            # Get recommendations using existing model
            recommendations = model.get_recommendations(articul)
            return jsonify(recommendations)
        return jsonify(["❌ Не удалось получить данные о товаре"]), 404
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify(["Ошибка при получении рекомендаций"]), 500

@app.route('/api/product/<int:articul>')
def get_product_info(articul):
    try:
        metrics = get_article_metrics(articul)
        if metrics:
            return jsonify(metrics)
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
