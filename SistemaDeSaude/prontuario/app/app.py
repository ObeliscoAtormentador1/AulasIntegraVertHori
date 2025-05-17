from flask import Flask, jsonify, request

app = Flask(__name__)

prontuarios = {}

@app.route('/prontuarios', methods=['POST'])
def criar_prontuario():
    dados = request.json
    prontuario = {
        "consulta_id": dados['consulta_id'],
        "paciente_id": dados['paciente_id'],
        "anotacoes": "",
        "receituario": []
    }
    prontuarios[dados['consulta_id']] = prontuario
    return jsonify(prontuario), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)