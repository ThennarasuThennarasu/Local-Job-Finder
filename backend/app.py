from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ---------- Database Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",      # your MySQL host
        user="root",           # your MySQL username
        password="Thennu67@#",  # 🔹 change this
        database="local_job_finder"
    )

# ---------- Signup ----------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "Email already registered!"}), 400

    # Insert new user
    cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", (email, password, role))
    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful!"})

# ---------- Login ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful!", "role": user["role"]})
    else:
        return jsonify({"message": "Invalid email or password!"}), 401


if __name__ == "__main__":
    app.run(debug=True)






from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Thennu67@#",
        database="local_job_finder"
    )

# ---------- Worker sends location ----------
@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.get_json()
    worker_id = data.get("worker_id")
    lat = data.get("latitude")
    lon = data.get("longitude")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO worker_locations (worker_id, latitude, longitude)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE latitude=%s, longitude=%s
    """, (worker_id, lat, lon, lat, lon))
    conn.commit()
    conn.close()

    return jsonify({"message": "Location updated"})

# ---------- Employer fetches worker location ----------
@app.route("/get_worker_location/<int:worker_id>", methods=["GET"])
def get_worker_location(worker_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM worker_locations WHERE worker_id = %s", (worker_id,))
    location = cursor.fetchone()
    conn.close()

    if location:
        return jsonify(location)
    else:
        return jsonify({"message": "No location found"}), 404

if __name__ == "__main__":
    app.run(debug=True)







@app.route('/api/submitRating', methods=['POST'])
def submit_rating():
    data = request.get_json()
    job_id = data['jobId']
    worker_id = data['workerId']
    rating = data['rating']
    feedback = data['feedback']
    employer_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ratings (job_id, employer_id, worker_id, rating, feedback) VALUES (%s, %s, %s, %s, %s)",
                (job_id, employer_id, worker_id, rating, feedback))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Rating saved successfully!'})
