# REST API  
**Flask + SQLAlchemy + PostgreSQL (через Docker)**  

## Визначення варіанту до 3 ЛР

Група: ІО-35.

Варіант: 5 mod 3 = 2 (Користувацькі категорії витрат)

## Опис проєкту  
Цей проєкт реалізує REST API для керування **користувачами**, **категоріями витрат** і **фінансовими записами**.  
Він побудований на Flask з використанням ORM SQLAlchemy, Marshmallow для валідації даних і Flask-Migrate для роботи з міграціями бази даних.  

База даних PostgreSQL запускається в контейнері Docker.  
API підтримує **глобальні** та **індивідуальні** категорії витрат для кожного користувача.

## Структура проєкту
```
rest-api-lab-2/
│
├── docker-compose.yaml         # Сервіс PostgreSQL
├── config.py                   # Конфігурація застосунку
├── extensions.py                # Ініціалізація ORM і Migrate
├── models.py                   # ORM-моделі User, Category, Record
├── schemas.py                  # Marshmallow-схеми
├── wsgi.py                     # Точка входу Flask
├── requirements.txt            # Залежності
│
├── resources/                  # REST-ресурси (Blueprints)
│   ├── users.py
│   ├── categories.py
│   └── records.py
│
├── migrations/                 # Alembic-міграції
└── README.md                   # Цей файл
```

---

## Запуск проєкту

### Створити та активувати віртуальне середовище
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### Встановити залежності
```bash
pip install -r requirements.txt
```

### Запустити базу даних у Docker
```bash
docker-compose up -d db
```

(Контейнер створить PostgreSQL на порту **5433**)

---

## Налаштування підключення до БД
У файлі `config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://postgres:postgres@localhost:5433/finance_db"
```

---

## Міграції бази даних

Створити структуру таблиць:
```bash
flask --app wsgi db migrate -m "initial tables"
```

Застосувати міграції:
```bash
flask --app wsgi db upgrade
```

Перевірка у Docker:
```bash
docker exec -it rest-api-lab-2-db-1 psql -U postgres -d finance_db -c "\dt"
```

---

## Запуск сервера

```bash
flask --app wsgi run
```

Сервер за замовчуванням працює на:
```
http://127.0.0.1:5000/
```

---

## Основні ендпоінти

### Користувачі
| Метод | Endpoint | Опис |
|--------|-----------|------|
| `POST` | `/users` | створення нового користувача |
| `GET` | `/users/<id>` | отримати дані користувача |
| `DELETE` | `/users/<id>` | видалити користувача |

---

### Категорії
| Метод | Endpoint | Опис |
|--------|-----------|------|
| `GET` | `/categories` | список усіх категорій (глобальних + користувацьких) |
| `POST` | `/categories` | створення нової категорії |
| `DELETE` | `/categories/<id>` | видалення категорії |

#### Приклад запиту:
```json
POST /categories
{
  "name": "Food",
  "is_global": true
}
```

---

### Записи (Records)
| Метод | Endpoint | Опис |
|--------|-----------|------|
| `GET` | `/records` | список фінансових записів |
| `POST` | `/records` | створити запис витрат |
| `DELETE` | `/records/<id>` | видалити запис |

#### Приклад створення запису:
```json
POST /records
{
  "amount": 250.0,
  "description": "Groceries",
  "category_id": 1,
  "user_id": 1
}
```

---

## Приклади тестування через Postman
- **Headers:**  
  `Content-Type: application/json`  
- **Тіло запиту:** raw → JSON
- Якщо отримаєш `"Missing data for required field"`, перевір, чи в Postman вибрано `JSON`, а не `Text`.

---

## Команди для зручності
| Команда | Призначення |
|----------|--------------|
| `docker ps` | перевірити стан контейнера |
| `docker logs rest-api-lab-2-db-1` | подивитись логи PostgreSQL |
| `flask db current` | перевірити версію міграцій |
| `flask db downgrade` | відкотити останню міграцію |

---

## Теги
Використовується семантичне версіонування:
```
v2.0.0 – Лабораторна робота №2
```

---

##  Автор
**Гуренко Роман ІО-35**
