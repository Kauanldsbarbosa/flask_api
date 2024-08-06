import os
from flask import Flask, jsonify, request
from utils import curriculo_utils, dict_utils, ler_pdf, generate_random_numbers
from data.settings import configure_database
from data.models import curriculo, vaga, parceiro, empresa
import json


app = Flask(__name__)

configure_database()

@app.route('/', methods=['GET'])
def index():
    mensagem = ('realize uma chamada para algum dos endpoints: /empresa, /parceiros, /vagas, vagas/id, /vagas/<int:vaga_id>/curriculo',
        'Para obter detalhes da funcionalidade desta API consulte:',
        'https://github.com/Kauanldsbarbosa/flask_api/blob/main/README.md')
    return jsonify({'mensagem': mensagem}), 200

@app.route('/empresa', methods=['GET'])
def get_empresa_info():
    empresa_data = empresa.Empresa.get_empresa_data()
    data = dict_utils.juntar_dict_empresa_links(empresa_data)
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
    curriculo_file = os.path.join(
        os.getcwd(), 
        f'data/curriculos/curriculo{generate_random_numbers.generate_random_numbers()}.pdf',)
    
    curriculo_enviado = request.files['file']
    curriculo_enviado.save(dst=curriculo_file)


    curriculo_data = ler_pdf.get_text_in_pdf(curriculo_file)

    curriculo_dict_com_informações_de_interrese = dict_utils.gerar_dict_com_campos_do_curriculo(
        vaga.Vaga.get_by_id(vaga_id),
        ler_pdf.get_field_value_in_text(curriculo_data, 'nome'),
        ler_pdf.get_field_value_in_text(curriculo_data, 'cpf').replace(' ', ''),
        ler_pdf.get_field_value_in_text(curriculo_data, 'telefone'),
        ler_pdf.get_field_value_in_text(curriculo_data, 'data_de_nascimento').replace('/', '-'),
        ler_pdf.get_field_value_in_text(curriculo_data, 'email').replace(' ', ''),
    )
    
    if not curriculo_utils.arquivo_tem_extensao_pdf(curriculo_enviado.filename):
        os.remove(curriculo_file)
        return jsonify({"mensagem": "Mande o arquivo em formato de pdf."}), 400
    
    if curriculo_utils.curriculo_ja_foi_registrado_na_vaga(curriculo_dict_com_informações_de_interrese, vaga_id):
        os.remove(curriculo_file)
        return jsonify({"mensagem": "Você já está inscrito(a) nessa vaga. Aguarde mais informações."}), 400
    
    
    curriculo.Curriculo.add_curriculo_por_dicionario(dict=curriculo_dict_com_informações_de_interrese)
    os.remove(curriculo_file)
    return jsonify({"mensagem": "Currículo enviado com sucesso!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
