# Desafio-Python-Asset
<strong>Atividade Python:</strong>

Crie um código que entre no site https://crmpb.org.br/busca-medicos/ , clique no botão enviar da pesquisa e crie uma tabela com os primeiros 10 médicos, com os parametros já definidos na busca e salve em .csv. (Ex.: Colunas: nome do médico; Especialidade; Telefone)

<strong>Detalhes:</strong>
Como o código utiliza a biblioteca Selenium, será necessária a instalação do geckodrive(Firefox) e/ou ChromeDriver(Google Chrome). Os links para download seguem abaixo:

GoogleDriver: https://chromedriver.chromium.org/

Geckdriver: https://github.com/mozilla/geckodriver/releases

<strong>Explicação:</strong>
O código em questão é um script em Python que utiliza as bibliotecas pandas, csv, requests, time, selenium e BeautifulSoup para acessar um site (https://crmpb.org.br/busca-medicos/) e coletar informações sobre médicos cadastrados no Conselho Regional de Medicina da Paraíba (CRM-PB).

A primeira parte do código é a importação das bibliotecas necessárias e a definição da URL do site que será acessado. Em seguida, é definido um cabeçalho (headers) para a requisição, que inclui informações sobre o navegador utilizado.

A partir daí, o código utiliza a biblioteca selenium para abrir um navegador (Firefox), acessar a URL definida anteriormente e clicar em dois botões na página. O primeiro botão refere-se à Lei Geral de Proteção de Dados (LGPD) e o segundo ao botão de envio de informações. Em seguida, o código aguarda 3 segundos para que as informações sejam carregadas.

Com a página carregada, o código utiliza a biblioteca BeautifulSoup para coletar informações sobre os médicos cadastrados. O código busca por todas as tags HTML com a classe 'card-body' e armazena as informações em um objeto BeautifulSoup chamado 'medicos'.

Em seguida, o código utiliza a biblioteca pandas para criar um DataFrame vazio com as colunas "Nome do médico", "CRM", "Especialidade", "Situação", "Inscrição outro estado", "Endereço" e "Telefone". O código utiliza um loop para percorrer os 10 primeiros elementos da lista 'medicos' e extrair as informações necessárias sobre cada médico. As informações são armazenadas no DataFrame criado anteriormente.

Por fim, o código utiliza a biblioteca pandas para salvar o DataFrame em um arquivo .csv chamado "medicos.csv" e encerra o navegador.

Resumindo, o código em questão automatiza o processo de coleta de informações sobre médicos cadastrados no CRM-PB e as armazena em um arquivo .csv para posterior análise.
