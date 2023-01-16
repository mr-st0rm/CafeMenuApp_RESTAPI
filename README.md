REST API для некого кафе с такими сущностями как **Menu**, **SubMenu** и **Dish**.

API написано на FastAPI с использованием ORM **SqlAlchemy**.
**Обязательный префикс для всех запросов _/api/v1_**

### Запуск проекта:
- в _**cfg.ini**_ поменять данные от **PostgreSql** (имя, пароль и базу данных) на ваши
- запустить файл main.py
- проект запущен, хост и порт так же можно посмотреть или поменять в _**cfg.ini**_


### URI для запросов основного меню:
- GET /menus - получение всех меню
- POST /menus - создание меню
- GET /menus/{menu_id} - подробная информация о конкретном меню
- PATCH /menus/{menu_id} - обновление конкретного меню
- DELETE /menus/{menu_id} - удаление конкретного меню

### Дополнительно в ответе присутствует количество всех подменю и блюд
- submenus_count
- dishes_count

### URI для запросов подменю:
- GET /menus/{menu_id}/submenus - получение всех подменю конкретного меню
- POST /menus/{menu_id}/submenus - создание подменю
- GET /menus/{menu_id}/submenus/{submenu_id} - подробная информация о конкретном подменю
- PATCH /menus/{menu_id}/submenus/{submenu_id} - обновление конкретного подменю
- DELETE /menus/{menu_id}/submenus/{submenu_id} - удаление конкретного подменю

### Дополнительно в ответе присутствует количество всех блюд
- dishes_count

### URI для запросов блюд:
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes - получение всех блюд
- POST /menus/{menu_id}/submenus/{submenu_id}/dishes - создание блюда
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - подробная информация о конкретном блюде
- PATCH /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - обновление конкретного блюда
- DELETE /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - удаление конкретного блюда