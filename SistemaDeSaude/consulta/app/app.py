from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS

consultas_db = []
next_id = 1

@app.route('/consultas', methods=['GET', 'POST', 'OPTIONS'])
def handle_consultas():
    if request.method == 'GET':
        paciente = request.args.get('paciente')
        consultas = [c for c in consultas_db if c['paciente'] == paciente] if paciente else consultas_db
        return jsonify(consultas)
    
    elif request.method == 'POST':
        try:
            dados = request.json
            
            if not all(k in dados for k in ['paciente', 'especialidade', 'data', 'hora']):
                return jsonify({"error": "Dados incompletos"}), 400
            
            global next_id
            consulta = {
                "id": next_id,
                "paciente": dados['paciente'],
                "especialidade": dados['especialidade'],
                "data": dados['data'],
                "hora": dados['hora'],
                "status": "agendada"
            }
            
            consultas_db.append(consulta)
            next_id += 1
            
            return jsonify(consulta), 201
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'OPTIONS':
        return jsonify({}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)