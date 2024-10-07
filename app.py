from flask import Flask, request, jsonify
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

app = Flask(__name__)

# Подключение к базе данных PostgreSQL


def connect_db():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )

# Функция для преобразования запроса в вектор


def generate_vector(text):
    # например, используем TF-IDF векторизацию
    vectorizer = TfidfVectorizer(max_features=768)
    vector = vectorizer.fit_transform([text]).toarray()[0]
    return vector

# Функция для поиска ближайшего вектора в БД


def find_nearest_vector(vector, threshold=os.getenv('THRESHOLD_VALUE')):
    conn = connect_db()
    cur = conn.cursor()

    # Получаем все векторы из БД
    cur.execute("SELECT id, route_id, query_vector FROM request_vectors")
    results = cur.fetchall()

    max_similarity = 0
    nearest_route_id = None

    for row in results:
        db_vector = np.array(row[2])
        similarity = cosine_similarity([vector], [db_vector])[0][0]

        if similarity > max_similarity and similarity >= threshold:
            max_similarity = similarity
            nearest_route_id = row[1]

    cur.close()
    conn.close()

    return nearest_route_id

# Эндпоинт для генерации вектора и поиска ближайшего маршрута


@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.json
    query = data['query']

    # Генерация вектора для запроса
    vector = generate_vector(query)

    # Поиск ближайшего маршрута по вектору
    route_id = find_nearest_vector(vector)

    if route_id:
        return jsonify({'route_id': route_id}), 200
    else:
        return jsonify({'message': 'No similar route found'}), 404

# Эндпоинт для сохранения нового вектора в БД


@app.route('/save_vector', methods=['POST'])
def save_vector():
    data = request.json
    query = data['query']
    route_id = data['route_id']

    vector = generate_vector(query)

    conn = connect_db()
    cur = conn.cursor()

    # Сохранение вектора в БД
    cur.execute("INSERT INTO request_vectors (route_id, query_vector) VALUES (%s, %s)",
                (route_id, vector.tolist()))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'Vector saved successfully'}), 201


if __name__ == '__main__':
    app.run(host=os.getenv('APP_HOST'), port=os.getenv('APP_PORT'))
