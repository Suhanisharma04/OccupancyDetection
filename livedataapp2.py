from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global variables for shared sensor data
latest_temp = None
people_in_room = None

@app.before_request
def clear_session():
    if 'user' not in session and request.endpoint not in ['login', 'update_sensor_data']:
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
    session.pop('user', None)
    session.clear()
    return redirect(url_for('login'))

# Validate user login
def validate_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user and check_password_hash(user[0], password)

# ✅ New: Receive sensor data from Raspberry Pi
@app.route('/update_sensor_data', methods=['POST'])
def update_sensor_data():
    global latest_temp, people_in_room

    if not request.is_json:
        return {"error": "Invalid format, expected JSON"}, 400

    data = request.get_json()
    latest_temp = data.get('temperature')
    people_in_room = data.get('people_count')

    print(f"[Data Received] Temp: {latest_temp}°C | People: {people_in_room}")
    return {"success": True}, 200

@app.route('/occupancy')
def occupancy():
    if 'user' not in session:
        return redirect(url_for('login'))

    count = people_in_room if people_in_room is not None else 'No data yet'
    status = "Occupied" if isinstance(people_in_room, int) and people_in_room > 0 else "Vacant"

    return render_template('occupancy.html', status=status, count=count)

@app.route('/temperature')
def temperature():
    if 'user' not in session:
        return redirect(url_for('login'))

    temp = latest_temp if latest_temp is not None else 'No data yet'
    return render_template('temperature.html', temperature=temp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')