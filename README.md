#Foodgram


```
1. В директории infra следует выполнить команды:
```
docker compose up -d
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --no-input
```
2. Для создания суперпользователя, выполните команду:
```
docker compose exec backend python manage.py createsuperuser
```

3. Для добавления ингредиентов и тегов в базу данных, выполните команду:
```
docker compose exec backend python manage.py load_ingredients ingredients.csv
docker compose exec backend python manage.py load_tags
```
После выполнения этих действий проект будет запущен в трех контейнерах (backend, db, nginx) и доступен по адресам:

- Главная страница: http://<ip-адрес>/recipes/
- API проекта: http://<ip-адрес>/api/
- Admin-зона: http://<ip-адрес>/admin/

4. Проект запущен и готов к регистрации пользователей и добавлению рецептов.