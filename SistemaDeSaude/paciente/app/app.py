from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Habilita CORS
app.secret_key = 'dev-secret-key'

CONSULTA_SERVICE_URL = os.getenv('CONSULTA_SERVICE_URL', 'http://consulta:5000')

# Dados em memória
users_db = {
    'paciente': {'password': 'senha123', 'name': 'Paciente Teste'}
}

# Rotas básicas
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users_db and users_db[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Credenciais inválidas')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# API
@app.route('/api/pacientes/<username>', methods=['GET'])
def get_paciente(username):
    if username in users_db:
        return jsonify({
            'username': username,
            'name': users_db[username]['name']
        })
    return jsonify({'error': 'Paciente não encontrado'}), 404

@app.route('/api/consultas', methods=['GET'])
def get_consultas():
    if 'user' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    try:
        response = requests.get(f"{CONSULTA_SERVICE_URL}/consultas?paciente={session['user']}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Serviço de consultas indisponível'}), 503
    
@app.route('/api/agendar-consulta', methods=['POST'])
def agendar_consulta():
    if 'user' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    try:
        dados = {
            'paciente': session['user'],
            'especialidade': request.json.get('especialidade'),
            'data': request.json.get('data'),
            'hora': request.json.get('hora')
        }
        
        response = requests.post(
            f"{CONSULTA_SERVICE_URL}/consultas",
            json=dados,
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Serviço de consultas indisponível'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)