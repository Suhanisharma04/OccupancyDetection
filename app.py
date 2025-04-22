from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.before_request
def clear_session():
    if 'user' not in session and request.endpoint not in ['login']:
        session.clear()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if validate_user(email, password):
            session['user'] = email
            return redirect(url_for('index'))

        flash("Invalid email or password", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    session.clear()  # Clear session completely
    return redirect(url_for('login'))  # Redirect to login

# Function to check user credentials
def validate_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        return True
    return False

@app.route('/occupancy')
def occupancy():
    if 'user' not in session:
        return redirect(url_for('login'))
    current_status = "Occupied"
    people_count = 3

    return render_template('occupancy.html',
                           status=current_status, count=people_count)

@app.route('/temperature')
def temperature():
    if 'user' not in session:
        return redirect(url_for('login'))

    current_temp = 23.7

    return render_template('temperature.html',
                           temperature=current_temp)

def get_values():
    return
    
if __name__ == "__main__":
    app.run(debug=True)


