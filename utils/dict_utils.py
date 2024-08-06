from data.models.empresa import Links


def juntar_dict_empresa_links(empresa):
    try:
        parceiros_dict = {item['nome']: item['url'] for item in Links.get_parceiros_da_empresa(empresa).dicts()}
        data = empresa.dicts()[0]
        data['links'] = parceiros_dict
        return data
    except:
        return False

def gerar_dict_com_campos_do_curriculo(vaga_id, nome, cpf, numero_de_telefone, data_de_nascimento, email):
    curriculo_dict = {
        'vaga_id': vaga_id,
        'nome': nome,
        'cpf': cpf,
        'numero_de_telefone':numero_de_telefone,
        'data_de_nascimento':data_de_nascimento,
        'email': email,
    }

    return curriculo_dict
