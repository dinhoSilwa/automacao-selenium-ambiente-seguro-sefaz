# filtro.py

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

def aplicar_filtro_mfe(driver):
    wait = WebDriverWait(driver, 30)

    # --- Passos 1 a 3: navegação até o CGF ---
    print("Passo 1: Acessando MFE...")
    link_mfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb2003.asp?sm=104') and contains(text(), 'MFE')]")))
    link_mfe.click()
    time.sleep(1.5)

    print("Passo 2: Clicando em 'Acessar MFe'...")
    link_acessar_mfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb1010.asp') and contains(text(), 'Acessar MFe')]")))
    link_acessar_mfe.click()
    time.sleep(1.5)

    cgf = os.getenv("CGF")
    print(f"Passo 3: Clicando no CGF '{cgf}'...")
    link_cgf = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{cgf}']")))
    link_cgf.click()
    print("Redirecionando para o portal MFE...")

    # ⏳ Aguarda carregar a nova página (basta esperar pelo popup ou pelo menu)
    print("Aguardando carregamento da página do portal MFE...")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.mfe-migration-modal, .mainlevel"))
    )
    time.sleep(2)

    # ✅ FECHA O POPUP DE MIGRAÇÃO (obrigatório antes de qualquer interação)
    print("Passo 4: Verificando e fechando popup de migração...")
    try:
        close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']"))
        )
        print("Popup detectado. Fechando...")
        close_button.click()
        # Aguarda o popup desaparecer
        wait.until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mfe-migration-modal"))
        )
        time.sleep(1)
    except Exception as e:
        print("Nenhum popup de migração ativo.")

    # ✅ AGORA SIM: clica no link "Consultar NFC-e"
    print("Passo 5: Clicando em 'Consultar NFC-e'...")
    link_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList']"))
    )
    link_consultar.click()
    time.sleep(2)

    # --- Preenchimento dos filtros ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")

    if not all([start_date, start_time, end_date, end_time]):
        raise ValueError("As variáveis START, TIMESTART, END e TIMEEND devem estar no .env")

    print("Passo 6: Preenchendo filtros...")

    # Datas
    driver.execute_script("arguments[0].value = arguments[1];", 
        driver.find_element(By.ID, "form-start-date-search-coupons"), start_date)
    driver.execute_script("arguments[0].value = arguments[1];", 
        driver.find_element(By.ID, "form-end-date-search-coupons"), end_date)

    # Horários
    driver.execute_script("arguments[0].value = arguments[1];", 
        driver.find_element(By.XPATH, "//input[@ng-model='formData.startDateTime']"), start_time)
    driver.execute_script("arguments[0].value = arguments[1];", 
        driver.find_element(By.XPATH, "//input[@ng-model='formData.endDateTime']"), end_time)

    time.sleep(1)

    # Botão Consultar
    print("Passo 7: Clicando em 'Consultar'...")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@ng-click, 'find()')]")))
    btn.click()
    time.sleep(2)

    print("✅ Filtro aplicado com sucesso!")