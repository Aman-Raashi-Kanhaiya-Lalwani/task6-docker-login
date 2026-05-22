from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="userdb"
)

cursor = db.cursor()

# Create tables automatically
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logins(
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT
)
""")

@app.route('/')
def home():
    return redirect('/login')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        try:
            sql = "INSERT INTO users(fullname, email, password) VALUES(%s,%s,%s)"
            val = (fullname, email, password)

            cursor.execute(sql, val)
            db.commit()

            return redirect('/login')

        except:
            return "User already exists!"

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        val = (email, password)

        cursor.execute(sql, val)

        user = cursor.fetchone()

        if user:

            user_id = user[0]

            cursor.execute(
                "INSERT INTO logins(user_id) VALUES(%s)",
                (user_id,)
            )

            db.commit()

            return redirect('/welcome')

        else:
            return redirect('/register')

    return render_template('login.html')

# Welcome Page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)