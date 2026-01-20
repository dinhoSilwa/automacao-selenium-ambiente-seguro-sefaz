# login.py

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

def realizar_login_sefaz() -> webdriver.Chrome:
    """
    Realiza login no portal da SEFAZ-CE.
    Verifica se há mensagem de "usuário já logado" e aborta se necessário.
    Configura o Chrome para permitir downloads automáticos de XMLs.
    Retorna o driver autenticado.
    """
    # Configurações do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 👇 Configurações para download automático (evita "arquivo perigoso")
    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
    }
    options.add_experimental_option("prefs", prefs)

    # Inicializa o driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("delete navigator.__proto__.webdriver")

    try:
        url = os.getenv("SEFAZ_URL")
        cpf = os.getenv("CPF")
        senha = os.getenv("SENHA")

        if not all([url, cpf, senha]):
            raise ValueError("As variáveis SEFAZ_URL, CPF e SENHA devem estar definidas no .env")

        print("Acessando a URL da SEFAZ-CE...")
        driver.get(url)
        time.sleep(2)

        # 🔍 Verificação crítica: usuário já logado?
        try:
            mensagem_erro = driver.find_element(
                By.XPATH,
                "//p[contains(@style, 'color:#c00;') and contains(text(), 'O usuário já está logado no sistema')]"
            )
            if mensagem_erro.is_displayed():
                print("\n❌ ERRO CRÍTICO: O usuário já está logado no sistema.")
                print("   > Verifique outro login ou aguarde alguns minutos.")
                print("   > Encerrando o programa automaticamente.\n")
                driver.quit()
                sys.exit(1)
        except Exception:
            pass  # Prossegue normalmente

        # Preenche CPF
        wait = WebDriverWait(driver, 15)
        campo_cpf = wait.until(EC.presence_of_element_located((By.ID, "txtUsuario")))
        time.sleep(1)
        print("Digitando CPF...")
        for char in cpf:
            campo_cpf.send_keys(char)
            time.sleep(0.3)

        time.sleep(1)

        # Preenche senha
        campo_senha = driver.find_element(By.ID, "txtSenha")
        print("Digitando senha...")
        for char in senha:
            campo_senha.send_keys(char)
            time.sleep(0.3)

        time.sleep(1.5)

        # Seleciona "CONTADOR"
        print("Selecionando tipo de usuário: CONTADOR...")
        select_tipo = driver.find_element(By.ID, "cboTipoUsuario")
        Select(select_tipo).select_by_value("3")
        time.sleep(1.5)

        # Clica em Entrar
        print("Clicando em 'Entrar'...")
        botao_entrar = driver.find_element(By.ID, "btEntrar")
        botao_entrar.click()

        print("✅ Login concluído com sucesso!\n")
        return driver

    except Exception as e:
        driver.quit()
        raise RuntimeError(f"Falha no login: {e}")