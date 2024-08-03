import json

from data.models import curriculo, vaga


def curriculo_ja_foi_registrado_na_vaga(curriculo_json, vaga_id):
    curriculo_enviado = json.loads(curriculo_json)
    vaga_desejada = vaga.Vaga.get_vaga_by_id(vaga_id).first()
    curriculos_na_vaga = curriculo.Curriculo.get_curriculos_na_vaga(vaga_desejada)
    for _curriculo in curriculos_na_vaga.dicts():
        email_ja_registrado = curriculo_enviado['email'] == _curriculo['email']
        cpf_ja_registrado = curriculo_enviado['cpf'] == _curriculo['cpf']
        if email_ja_registrado or cpf_ja_registrado:
                return True
    return False
