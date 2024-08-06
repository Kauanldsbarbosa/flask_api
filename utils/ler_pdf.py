from PyPDF2 import PdfReader


def get_text_in_pdf(file_path):
    leitorPdf = PdfReader(file_path)
    page = leitorPdf.pages[0]
    text = page.extract_text()
    return text

def get_field_value_in_text(text, field_name):
    value = ''
    field_name_size = len(field_name)
    index = 0
    texto_limpo = str(text).lower().replace(' ', '_').replace(':', '').split()
    for texto in texto_limpo:
        if texto[:field_name_size] == f'{field_name}':
            for caractere in texto:
                index += 1
            value = texto[field_name_size: index].replace('_', ' ').lstrip()
    return value

