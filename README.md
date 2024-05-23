![example workflow](https://github.com/ValentinGorovenko/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект Foodgram
Foodgram - «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка

Склонируйте репозитрий на свой компьютер.

Заполните шаблон infra/.env.template

Выполните копирование файла командой:
cp infra/.env.template infra/.env 

Из папки infra/ соберите образ при помощи docker compose
docker compose up -d --build

Примените миграции
docker compose exec backend python manage.py migrate

Соберите статику
docker compose exec backend python manage.py collectstatic --no-input

Для доступа к админке не забудьте создать суперюзера
docker compose exec backend python manage.py createsuperuser

Для добавления ингредиентов и тегов в базу данных, выполните команду:
docker compose exec backend python manage.py load_ingredients ingredients.csv
docker compose exec backend python manage.py load_tags

## Деплой на удаленный сервер
Для запуска проекта на удаленном сервере необходимо:

скопировать на сервер папку infra выполнив команду:

scp -r infra user@server-ip:

создать переменные окружения в разделе secrets настроек текущего репозитория:

DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь зарегистрированный на сервере
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
TELEGRAM_TO # ID телеграм-аккаунта
TELEGRAM_TOKEN # Токен бота
 
 Примените миграции
docker compose exec backend python manage.py migrate

Соберите статику
docker compose exec backend python manage.py collectstatic --no-input

Для доступа к админке не забудьте создать суперюзера
docker compose exec backend python manage.py createsuperuser 

Для добавления ингредиентов и тегов в базу данных, выполните команду:
docker compose exec backend python manage.py load_ingredients ingredients.csv
docker compose exec backend python manage.py load_tags

 ### После каждого обновления репозитория (git push) будет происходить:

Проверка кода на соответствие стандарту PEP8.
Сборка и доставка докер-образов на Docker Hub.
Автоматический деплой.
Отправка уведомления в Telegram.
