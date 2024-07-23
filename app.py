from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use sessions

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']

        users = load_users()

        if username in users:
            error = 'Username already exists. Please choose another one.'
            return render_template('signup.html', error=error)

        users[username] = {
            'password': encrypt_password(password),
            'email': email,
            'age': age
        }

        save_users(users)
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username not in users:
            error = 'User not found. Please sign up.'
            return render_template('login.html', error=error)

        encrypted_password = encrypt_password(password)
        if users[username]['password'] != encrypted_password:
            error = 'Incorrect password. Please try again.'
            return render_template('login.html', error=error)

        session['username'] = username  # Store username in session
        return redirect(url_for('dashboard', username=username))

    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    users = load_users()
    user = users.get(username)
    if not user:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=username, user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
