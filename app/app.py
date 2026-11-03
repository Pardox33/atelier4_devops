import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "campus")
DB_USER = os.getenv("DB_USER", "campus")
DB_PASSWORD = os.getenv("DB_PASSWORD", "dev-password")


@app.get("/health")
def health():
    try:
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3,
        ) as conn:
            conn.execute("select 1")
        return jsonify(status="ok", database="up")
    except Exception as e:
        app.logger.error("Database unreachable (%s:%s): %s", DB_HOST, DB_PORT, e)
        return jsonify(status="down", database="down"), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
