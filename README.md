REST API для некого кафе с такими сущностями как **Menu**, **SubMenu** и **Dish**.

API написано на FastAPI с использованием ORM **SqlAlchemy**.
**Обязательный префикс для всех запросов _/api/v1_**

---

### Запуск проекта:
- устанавливаем себе на ПК Docker/Docker-Compose


- Выполняем команды одну за одной
  - `docker-compose up -d`
- После этого приложение запущено и доступно в браузере по ссылке http://127.0.0.1:8000/docs
- API - http://127.0.0.1:8000/api/v1/menus


- Для запуска тестов(app/tests)
  - `docker-compose -f docker-compose.tests.yml up -d`

Можем посмотреть результаты тестов в логах контейнера под названием `test_api` с помощью команды
- `docker logs test_api`

### Генерация записей в БД для экспорта .xlsx файла
- **POST** запрос с пустым телом на - `http://127.0.0.1:8000/api/v1/fill_db`

### URL для создания task'ов в Celery
- **POST** запрос с пустым телом на - `http://127.0.0.1:8000/api/v1/report/xlsx`
- **GET** запрос с task_id в URL запроса - `http://127.0.0.1:8000/api/v1/report/xlsx/{task_id}`
- **GET** запрос с именем файла на - `http://127.0.0.1:8000/api/v1/report/xlsx/download/f/{file_name}`

### URL для запросов основного меню:
- GET /menus - получение всех меню
- POST /menus - создание меню
- GET /menus/{menu_id} - подробная информация о конкретном меню
- PATCH /menus/{menu_id} - обновление конкретного меню
- DELETE /menus/{menu_id} - удаление конкретного меню

**Дополнительно в ответе на GET запросы присутствует количество всех подменю и блюд**
- submenus_count
- dishes_count

### URL для запросов подменю:
- GET /menus/{menu_id}/submenus - получение всех подменю конкретного меню
- POST /menus/{menu_id}/submenus - создание подменю
- GET /menus/{menu_id}/submenus/{submenu_id} - подробная информация о конкретном подменю
- PATCH /menus/{menu_id}/submenus/{submenu_id} - обновление конкретного подменю
- DELETE /menus/{menu_id}/submenus/{submenu_id} - удаление конкретного подменю

**Дополнительно в ответе на GET запросы присутствует количество всех блюд**
- dishes_count

### URL для запросов блюд:
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes - получение всех блюд
- POST /menus/{menu_id}/submenus/{submenu_id}/dishes - создание блюда
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - подробная информация о конкретном блюде
- PATCH /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - обновление конкретного блюда
- DELETE /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - удаление конкретного блюда
