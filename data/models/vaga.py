from peewee import  Model, CharField, DateField
from data.database import app_database


class Vaga(Model):
    vaga = CharField()
    descricao = CharField()
    modalidade = CharField()
    tipo = CharField()
    formacao = CharField()
    data_encerramento = DateField(formats='%Y-%m-%d')

    class Meta:
        database = app_database

    @staticmethod
    def get_vagas():
        vagas = [vaga for vaga in Vaga.select().dicts()]
        return vagas
    
    @staticmethod
    def get_vaga_by_id(id):
        vaga = Vaga.select().where(Vaga.id == id)
        return vaga
    