from data.models.empresa import Links


def juntar_dict_empresa_links(empresa):
    try:
        parceiros_dict = {item['nome']: item['url'] for item in Links.get_parceiros_da_empresa(empresa).dicts()}
        data = empresa.dicts()[0]
        data['links'] = parceiros_dict
        return data
    except:
        return False
