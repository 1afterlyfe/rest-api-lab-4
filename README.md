# REST API для Обліку Витрат (Flask)

Це базовий REST API застосунок для обліку витрат, створений на Flask. Дані зберігаються в пам'яті застосунку.

**Задеплоєний проект:** `https://rest-api-lab-2.onrender.com/healthcheck`

---

## Встановлення та запуск локально

1.  **Клонуйте репозиторій:**
    ```bash
    git clone https://github.com/1afterlyfe/rest-api-lab-2
    cd rest-api-lab-2
    ```

2.  **Створіть та активуйте віртуальне середовище:**
    ```bash
    # Для macOS/Linux
    python -m venv venv
    source venv/bin/activate

    # Для Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Встановіть залежності:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Запустіть застосунок:**
    ```bash
    python app.py
    ```

Застосунок буде доступний за адресою `http://127.0.0.1:5000`.

---

## Ендпоінти API

### Users

* `POST /user` - Створює нового користувача.
    * **Body (JSON):** `{"name": "Your Name"}`
* `GET /users` - Отримує список всіх користувачів.
* `GET /user/<user_id>` - Отримує одного користувача по ID.
* `DELETE /user/<user_id>` - Видаляє користувача по ID.

### Categories

* `POST /category` - Створює нову категорію.
    * **Body (JSON):** `{"name": "Groceries"}`
* `GET /category` - Отримує список всіх категорій.
* `GET /category/<category_id>` - Отримує одну категорію по ID.
* `DELETE /category/<category_id>` - Видаляє категорію по ID.

### Records

* `POST /record` - Створює новий запис про витрати.
    * **Body (JSON):** `{"user_id": 1, "category_id": 1, "amount": 99.99}`
* `GET /record/<record_id>` - Отримує один запис по ID.
* `DELETE /record/<record_id>` - Видаляє запис по ID.
* `GET /record` - Отримує список записів з фільтрацією.
    * **Обов'язково** потрібен хоча б один параметр: `user_id` або `category_id`.
    * **Приклад:** `GET /record?user_id=1&category_id=2`