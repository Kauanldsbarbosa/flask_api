from data.models.curriculo import Curriculo
import unittest
import json
from app import app
from flask.testing import FlaskClient
import os


app_test_client = app.test_client(FlaskClient)

class TestIndex(unittest.TestCase):
    def setUp(self) -> None:
        with app_test_client as client:
            self.response = client.get('/')
    
    def test_get_empresa_info_retorna_status_code_200(self):
        mesagem = self.response.get_json()['mensagem']
        self.assertIsNotNone(mesagem)
        self.assertEqual(self.response.status_code, 200) 

class TestGetEmpresaInfo(unittest.TestCase):
    def setUp(self) -> None:
        with app_test_client as client:
            self.response = client.get('/empresa')

    def test_get_empresa_info_retorna_status_code_200(self):
        self.assertEqual(self.response.status_code, 200) 

    def test_se_formato_dos_dados_e_json(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')
        
    def test_se_todos_os_dados_da_empresa_estao_sendo_retornados(self):
        campos_requeridos = ['endereco', 'id', 'links', 'nome', 'telefone']
        data = json.loads(self.response.data)
        campos_retornados = list(data['empresa'].keys())
        self.assertEqual(set(campos_requeridos), set(campos_retornados))
        

class GetParceirosTest(unittest.TestCase):
    def setUp(self) -> None:
        with app_test_client as client:
            self.response = client.get('/parceiros')

    def test_get_parceiros_retorna_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')
        
    def test_se_a_lista_de_dicionarios_e_retornada(self):
        data = json.loads(self.response.data)
        for field in data:
            tipo_field = isinstance(field, dict)
            self.assertEqual(tipo_field, True)


class GetVagasTest(unittest.TestCase):
    def setUp(self) -> None:
        with app_test_client as client:
            self.response = client.get('/vagas')

    def test_get_vagas_retorna_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')
        
    def test_se_a_lista_de_dicionarios_e_retornada(self):
        data = json.loads(self.response.data)
        for field in data:
            tipo_field = isinstance(field, dict)
            self.assertEqual(tipo_field, True)


class GetVagasDetailTest(unittest.TestCase):
    def setUp(self) -> None:
        with app_test_client as client:
            self.response = client.get('/vagas/1')
            self.bad_response = client.get('/vagas/999')

    def test_get_vagas_retorna_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_se_formato_dos_dados_e_json(self):
        self.assertEqual(self.response.headers['Content-Type'], 'application/json')

    def test_buscar_vaga_nao_existente(self):
        data = json.loads(self.bad_response.data)
        self.assertEqual(self.bad_response.status_code, 404)
        self.assertEqual(data['mensagem'], 'vaga nao encontrada')
        
class SendCurriculo(unittest.TestCase):
    def setUp(self) -> None:
        curriculo_pdf_file = os.path.join(os.getcwd(), 'data/curriculos/curriculo_teste.pdf',)
        curriculo_formato_errado_file = os.path.join(os.getcwd(), 'data/curriculos/curriculo_teste.xml',)
        with app_test_client as client:
            self.response = self.send_file(client, curriculo_pdf_file)
            self.repeated_data_response = self.send_file(client, curriculo_pdf_file)
            self.arquivo_com_formato_errado_response = self.send_file(client, curriculo_formato_errado_file)

        
    def test_enviar_curriculo(self):
        self.assertEqual(self.response.status_code, 200)


    def test_enviar_curriculo_com_dados_ja_cadastrado(self):
        response_message = self.repeated_data_response.get_json()['mensagem']
        self.assertEqual(response_message, 'Você já está inscrito(a) nessa vaga. Aguarde mais informações.')
        self.assertEqual(self.repeated_data_response.status_code, 400)

    def test_enviar_arquivo_com_formato_diferente_de_pdf(self):
        response_message = self.arquivo_com_formato_errado_response.get_json()['mensagem']
        self.assertEqual(response_message, 'Mande o arquivo em formato de pdf.')
        self.assertEqual(self.arquivo_com_formato_errado_response.status_code, 400)

    def tearDown(self) -> None:
        for registro in Curriculo.select().where(Curriculo.cpf == '11122233345'):
                        registro.delete_instance()

    def send_file(self, client, caminho_do_arquivo):
        with open(caminho_do_arquivo, 'rb') as file:
            response = client.post('/vagas/1/curriculo', data={'file': file})
            return response



if __name__ == '__main__':
    unittest.main()    
    