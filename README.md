# Aplicação flask para consultar informações da empresa

Esta aplicação Flask fornece uma API para consultar dados sobre a empresa, vagas disponiveis na empresa e detalhes sobre a vaga, parceiros da empresa e enviar um curriculo para vagas especificas.

## Endpoits
<b>Essa aplicação possui cinco endpoints sendo eles:</b>

/empresa -> que retorna os dados da empresa;<br>
/parceiros -> que retorna os dados dos parceiros da empresa;<br>
/vagas -> que retorna uma lista de vagas da empresa;<br>
/vagas/id -> que retorna os dados de uma vaga especifica;<br>
/vagas/id/curriculo -> que o cliente pode enviar seu curriculo para a vaga desejada.

## Observações

Como esse projeto foi criado apenas para fins de demontração, banco de dados ja vem com dois modelos de vagas, quatro de parceiros e uma empresa.

-> O retorno de dados esta no formato json.<br>
-> Os dados enviados para o endpoint /vagas/id/curriculo devem ser estar formato json.


## Utilização

<b>Para utilizar esse repositório siga as seguintes instruções:</b>

    1. Crie uma ambiente virtual em sua máquina e ative esse ambiente;
    2. No teminal, execute o comando pip install -r requirements.txt
    3. Para iniciar a api basta executar o comando python3 app.py
    5. Para iniciar os testes de unidade basta executar o comando python3 app.py e, em seguida, 
      em outro terminal, executar o comando python3 app_test.py
