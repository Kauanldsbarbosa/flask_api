from flask import Flask, jsonify, request
from utils import juntar_dict as jdel, curriculo_registrado as cure
from data.settings import configure_database
from data.models import curriculo, vaga, parceiro, empresa
import json


app = Flask(__name__)

configure_database()

@app.route('/empresa', methods=['GET'])
def get_empresa_info():
    empresa_data = empresa.Empresa.get_empresa_data()
    data = jdel.juntar_dict_empresa_links(empresa_data)
    return jsonify({'empresa': data}), 200

@app.route('/parceiros', methods=['GET'])
def get_parceiros():
    parceiros = parceiro.Parceiros.get_parceiros()
    return jsonify(parceiros), 200

@app.route('/vagas', methods=['GET'])
def get_vagas():
    vagas = vaga.Vaga.get_vagas()
    return jsonify(vagas), 200

@app.route('/vagas/<int:vaga_id>', methods=['GET'])
def get_vaga_detail(vaga_id):
    vaga_data = vaga.Vaga.get_vaga_by_id(vaga_id).dicts().first()
    if not vaga_data:
        return jsonify({'mensagem': 'vaga nao encontrada'}), 404
    return jsonify({'vaga': vaga_data}), 200

@app.route('/vagas/<int:vaga_id>/curriculo', methods=['POST'])
def send_curriculo(vaga_id):
    curriculo_enviado = request.get_json()
    if cure.curriculo_ja_foi_registrado_na_vaga(curriculo_enviado, vaga_id):
        return jsonify({"mensagem": "Você já está inscrito(a) nessa vaga. Aguarde mais informações."}), 400
    
    curriculo.Curriculo.add_curriculo_por_dicionario(json.loads(curriculo_enviado))
    return jsonify({"mensagem": "Currículo enviado com sucesso!"}), 200

app.run(debug=True)
