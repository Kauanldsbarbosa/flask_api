from data.models.curriculo import Curriculo
from data.models.vaga import Vaga
from unittest import TestCase, main as unittestmain
import json
import requests


class GetEmpresaInfoTest(TestCase):
    def test_get_empresa_info_retorna_status_code_200(self):
        response = requests.get('http://127.0.0.1:5000/empresa')
        self.assertEqual(response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        response = requests.get('http://127.0.0.1:5000/empresa')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
    def test_se_todos_os_dados_da_empresa_estao_sendo_retornados(self):
        response = requests.get('http://127.0.0.1:5000/empresa')
        campos_requeridos = ['endereco', 'id', 'links', 'nome', 'telefone']
        data = json.loads(response.content)
        campos_retornados = list(data['empresa'].keys())
        self.assertEqual(set(campos_requeridos), set(campos_retornados))
        

class GetParceirosTest(TestCase):
    def test_get_parceiros_retorna_status_code_200(self):
        response = requests.get('http://127.0.0.1:5000/parceiros')
        self.assertEqual(response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        response = requests.get('http://127.0.0.1:5000/parceiros')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
    def test_se_a_lista_de_dicionarios_e_retornada(self):
        response = requests.get('http://127.0.0.1:5000/parceiros')
        data = json.loads(response.content)
        for field in data:
            tipo_field = isinstance(field, dict)
            self.assertEqual(tipo_field, True)


class GetVagasTest(TestCase):
    def test_get_vagas_retorna_status_code_200(self):
        response = requests.get('http://127.0.0.1:5000/vagas')
        self.assertEqual(response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        response = requests.get('http://127.0.0.1:5000/vagas')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
    def test_se_a_lista_de_dicionarios_e_retornada(self):
        response = requests.get('http://127.0.0.1:5000/vagas')
        data = json.loads(response.content)
        for field in data:
            tipo_field = isinstance(field, dict)
            self.assertEqual(tipo_field, True)


class GetVagasDetailTest(TestCase):
    def test_get_vagas_retorna_status_code_200(self):
        response = requests.get('http://127.0.0.1:5000/vagas/1')
        self.assertEqual(response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        response = requests.get('http://127.0.0.1:5000/vagas/1')
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_buscar_vaga_nao_existente(self):
        response = requests.get('http://127.0.0.1:5000/vagas/999')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['mensagem'], 'vaga nao encontrada')
        
class SendCurriculo(TestCase):
    def setUp(self) -> None:
        self.data = {
            'vaga_id': '1',
            'nome': 'Fulano de Ciclano Betano',
            'cpf': '11122233345',
            'numero_de_telefone': '(11) 91234-5678',
            'data_de_nascimento': '2002-01-13',
            'email': 'fulanociclano@betano.com',
        }

        self.vaga = Vaga.get_vaga_by_id(1)
        
        self.curriculo = Curriculo.create(
                vaga = self.vaga,
                nome = self.data['nome'],
                cpf = '33344455567',
                numero_de_telefone = self.data['numero_de_telefone'],
                data_de_nascimento = self.data['data_de_nascimento'],
                email = 'teste@email.com'
        )
        return super().setUp()
    
    def test_enviar_curriculo(self):
        response = requests.post(
            url='http://127.0.0.1:5000/vagas/1/curriculo',
            json=json.dumps(self.data)
        )
        message = json.loads(response.text)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message['mensagem'], 'Currículo enviado com sucesso!')

    def test_se_curriculo_foi_salvo_no_banco_de_dados(self):
        curriculo_cadastrado = Curriculo.select().where(Curriculo.cpf == self.data['cpf'])
        self.assertEqual(curriculo_cadastrado, True)
        Curriculo.remove_curriculo_pelo_cpf(self.data['cpf'])


    def test_enviar_curriculo_com_cpf_ja_cadastrado(self):
        self.data['cpf'] = '33344455567'
        response = requests.post(
            url='http://127.0.0.1:5000/vagas/1/curriculo',
            json=json.dumps(self.data)
        )
        message = json.loads(response.text)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['mensagem'], 'Você já está inscrito(a) nessa vaga. Aguarde mais informações.')

    def test_enviar_curriculo_com_email_ja_cadastrado(self):
        self.data['email'] = 'teste@email.com'
        response = requests.post(
            url='http://127.0.0.1:5000/vagas/1/curriculo',
            json=json.dumps(self.data)
        )
        message = json.loads(response.text)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['mensagem'], 'Você já está inscrito(a) nessa vaga. Aguarde mais informações.')
        self.curriculo.delete()

if __name__ == '__main__':
    unittestmain()
    