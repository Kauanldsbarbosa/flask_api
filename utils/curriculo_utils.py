import json

from data.models import curriculo, vaga


def curriculo_ja_foi_registrado_na_vaga(curriculo_dict, vaga_id):
    vaga_desejada = vaga.Vaga.get_vaga_by_id(vaga_id).first()
    curriculos_na_vaga = curriculo.Curriculo.get_curriculos_na_vaga(vaga_desejada)
    for _curriculo in curriculos_na_vaga.dicts():
        email_ja_registrado = curriculo_dict['email'] == _curriculo['email']
        cpf_ja_registrado = curriculo_dict['cpf'] == _curriculo['cpf']
        if email_ja_registrado or cpf_ja_registrado:
                return True
    return False


def arquivo_tem_extensao_pdf(arquivo):
     if not str(arquivo).endswith('.pdf'):
          return False
     return True

testaa = curriculo_ja_foi_registrado_na_vaga({
        'vaga_id': 1,
        'nome': 'aaaa',
        'cpf': '11122233345',
        'numero_de_telefone':'1',
        'data_de_nascimento':'1',
        'email': 'fulanociclano@betano.com',
    }, 1)

