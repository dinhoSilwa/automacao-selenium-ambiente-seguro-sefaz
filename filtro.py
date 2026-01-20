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

    # --- Passo 1: Acessar MFE ---
    print("Passo 1: Acessando 'MFE - Modulo Fiscal Eletronico'...")
    link_mfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb2003.asp?sm=104') and contains(text(), 'MFE')]")))
    link_mfe.click()
    time.sleep(1.5)

    # --- Passo 2: Acessar MFe ---
    print("Passo 2: Clicando em 'Acessar MFe'...")
    link_acessar_mfe = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb1010.asp') and contains(text(), 'Acessar MFe')]")))
    link_acessar_mfe.click()
    time.sleep(1.5)

    # --- Passo 3: Clicar no link com CGF ---
    cgf = os.getenv("CGF")
    if not cgf:
        raise ValueError("Variável CGF não definida no .env")

    print(f"Passo 3: Procurando link com CGF '{cgf}'...")
    try:
        # Tenta encontrar o link pelo texto exato
        link_cgf = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{cgf}']"))
        )

        # Scroll até o elemento (garante que está visível)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", link_cgf)
        time.sleep(1)

        # Tenta clicar normalmente
        link_cgf.click()
        print("Clique no CGF realizado com sucesso.")

    except Exception as e:
        print(f"Falha ao clicar no CGF via XPath. Tentando via JavaScript...")
        # Se falhar, tenta clicar via JS (bypass de obstáculos visuais)
        try:
            link_cgf_js = driver.find_element(By.XPATH, f"//a[text()='{cgf}']")
            driver.execute_script("arguments[0].click();", link_cgf_js)
            print("Clique no CGF realizado via JavaScript.")
        except Exception as js_error:
            raise RuntimeError(f"Falha ao clicar no CGF '{cgf}': {js_error}")

    print("Redirecionando para o portal MFE...")

    # --- ⏳ AGUARDA O CARREGAMENTO DA NOVA PÁGINA (SPA) ---
    print("Aguardando carregamento do menu do portal MFE...")
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'consultar-cupons-nfce-fiscais')]"))
    )
    time.sleep(2)

    # --- ✅ FECHA POPUP DE MIGRAÇÃO (se estiver visível) ---
    print("Verificando popup de migração 'ATENÇÃO!!!!!!'...")
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']")
        if close_button.is_displayed():
            print("Popup detectado. Fechando...")
            close_button.click()
            time.sleep(1)
    except Exception:
        print("Nenhum popup de migração encontrado.")

    # --- Passo 4: Clicar em 'Consultar NFC-e' ---
    print("Passo 4: Clicando em 'Consultar NFC-e'...")
    link_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'consultar-cupons-nfce-fiscais')]"))
    )
    link_consultar.click()
    time.sleep(2)

    # --- Passo 5: Preencher filtros de data/hora ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")

    if not all([start_date, start_time, end_date, end_time]):
        raise ValueError("As variáveis START, TIMESTART, END e TIMEEND devem estar no .env")

    print("Passo 5: Preenchendo filtros de período...")

    # Data inicial
    date_start_input = wait.until(EC.presence_of_element_located((By.ID, "form-start-date-search-coupons")))
    driver.execute_script("arguments[0].value = arguments[1];", date_start_input, start_date)

    # Hora inicial
    time_start_input = driver.find_element(By.XPATH, "//input[@ng-model='formData.startDateTime' and @bs-timepicker]")
    driver.execute_script("arguments[0].value = arguments[1];", time_start_input, start_time)

    # Data final
    date_end_input = driver.find_element(By.ID, "form-end-date-search-coupons")
    driver.execute_script("arguments[0].value = arguments[1];", date_end_input, end_date)

    # Hora final
    time_end_input = driver.find_element(By.XPATH, "//input[@ng-model='formData.endDateTime' and @bs-timepicker]")
    driver.execute_script("arguments[0].value = arguments[1];", time_end_input, end_time)

    time.sleep(1)

    # --- Passo 6: Clicar em 'Consultar' ---
    print("Passo 6: Clicando em 'Consultar'...")
    btn_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Consultar') and @ng-click]"))
    )
    btn_consultar.click()
    time.sleep(2)

    print("✅ Filtro aplicado com sucesso!")