# Flask App with PostgreSQL

## Описание
Это Flask приложение для обработки текстовых запросов с помощью TF-IDF и поиска похожих маршрутов.

## Требования
- Docker и Docker Compose или локально

## Запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your_username/your_repo.git
   cd your_repo


Убедитесь, что у вас установлен Python 3. Установите virtualenv, если он не установлен

pip install virtualenv

Создайте и активируйте виртуальное окружение:
virtualenv myservice
source myservice/bin/activate

Установите необходимые зависимости (Flask, numpy, scikit-learn, psycopg2-binary):
pip install -r requirements.txt
или
pip install Flask numpy scikit-learn psycopg2-binary python-dotenv

Установите PostgreSQL, если он не установлен:
sudo apt-get install postgresql postgresql-contrib
Или любую другую БД на Ваш вкус

## По БД:
sudo -u postgres psql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;

Создайте таблицу для хранения векторов:
CREATE TABLE request_vectors (
  id SERIAL PRIMARY KEY,
  route_id INTEGER NOT NULL,
  query_vector FLOAT8[] NOT NULL
);

## Докер
docker-compose up

Сервис будет доступен по http://localhost:5000

## env

THRESHOLD_VALUE = необходимое значение похожести в %

## Laravel

# Сохранение нового вектора для маршрута
public function saveRouteVector($query, $routeId)
{
    $url = 'http://127.0.0.1:5000/save_vector';
    $response = Http::post($url, [
        'query' => $query,
        'route_id' => $routeId,
    ]);

    return $response->successful();
}

# Отправка запроса для поиска похожего маршрута
public function checkSimilarRoute($query)
{
    $url = 'http://127.0.0.1:5000/process_query';
    $response = Http::post($url, [
        'query' => $query,
    ]);

    if ($response->successful()) {
        $routeId = $response->json()['route_id'];
        return $routeId; // возвращаем найденный маршрут
    } else {
        return null; // похожий маршрут не найден
    }
}
