# Проект Foodgram
## CI и CD проекта foodgram_project
![status workflow](https://github.com/AnnPovor/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Внешний IP
```python
http://51.250.66.186/
```

## Описание
### Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Установка проекта

### 1. Склонировать репозиторий на локальную машину:

```python
git clone git@github.com:AnnPovor/foodgram-project-react.git
```

## 2. Создать и активировать виртуальное окружение:
###
```python
python -m venv venv
```
```python
source venv/Scripts/activate
```

## 3. Создать файл .env в папке infra/:
###
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
## 4. Установить зависимости из папки backend/:
###
```python
cd backend/
pip install -r requirements.txt
```
## 5. Выполнить миграции
###
```python
python manage.py migrate
```
## 6. Запустить проект:
###
```python 
python manage.py runserver
```

## Запуск проекта в Docker контейнере

### 1. Установите Docker.
### Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/.
При необходимости добавьте/измените адреса проекта в файле nginx.conf

### 2. Запустите docker compose:
```python
docker-compose up -d --build
```
### 3. Сделайте миграции:
```python
docker-compose exec backend python manage.py migrate
```
### 4. Создайте суперюзера:
```python
docker-compose exec backend python manage.py createsuperuser
```

### 5. Соберите статику:
```python
docker-compose exec backend python manage.py collectstatic --noinput
```
### Вход в админку:
email: admin@mail.ru
password: 020519