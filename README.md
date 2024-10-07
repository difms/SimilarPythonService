# Flask App with PostgreSQL

## Описание
Это Flask приложение для обработки текстовых запросов с помощью TF-IDF и поиска похожих маршрутов.

## Требования
- Docker и Docker Compose или локально

## Запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/difms/SimilarPythonService.git
   cd SimilarPythonService


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

## Для запуска Flask-приложения через pm2, вам нужно сделать следующее:

npm install pm2 -g

Для более производительного запуска Flask-приложений, вы можете использовать gunicorn в связке с pm2.

Установите gunicorn:
pm2 start "gunicorn --bind 0.0.0.0:5000 app:app" --name flask-app

Здесь:

gunicorn — это WSGI-сервер для обработки запросов.
--bind 0.0.0.0:5000 — привязка сервера к вашему хосту и порту (5000).
app:app — указание, что нужно запустить Flask-приложение из файла app.py, где app — это имя экземпляра приложения Flask.
--name flask-app — это имя процесса в pm2, которое поможет вам его идентифицировать.

Работа: pm2 list / pm2 stop flask-app / pm2 restart flask-app
Сохранить процесс для автозапуска: pm2 save
Добавить автозапуск при перезагрузке сервера: pm2 startup / pm2 save
Логи: pm2 logs flask-app

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
