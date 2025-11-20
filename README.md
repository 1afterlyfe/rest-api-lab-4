
# Лабораторна робота №4  
## Розробка REST API. Автентифікація. Тестування за допомогою Postman Flow  
**Студент:** Гуренко Роман Юрійович  
**Група:** ІО-35  
**Предмет:** Back-end розробка / Web API  

---

## Мета роботи
1. Створити REST API з підтримкою CRUD-операцій.  
2. Реалізувати реєстрацію та автентифікацію користувачів через JWT.  
3. Налаштувати захист ендпоінтів за допомогою `@jwt_required`.  
4. Використати **Postman Flow** для автоматичного тестування всіх запитів.  

---

## Структура проєкту

```
rest-api-lab-3/
│── app.py / wsgi.py
│── extensions.py
│── models.py
│── schemas.py
│── resources/
│     ├── users.py
│     ├── categories.py
│     ├── records.py
│── migrations/
│── instance/
│── .gitignore
│── requirements.txt
│── README.md
```

---

## Використані технології

| Технологія | Призначення |
|-----------|-------------|
| **Flask** | Web-сервер REST API |
| **Flask-SQLAlchemy** | ORM для роботи з БД |
| **Flask-Migrate** | Міграції |
| **Flask-JWT-Extended** | JWT |
| **Passlib (pbkdf2_sha256)** | Хешування паролів |
| **SQLite** | Локальна БД |
| **Postman + Postman Flow** | Тестування API |

---

## Автентифікація (JWT)

### Реєстрація  
`POST /users`  
Тіло:
```json
{
  "username": "roman",
  "password": "qwerty123"
}
```

### Логін  
`POST /login`  
Повертає:
```json
{
  "access_token": "eyJhbGciOi..."
}
```

### Захищені маршрути
Потребують `"Authorization: Bearer <token>"`:

- `GET /users`
- `GET /categories`
- `GET /records`
- `POST /records`
- `POST /categories`

---

## CRUD-операції

### Користувачі
- Реєстрація  
- Логін  
- Отримання списку користувачів (JWT)

### Категорії
- Створення категорії  
- Перегляд списку  
- Видалення  

### Фінансові записи
- Створення запису  
- Отримання списку  
- Видалення  

---

## Postman Flow (автоматизація)

Реалізовано pipeline:

1. **Start**
2. **POST /login**  
   → Зберігання глобальної змінної `Token`
3. **GET /users**
4. **GET /categories**
5. **GET /records`

Flow обробляє:
- `token_expired`
- `invalid_token`

Використовуються глобальні змінні:
- `base_url`
- `Token`

---

## Запуск проєкту

### 1. Віртуальне середовище
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Міграції БД
```bash
flask db upgrade
```

### 4. Запуск сервера
```bash
flask run
```

Сервер буде доступний на:  
http://127.0.0.1:5000

---

## ✔ Висновки

У ході виконання лабораторної роботи було:
- створено REST API з авторизацією через JWT;  
- реалізовано CRUD-операції для користувачів, категорій та записів;  
- налаштовано автоматизоване тестування через Postman Flow;  
- відпрацьовано роботу з базою даних, міграціями та токенами.

Результатом є повністю робочий API з автоматизованою схемою тестування.
