from flask import Flask, jsonify
from flask_cors import CORS
import random
import mysql.connector  # Biblioteca para conectar com o banco de dados

app = Flask(__name__)
CORS(app)

# Conexão com o banco de dados
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="data"
    )

def get_sensor_data():
    data = {
        "temperatura": round(random.uniform(20, 80), 2),
        "umidade": round(random.uniform(30, 90), 2),
        "pressao": round(random.uniform(900, 1100), 2)
    }

    # Inserir dados no banco
    insert_sensor_data(data)

    return data

# Função para inserir os dados
def insert_sensor_data(data):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO sensores (temperatura, pressao, umidade) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['temperatura'], data['pressao'], data['umidade']))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/sensores', methods=['GET'])
def sensores():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(debug=True)
