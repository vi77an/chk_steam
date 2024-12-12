from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def carregar_credenciais(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    credenciais = []
    for linha in linhas:
        partes = linha.strip().split(":")
        if len(partes) >= 2:
            usuario, senha = partes[-2], partes[-1]
            credenciais.append((usuario, senha))
    return credenciais

def realizar_login(driver, wait, usuario, senha):
    try:
        driver.get("https://store.steampowered.com/login/")

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2GBWeup5cttgbTw8FM3tfx"))).send_keys(usuario)
        driver.find_elements(By.CLASS_NAME, "_2GBWeup5cttgbTw8FM3tfx")[1].send_keys(senha)

        driver.find_element(By.CLASS_NAME, "DjSvCZoKKfoNSmarsEcTS").click()

        time.sleep(5)

        if driver.find_elements(By.CLASS_NAME, "_2o5mE8JpPFOyJ0HwX_y0y7"):
            print(f"A conta {usuario} está protegida por autenticação via e-mail.")
            return
        if driver.find_elements(By.CLASS_NAME, "_1W_6HXiG4JJ0By1qN_0fGZ"):
            print(f"Erro de login para {usuario}: Verifique a sua senha e nome de usuário e tente novamente.")
            return
        if driver.find_elements(By.CLASS_NAME, "_3H-JHTYIWOo9uVrF0SXAX0"):
            print(f"Erro geral para {usuario}: Houve um erro ao tentar iniciar a sessão. Tente novamente mais tarde.")
            return

        if "store.steampowered.com" in driver.current_url:
            print(f"Login efetuado com sucesso para {usuario}!")
        else:
            print(f"Falha no login para {usuario}. Verifique as credenciais.")

    except Exception as e:
        print(f"Erro inesperado ao tentar login para {usuario}: {e}")

caminho_arquivo = "credenciais.txt"
credenciais = carregar_credenciais(caminho_arquivo)

if not credenciais:
    print("Erro: Não foi possível carregar as credenciais do arquivo.")
    exit()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    for usuario, senha in credenciais:
        realizar_login(driver, wait, usuario, senha)
finally:
    driver.quit()
