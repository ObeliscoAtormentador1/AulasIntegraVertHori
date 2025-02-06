from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

CORS(app)

def get_sensor_data():
    return {
        "temperatura":round(random.uniform(20,80), 2),
        "umidade":round(random.uniform(30,90), 2),
        "pressao":round(random.uniform(900,1100), 2)
    }

@app.route('/sensores', methods=['GET'])
def sensores():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(debug=True)
