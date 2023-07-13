from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, origins='*')
DATABASE = 'consultas.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            codigo INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            telefono INTEGER NOT NULL,
            email TEXT NOT NULL,
            noticias BOOLEAN NOT NULL,
            asunto TEXT NOT NULL,
            duda TEXT NOT NULL,
            respuesta TEXT,
            respondido BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/consultas-pendientes', methods=['GET'])
def get_consultas_pendientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT codigo, nombre, apellido, asunto, duda
        FROM consultas
        WHERE respondido = 0
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    consultas_pendientes = []

    for row in rows:
        consulta = {
            'codigo': row['codigo'],
            'nombre': row['nombre'],
            'apellido': row['apellido'],
            'asunto': row['asunto'],
            'duda': row['duda']
        }
        consultas_pendientes.append(consulta)

    return jsonify(consultas_pendientes)


@app.route('/consultas', methods=['POST'])
def guardar_consulta():
    data = request.form  # Accede a los datos del formulario

    nombre = data['nombre']
    apellido = data['apellido']
    fecha_nacimiento = data['fecha']
    telefono = data['telefono']
    email = data['email']
    noticias = True if 'noticias' in data else False
    asunto = data['asunto']
    duda = data['duda']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consultas (nombre, apellido, fecha_nacimiento, telefono, email, noticias, asunto, duda, respondido)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido, fecha_nacimiento, telefono, email, noticias, asunto, duda, False))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Consulta guardada exitosamente'}), 200


@app.route('/consultas/<int:codigo>', methods=['GET', 'POST'])
def get_consulta(codigo):
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nombre, apellido, telefono, email, asunto, duda
            FROM consultas
            WHERE codigo = ? AND respondido = 0
        ''', (codigo,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            consulta = {
                'nombre': row['nombre'],
                'apellido': row['apellido'],
                'telefono': row['telefono'],
                'email': row['email'],
                'asunto': row['asunto'],
                'duda': row['duda']
            }
            return jsonify(consulta)
        else:
            return jsonify({'error': 'Consulta no encontrada'}), 404

    elif request.method == 'POST':
        data = request.get_json()
        respuesta = data['respuesta']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE consultas
            SET respuesta = ?, respondido = ?
            WHERE codigo = ?
        ''', (respuesta, True, codigo))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Respuesta enviada exitosamente'}), 200


if __name__ == '__main__':
    create_table()
    app.run()
