# Flask + MySQL: авторизация

Практика 9.11.2026. Flask-приложение с формой входа, проверкой логина и пароля
по таблице `users` в MySQL через `pymysql`.

## Задание (4 пункта)

1. **Схема и таблица.** В MySQL создать БД `flask_auth` и таблицу `users`
   с полями `id`, `user_name`, `user_password`.
2. **Класс `Database`.** Подключение через `pymysql.connect(...)`, курсор,
   закрытие соединения.
3. **Метод `get_user(username)`.** Возвращает запись из `users` или `None`.
4. **Проверка в роуте `/login`.** Получить данные через `Database`, сверить
   пароль, обработать ошибки, сделать редирект.

## Файлы

- `main.py` — Flask-приложение и класс `Database`
- `schema.sql` — база `flask_auth`, таблица `users`, тестовая запись
- `templates/index.html` — форма входа
- `templates/login.html` — страница «Вы успешно вошли»
- `requirements.txt` — зависимости (`flask`, `pymysql`)

## Запуск

```bash
# 1. Виртуальное окружение и зависимости
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. База и таблица (пароль root ввести при запросе)
mysql -u root -p < schema.sql

# 3. В main.py в DB_CONFIG указать свои user / password / database

# 4. Запуск
python main.py
```

Открыть <http://127.0.0.1:5000/login> и войти:

- логин: `Vladimir Putin`
- пароль: `123456789`

## Как это работает

- `Database.__init__` открывает соединение и создаёт курсор,
  `Database.close()` закрывает и курсор, и соединение.
- `get_user()` выполняет параметризованный запрос
  `SELECT ... WHERE user_name = %s`, поэтому SQL-инъекция не проходит;
  `fetchone()` возвращает словарь с полями пользователя или `None`.
- Роут `/login` создаёт `Database`, сравнивает пароль и при совпадении делает
  `redirect` на `/login_page`; при ошибке показывает сообщение на форме.
  Соединение закрывается в `finally` даже после редиректа.
- Ошибка подключения (`pymysql.MySQLError`) показывается как
  «Нет подключения к базе данных», приложение не падает.

## Примечания

- Пароль хранится в открытом виде — так требует учебное задание. В реальном
  проекте храните хеш (`werkzeug.security.generate_password_hash`) и сравнивайте
  через `check_password_hash`.
- В названии папки «:» заменено на « - », иначе репозиторий не склонируется
  на Windows.
