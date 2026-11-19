from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Данные подключения к MySQL — поменяй под свой сервер
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "flask_auth",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


class Database:
    """Подключение к MySQL, курсор и запросы к таблице users."""

    def __init__(self):
        self.connection = pymysql.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def get_user(self, username):
        sql = "SELECT id, user_name, user_password FROM users WHERE user_name = %s"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone()  # словарь с полями users или None

    def close(self):
        self.cursor.close()
        self.connection.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        db = None

        try:
            db = Database()
            user = db.get_user(username)

            if user and user['user_password'] == password:
                return redirect(url_for('login_page'))

            error = "Неверное имя пользователя или пароль"
        except pymysql.MySQLError:
            error = "Нет подключения к базе данных"
        except Exception:
            error = "Ошибка при обработке данных"
        finally:
            if db is not None:
                db.close()

    return render_template('index.html', error=error)


@app.route('/login_page')
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
