from peewee import  Model, CharField, DateField, ForeignKeyField
from data.database import app_database
from data.models import vaga
import json


class Curriculo(Model):
    vaga = ForeignKeyField(vaga.Vaga, related_name='vaga')
    nome = CharField()
    cpf = CharField()
    numero_de_telefone = CharField()
    data_de_nascimento = DateField()
    email = CharField()

    class Meta:
        database = app_database


    @staticmethod
    def get_curriculos_na_vaga(vaga):
        curriculos_na_vaga = Curriculo.select().where(Curriculo.vaga == vaga.id)
        return curriculos_na_vaga

    @staticmethod
    def add_curriculo_por_dicionario(dict):
        try:
            vaga_desejada = vaga.Vaga.get_vaga_by_id(dict['vaga_id'])
            new_curriculo = Curriculo(
                vaga = vaga_desejada['vaga_id'],
                nome = dict['nome'],
                cpf = dict['cpf'],
                numero_de_telefone = dict['numero_de_telefone'],
                data_de_nascimento = dict['data_de_nascimento'],
                email = dict['email']
            )
            new_curriculo.save()
            return True
        
        except:
            return False

    @staticmethod
    def remove_curriculo_pelo_cpf(cpf):
        try:
            Curriculo.select().where(Curriculo.cpf == cpf).first().delete()
        except:
            pass