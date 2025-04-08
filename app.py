import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# ANTI-PATTERN: Hardcoded database path (no configuration management)
DATABASE_PATH = "customer_data.db"

# ANTI-PATTERN: Hardcoded credentials that should be secured
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# ANTI-PATTERN: No database connection pooling or error handling
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (done every time the app starts - no migration strategy)
def init_db():
    # ANTI-PATTERN: Creating DB tables on startup instead of proper migrations
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        ssn TEXT NOT NULL,
        credit_card TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")  # ANTI-PATTERN: Using print instead of proper logging

init_db()

@app.route('/health', methods=['GET'])
def health_check():
    # ANTI-PATTERN: Simplistic health check that doesn't actually verify system health
    return jsonify({"status": "up", "timestamp": datetime.now().isoformat()})

@app.route('/customers', methods=['POST'])
def add_customer():
    # ANTI-PATTERN: No input validation
    data = request.get_json()
    
    # ANTI-PATTERN: No sanitization of sensitive data
    name = data.get('name')
    email = data.get('email')
    ssn = data.get('ssn')  # ANTI-PATTERN: Storing sensitive data like SSN in plain text
    credit_card = data.get('credit_card')  # ANTI-PATTERN: Storing credit card in plain text
    
    # ANTI-PATTERN: Ad-hoc logging that exposes sensitive data
    print(f"Adding customer: {name}, {email}, SSN: {ssn}, CC: {credit_card}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, ssn, credit_card, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, email, ssn, credit_card, datetime.now().isoformat())
    )
    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()
    
    # ANTI-PATTERN: Returning sensitive data in response
    return jsonify({
        "id": customer_id,
        "name": name,
        "email": email,
        "ssn": ssn,
        "credit_card": credit_card,
        "message": "Customer added successfully"
    }), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    # ANTI-PATTERN: No authentication for sensitive data access
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    
    # ANTI-PATTERN: Returning all sensitive data at once
    result = []
    for customer in customers:
        result.append({
            "id": customer['id'],
            "name": customer['name'],
            "email": customer['email'],
            "ssn": customer['ssn'],
            "credit_card": customer['credit_card'],
            "created_at": customer['created_at']
        })
    
    return jsonify(result)

@app.route('/admin', methods=['POST'])
def admin_login():
    # ANTI-PATTERN: Basic auth with hardcoded credentials
    data = request.get_json()
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.errorhandler(Exception)
def handle_error(e):
    # ANTI-PATTERN: Exposing error details that might contain sensitive information
    return jsonify({
        "error": str(e),
        "stack_trace": str(e.__traceback__)
    }), 500

if __name__ == '__main__':
    # ANTI-PATTERN: Running with debug=True in all environments
    # ANTI-PATTERN: Using default Flask server for production
    # ANTI-PATTERN: No HTTPS
    app.run(host='0.0.0.0', port=5000, debug=True) 