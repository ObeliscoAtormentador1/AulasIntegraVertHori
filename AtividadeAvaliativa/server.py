from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random
import mysql.connector
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

#Conexão com Thinspeak
API_KEY = "5N7GPW8YT9NMVTPL"
URL = f"https://api.thingspeak.com/update?api_key=5N7GPW8YT9NMVTPL"
api_key = "5N7GPW8YT9NMVTPL"


def enviar_dados(temperatura, umidade, pressao, radiacao) :
    url = f'https://api.thingspeak.com/update?api_key=5N7GPW8YT9NMVTPL&field1={temperatura}&field2={umidade}&field3={pressao}&field4={radiacao}'
    resposta = requests.get(url)
    print(f"Resposta: {resposta.text}")

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="data"
    )

def insert_sensor_data(data):
    conn = None
    cursor = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO sensores (temperatura, pressao, umidade, radiacao) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['temperatura'], data['pressao'], data['umidade'], data['radiacao']))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_sensor_data():
    data = {
        "temperatura": round(random.uniform(20, 80), 2),
        "umidade": round(random.uniform(30, 90), 2),
        "pressao": round(random.uniform(900, 1100), 2),
        "radiacao": round(random.uniform(15, 2000), 2),
    }

    # Enviar ao banco MySQL
    insert_sensor_data(data)

    # Enviar ao ThingSpeak
    try:
        response = requests.get(
            "https://api.thingspeak.com/update",
            params={
                "api_key": API_KEY,
                "field1": data["temperatura"],
                "field2": data["umidade"],
                "field3": data["pressao"],
                "field4": data["radiacao"],
            }
        )
        print("ThingSpeak response:", response.text)  # Deve retornar um número se funcionar
    except Exception as e:
        print("Erro ao enviar ao ThingSpeak:", e)

    return data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensores', methods=['GET'])
def sensores():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(debug=True)
