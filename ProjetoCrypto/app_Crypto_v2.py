from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
import requests
import schedule
from datetime import datetime
from credentials import *

def jobAlerta():
    # Configurando o driver do navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # Acessando a página das criptomoedas
    url = "https://br.investing.com/crypto/"
    driver.get(url)

    # Esperando a página carregar completamente
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "fullColumn")))

    # Coletando as informações das criptomoedas Apenas as 10 primeiras
    criptomoedas = []

    rows = driver.find_elements('xpath', './/tbody/tr')[:10]
    for row in tqdm(rows, total=10):
        # ranking = row.find_element('xpath', './/td[1]/a').text
        # time.sleep(1)
        nome = row.find_element('xpath', './/td[3]').text
        time.sleep(3)
        codigos = row.find_elements('xpath', './/td[4]')
        time.sleep(3)
        precos = row.find_elements('xpath', './/td[5]')
        time.sleep(3)
        for codigo, preco in zip(codigos, precos):
            criptomoedas.append({"Crypto": nome, "Código": codigo.text, "Valor": preco.text})
    # Imprimindo as informações coletadas
    #print(json.dumps(criptomoedas, indent=4, ensure_ascii=False))

    # Obter a data e hora atual
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # variavel message em branco para receber os dados antes do envio ao Telegram
    message = ""
    # Concatenando todos os dados da Lista e agrupando na message
    for criptomoeda in criptomoedas:
        message += f"Crypto: {criptomoeda.get('Crypto', '')}\n"
        message += f"Código: {criptomoeda.get('Código', '')}\n"
        message += f"Valor: $ {criptomoeda.get('Valor', '')}\n"
        message += "\n"
        hoje = f"Data do envio: {now}"
        alerta = ":: ALERTA CRYPTO ::\n"
    print(alerta + message + hoje)

    #Enviando ao Telegram
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={alerta}+{message}+{hoje}'
    requests.get(url)

    # Fechando o driver do navegador
    driver.quit()

#Programando para Requisitar e enviar a cada 40 minutos
schedule.every(40).seconds.do(jobAlerta)

while True:
    schedule.run_pending()
    time.sleep(1)