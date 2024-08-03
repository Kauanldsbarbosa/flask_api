from data.models import empresa, parceiro, vaga, curriculo
from data.database import app_database


def configure_database():
    app_database.connect()
    app_database.create_tables([empresa.Empresa, empresa.Links, parceiro.Parceiros, vaga.Vaga, curriculo.Curriculo])
    

if __name__ == '__main__':
    configure_database()