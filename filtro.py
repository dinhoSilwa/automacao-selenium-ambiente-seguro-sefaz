# filtro.py

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

def aplicar_filtro_mfe(driver):
    """
    Executa o fluxo completo de navegação e filtragem após o login.
    Recebe um driver autenticado (ex: retornado por login.py).
    """
    wait = WebDriverWait(driver, 20)

    # --- Passo 1: Clicar em "MFE - Modulo Fiscal Eletronico" ---
    print("Passo 1: Acessando MFE...")
    link_mfe = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb2003.asp?sm=104') and contains(text(), 'MFE - Modulo Fiscal Eletronico')]"))
    )
    link_mfe.click()
    time.sleep(2)

    # --- Passo 2: Clicar em "Acessar MFe" ---
    print("Passo 2: Clicando em 'Acessar MFe'...")
    link_acessar_mfe = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb1010.asp') and contains(text(), 'Acessar MFe')]"))
    )
    link_acessar_mfe.click()
    time.sleep(2)

    # --- Passo 3: Clicar no link com o CGF exato ---
    cgf = os.getenv("CGF")
    if not cgf:
        raise ValueError("Variável CGF não definida no .env")

    print(f"Passo 3: Procurando e clicando no link com CGF = {cgf}...")
    link_cgf = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//a[text()='{cgf}']"))
    )
    link_cgf.click()
    time.sleep(2)

    # --- Passo 4: Fechar popup "ATENÇÃO!!!!!!" (se aparecer) ---
    print("Passo 4: Aguardando possível popup 'ATENÇÃO!!!!!!'...")
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-header']//button[@class='close' and @ng-click='$hide()']"))
        )
        print("Popup detectado. Fechando...")
        close_button.click()
        WebDriverWait(driver, 3).until_not(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-header']/h4[text()='ATENÇÃO!!!!!!']"))
        )
        time.sleep(1)
    except Exception:
        print("Nenhum popup 'ATENÇÃO!!!!!!' encontrado ou não foi necessário fechar.")


    # --- Passo 5: Clicar em "Consultar NFC-e" ---
    print("Passo 5: Acessando 'Consultar NFC-e'...")
    link_consultar_nfce = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList' and contains(@href, 'consultar-cupons-nfce-fiscais')]"))
    )
    link_consultar_nfce.click()
    time.sleep(3)

    # --- Passo 6: Preencher data/hora de início ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    if not start_date or not start_time:
        raise ValueError("Variáveis START e TIMESTART devem estar definidas no .env")

    print(f"Passo 6: Preenchendo período inicial: {start_date} {start_time}...")
    date_start_input = wait.until(EC.presence_of_element_located((By.ID, "form-start-date-search-coupons")))
    driver.execute_script("arguments[0].value = arguments[1];", date_start_input, start_date)
    time.sleep(0.5)

    time_start_input = driver.find_element(By.XPATH, "//input[@ng-model='formData.startDateTime' and @bs-timepicker]")
    driver.execute_script("arguments[0].value = arguments[1];", time_start_input, start_time)
    time.sleep(1)

    # --- Passo 7: Preencher data/hora final ---
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")
    if not end_date or not end_time:
        raise ValueError("Variáveis END e TIMEEND devem estar definidas no .env")

    print(f"Passo 7: Preenchendo período final: {end_date} {end_time}...")
    date_end_input = driver.find_element(By.ID, "form-end-date-search-coupons")
    driver.execute_script("arguments[0].value = arguments[1];", date_end_input, end_date)
    time.sleep(0.5)

    time_end_input = driver.find_element(By.XPATH, "//input[@ng-model='formData.endDateTime' and @bs-timepicker]")
    driver.execute_script("arguments[0].value = arguments[1];", time_end_input, end_time)
    time.sleep(1)

    # --- Passo 8: Clicar no botão "Consultar" ---
    print("Passo 8: Clicando em 'Consultar'...")
    btn_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@ng-click, 'find()') and contains(text(), 'Consultar')]"))
    )
    btn_consultar.click()
    time.sleep(2)

    print("✅ Filtro aplicado com sucesso!")