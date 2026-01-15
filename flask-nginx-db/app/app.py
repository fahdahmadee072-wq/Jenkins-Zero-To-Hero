from flask import Flask
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def home():
    return "Hello from Flask + NGINX + Postgres!"

@app.route("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return "OK", 200
    except Exception as e:
        return f"DB NOT READY: {str(e)}", 500
