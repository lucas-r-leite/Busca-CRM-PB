import pandas as pd
import csv, requests, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


url ='https://crmpb.org.br/busca-medicos/'
headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

#Abrindo do Navegador e entrando no site
first_acess = input("Esta é a primera vez que você roda o código nesta máquina?[s/n] ")
first_acess = first_acess.lower() #Tornando todas as letras minúsculas
browser = input("Qual o seu navegador?[Chrome/Firefox]? ")
browser = browser.lower() #Tornando todas as letras minúsculas

while first_acess !="s" or first_acess!="n":
    if first_acess == "s":
        if browser=="firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            break
        elif browser=="chrome":
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            break
        else:
            print("Entrada não reconhecida, irei rodar o Google Chrome")
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            break
    elif first_acess=="n":
        if browser=="firefox":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager
            driver = webdriver.Firefox()
            break
        elif browser=="chrome":
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome()
            break
        else:
            print("Entrada não reconhecida, irei rodar o Firefox")
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome()
            break
    else:
        print("Responda s ou n!")
        first_acess = input("Esta é a primera vez que você roda o código nesta máquina?[s/n] ")
        first_acess = first_acess.lower()
        browser = input("Qual o seu navegador?[chrome/firefox]? ")
        browser = browser.lower()

driver.get("https://crmpb.org.br/busca-medicos/")

#clicando no botão da LGPD
enviar_btn = driver.find_element(By.XPATH,'//*[@id="page"]/div[4]/div[2]/button')
enviar_btn.click()

#Selecionando a UF
uf_select = driver.find_element(By.NAME,'uf')
select_uf = Select(uf_select)
select_uf.select_by_value('PB')

#Selecionando a cidade
municipio_select = driver.find_element(By.NAME,'municipio')
select_municipio = Select(municipio_select)
select_municipio.select_by_value('4964')
#select_municipio.select_by_visible_text("João Pessoa")

#Clicando no botão enviar
enviar_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/section[2]/div/div/div/article/div[2]/div/div/form/div/div[4]/div[2]/button')
enviar_btn.click()


#Esperando informações serem carregadas
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content"]/section[2]/div/div/div/div[1]/div[1]/div')))
time.sleep(2)


#Atualizando o html 
#html = driver.page_source
#soup = BeautifulSoup(html, 'html.parser')
# Criando a tabela .csv
df = pd.DataFrame(columns=["Nome do médico", "CRM", "Especialidade" ,"Situação", "Inscrição outro estado","Endereço", "Telefone"])
#final_pag = input(int("Até qual página deseja realizar a pesquisa?"))
for i in range(1,6):
    enviar_btn = driver.find_element(By.CSS_SELECTOR,f'[data-num="{i}"]')
    enviar_btn.click()
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    medicos = soup.find_all('div',class_='card-body')
    for medico in medicos[:10]:
        nome = medico.find('h4').get_text()

        #CRM
        crm = medico.find('div',class_='row').get_text()
        index_line = crm.find("-")
        index_crm = crm.find("CRM:")
        crm = crm[index_crm+4:index_line+3]

        #Situação
        situacao = medico.find('div',class_='col-md').get_text()
        index_situacao = situacao.find("Situação:")
        situacao = situacao[index_situacao+10:]

        #Especialidade
        especialidade = medico.find('div',style='display: flex;').get_text()
        especialidade = especialidade.replace("Especialidades/Áreas de Atuação:","")

        #Inscrição outro estado:
        inscricao = medico.find('div',class_='col-md-12').get_text()
        inscricao = inscricao.replace("Inscrições em outro estado: ","")

        #Endereço
        endereco = medico.find('div',class_='row endereco').get_text()
        endereco = endereco.replace("Endereço: ","")

        #Telefone
        telefone = medico.find('div',class_='row telefone').get_text()
        telefone = telefone.replace("Telefone(s): ","")
        telefone = telefone.replace("Telefone: ","")

        df = df.append({"Nome do médico": nome, "CRM":crm, "Especialidade":especialidade ,"Situação":situacao, "Inscrição outro estado":inscricao,"Endereço": endereco, "Telefone": telefone}, ignore_index=True)

df.to_csv("medicos.csv", index=False, encoding='UTF-8')

#Clicando no botão para acessar as páginas
#for i in range(1,4):
    #enviar_btn = driver.find_element(By.CSS_SELECTOR,f'[data-num="{i}"]')
    #enviar_btn.click()
    #time.sleep(5)

#Fechando navegador e encerrando o Selenium
driver.close()
driver.quit()
