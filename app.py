from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
latest_temp = None
people_in_room = None
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

@app.context_processor
def inject_sensor_data():
    global latest_temp, people_in_room
    return dict(
        temperature=latest_temp if latest_temp else "No data yet",
        occupancy="Occupied" if isinstance(people_in_room, int) and people_in_room > 0 else "Vacant",
        occupancy_count=people_in_room if people_in_room is not None else "No data yet"
    )

@app.route('/update_sensor_data', methods=['POST'])
def update_sensor_data():
    global latest_temp, people_in_room

    if not request.is_json:
        return {"error": "Expected JSON"}, 400

    data = request.get_json()
    latest_temp = data.get("temperature")
    people_in_room = data.get("people_count")

    print(f"Data received: Temp = {latest_temp}, People = {people_in_room}")
    return {"success": True}, 200


@app.route('/temperature')
def temperature_page():
    return render_template('temperature.html')

@app.route('/occupancy')
def occupancy_page():
    return render_template('occupancy.html')


def get_values():
    return
    
if __name__ == "__main__":
    app.run(debug=True)


