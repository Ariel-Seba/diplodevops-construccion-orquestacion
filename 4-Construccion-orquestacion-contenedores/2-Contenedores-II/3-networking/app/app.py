import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            apellido VARCHAR(100),
            documento INTEGER
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM personas")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": r[0], "nombre": r[1], "apellido": r[2], "documento": r[3]}
        for r in rows
    ])


@app.route('/personas', methods=['POST'])
def create():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO personas (nombre, apellido, documento) VALUES (%s, %s, %s) RETURNING id",
        (data['nombre'], data['apellido'], data['documento'])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, **data}), 201


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
