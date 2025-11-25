from flask import Flask, jsonify, render_template
import os
import psycopg2

app = Flask(__name__)

DB = {
    "host": os.getenv("NEON_HOST"),
    "port": "5432",
    "dbname": os.getenv("NEON_DB"),
    "user": os.getenv("NEON_USER"),
    "password": os.getenv("NEON_PASSWORD"),
    "sslmode": "require"
}

TABLE_NAME = "detecciones"
ESTADO_COL = "resultado"

def get_data():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT {ESTADO_COL}, COUNT(*)
        FROM {TABLE_NAME}
        GROUP BY {ESTADO_COL};
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = {}
    for estado, total in rows:
        data[str(estado).lower()] = total

    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0")
