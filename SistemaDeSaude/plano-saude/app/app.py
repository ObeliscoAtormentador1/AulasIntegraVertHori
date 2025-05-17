from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/planos/<plano_id>/cobertura/<procedimento>', methods=['GET'])
def verificar_cobertura(plano_id, procedimento):
    # Simulação - sempre retorna coberto para testes
    return jsonify({
        "coberto": True,
        "valor_coberto": 100.00
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)