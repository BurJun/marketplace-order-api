# Order Service (FastAPI + PostgreSQL)

Небольшой сервис для работы с заказами маркетплейса.  

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker, Docker Compose
- Uvicorn

## Функциональность

### POST `/orders/items`

Добавляет товар в существующий заказ.

**Request body:**

```json
{
  "order_id": 1,
  "product_id": 1,
  "quantity": 2
}
```
## Логика работы эндпоинта:
•	Проверяется существование заказа (CustomerOrder) и товара (Product).
•	Проверяется, что на складе достаточно товара (product.quantity).
•	Если позиция с этим product_id уже есть в заказе (OrderItem), её количество увеличивается.
•	Если позиции нет — создаётся новая строка в order_item.
•	Остаток товара на складе уменьшается на переданное количество.
•	В ответе возвращается итоговое количество этого товара в заказе.
## Возможные ответы:
•	200 OK — товар успешно добавлен/обновлён.
•	404 Not Found — заказ или товар не найдены.
•	409 Conflict — недостаточно товара на складе.
•	500 Internal Server Error — внутренняя ошибка сервера.

## Установка и запуск без Docker
1. Клонировать репозиторий

2. Создать виртуальное окружение и установить зависимости

3. Настроить базу данных
Поднять PostgreSQL, создать базу или изменить строку подключения в db.py:

```python
DB_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/test"
```
4. Создать таблицы и добавить тестовые данные

```bash
python init_db.py
```

5. Запустить приложение

```bash
uvicorn main:app --reload
```

## Запуск через Docker Compose
1. Собрать и запустить контейнеры

```bash
docker compose up --build
```

2. Можно выполнить init_db.py внутри контейнера приложения:

```bash
docker exec -it sales_app python init_db.py
```

