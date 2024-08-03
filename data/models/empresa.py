from peewee import  Model, CharField, TextField, ForeignKeyField
from data.database import app_database




class Empresa(Model):
    nome = CharField()
    telefone = CharField()
    endereco = CharField()

    class Meta:
        database = app_database

    @staticmethod
    def get_empresa_data():
        data = Empresa.select()
        return data
    
class Links(Model):
    empresa = ForeignKeyField(Empresa, backref='empresa')
    nome = CharField()
    url = TextField()

    class Meta:
        database = app_database

    @staticmethod
    def get_parceiros_da_empresa(_empresa):
        parceiros = Links.select().where(Links.empresa == _empresa)
        return parceiros
