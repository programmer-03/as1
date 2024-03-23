from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Create MySQL connection
conn = mysql.connector.connect(host='localhost', user='root', password='Aryan2634', database='UserAuthentication')
cursor = conn.cursor()

# Route for home page
@app.route('/')
def index():
    return render_template('home.html')

# Route for login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for login authentication
@app.route('/login/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[5], password):  # Assuming the password is in the 6th column
                session['user_id'] = user[0]  # Set the user_id session variable
                return redirect(url_for('postlogin'))
            else:
                return 'Login failed'
        except Exception as e:
            return f'Login failed: {str(e)}'

# Route for registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Route for registration process
@app.route('/register/process', methods=['POST'])
def register_process():
    if request.method == 'POST':
        try:
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            contact = request.form['contactNo']
            email = request.form['email']
            password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

            cursor.execute("INSERT INTO users (first_name, last_name, contact, email, password) VALUES (%s, %s, %s, %s, %s)",
                           (first_name, last_name, contact, email, password))
            conn.commit()

            return redirect(url_for('index'))  # Redirect to home page after successful registration
        except Exception as e:
            return f'Registration failed: {str(e)}'

# Route for post-login page after successful login
@app.route('/postlogin')
def postlogin():
    return render_template('postlogin.html')

# Route for regform page after successful login
@app.route('/regform')
def regform():
    return render_template('regform.html')

# Route for uploading after successful login
@app.route('/upload')
def upload():
    return redirect(url_for('regform'))  # Redirect to registration form after successful login


if __name__ == '__main__':
    app.run(debug=True)
