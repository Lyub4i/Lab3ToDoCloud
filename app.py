from flask import Flask, render_template, json, request, redirect, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin1234'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'database-1.cvg2a0y6kojy.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

app.secret_key = 'why would I tell you my secret key?'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signup')
def showSignUp():
    return render_template('signup.html')


@app.route('/signin')
def showSignin():
    return render_template('signin.html')


@app.route('/api/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Підключення до бази даних
        cursor = mysql.connection.cursor()

        # Викликаємо збережену процедуру для перевірки користувача
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            # Використовуємо функцію перевірки пароля з хешуванням
            if check_password_hash(data[0][3], _password):
                session['user'] = data[0][0]
                return redirect('/userhome')
            else:
                return render_template('error.html', error='Неправильна електронна адреса або пароль')
        else:
            return render_template('error.html', error='Неправильні дані для входу')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()


@app.route('/api/signup', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Перевірка введених значень
        if _name and _email and _password:

            # Створення хешованого пароля
            _hashed_password = generate_password_hash(_password)

            # Підключення до бази даних
            cursor = mysql.connection.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) == 0:
                mysql.connection.commit()
                return json.dumps({'message': 'Користувач успішно створений!'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Введіть необхідні поля</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()


@app.route('/userhome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html', error='Несанкціонований доступ')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
