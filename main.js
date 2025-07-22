// src/App.js
import React, { useState } from "react";

function App() {
  const [article, setArticle] = useState("");
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRecommendations(null);
    try {
      // Заменить на адрес твоего бэкенда
      const res = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ article }),
      });
      const data = await res.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      setRecommendations(["Ошибка при получении рекомендаций"]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", padding: 20 }}>
      <h2>Wildberries: рекомендации для продвижения</h2>
      <form onSubmit={handleSubmit}>
        <input
          value={article}
          onChange={(e) => setArticle(e.target.value)}
          type="text"
          required
          placeholder="Введите артикул товара"
          autoFocus
          style={{ padding: 10, width: "60%" }}
        />
        <button
          type="submit"
          disabled={!article || loading}
          style={{ marginLeft: 10 }}
        >
          Получить рекомендации
        </button>
      </form>
      {loading && <div style={{ marginTop: 30 }}>Загрузка рекомендаций...</div>}
      {recommendations && (
        <div style={{ marginTop: 30 }}>
          <h3>Рекомендации:</h3>
          <ul>
            {recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
