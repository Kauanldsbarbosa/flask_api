from peewee import  Model, CharField
from data.database import app_database


class Parceiros(Model):
    nome = CharField()
    contato = CharField()

    class Meta:
        database = app_database

    
    @staticmethod
    def get_parceiros():
        parceiros = [parceiro for parceiro in Parceiros.select().dicts()]
        return parceiros
