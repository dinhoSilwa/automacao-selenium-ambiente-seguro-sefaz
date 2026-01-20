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
    link_mfe = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb2003.asp?sm=104') and contains(text(), 'MFE')]"))
    )
    link_mfe.click()
    time.sleep(1.5)

    # --- Passo 2: Acessar MFe ---
    print("Passo 2: Clicando em 'Acessar MFe'...")
    link_acessar_mfe = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cweb1010.asp') and contains(text(), 'Acessar MFe')]"))
    )
    link_acessar_mfe.click()
    time.sleep(1.5)

    # --- Passo 3: Clicar no CGF e mudar para nova aba ---
    cgf = os.getenv("CGF")
    if not cgf:
        raise ValueError("Variável CGF não definida no .env")

    print(f"Passo 3: Clicando no CGF '{cgf}'...")
    original_window = driver.current_window_handle
    link_cgf = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{cgf}']")))
    driver.execute_script("arguments[0].click();", link_cgf)

    # Aguarda nova aba
    WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
    new_window = [w for w in driver.window_handles if w != original_window][0]
    driver.switch_to.window(new_window)
    print("Mudou para a nova aba.")

    # Fecha aba antiga
    driver.switch_to.window(original_window)
    driver.close()
    driver.switch_to.window(new_window)

    # --- Aguarda carregamento da nova página ---
    print("Aguardando carregamento do portal MFE...")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.mfe-migration-modal, .mainlevel"))
    )
    time.sleep(2)

    # --- Fecha popup de migração (se existir) ---
    try:
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']"))
        )
        print("Popup de migração detectado. Fechando...")
        close_btn.click()
        time.sleep(1)
    except:
        print("Nenhum popup de migração encontrado.")

    # --- Passo 4: Clicar em 'Consultar NFC-e' ---
    print("Passo 4: Clicando em 'Consultar NFC-e'...")
    link_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList']"))
    )
    link_consultar.click()
    time.sleep(2)

    # --- Preencher filtros ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")

    if not all([start_date, start_time, end_date, end_time]):
        raise ValueError("As variáveis START, TIMESTART, END e TIMEEND devem estar no .env")

    print("Preenchendo filtros...")

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

    # --- Aplicar filtro com lógica de retry + detecção de "CNPJ: Não informado" ---
    max_tentativas = 2
    tabela_xpath = '//*[@id="conteudo_central"]/div/div/div/div[3]/div[2]'

    for tentativa in range(1, max_tentativas + 1):
        print(f"\nTentativa {tentativa}: clicando em 'Consultar'...")

        # Clica no botão Consultar
        btn_consultar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='find()' and contains(text(), 'Consultar')]"))
        )
        btn_consultar.click()
        time.sleep(2)

        # Verifica se o popup de "CNPJ: Não informado" apareceu
        try:
            cnpj_nao_informado = driver.find_element(
                By.XPATH, "//div[@class='modal-body']//div[contains(@style, 'font-weight:bold;') and contains(text(), 'CNPJ: Não informado')]"
            )
            if cnpj_nao_informado.is_displayed():
                print("⚠️ Detectado 'CNPJ: Não informado'. Recarregando e repetindo o filtro...")
                driver.refresh()
                time.sleep(3)

                # Reaplica os filtros após refresh
                driver.execute_script("arguments[0].value = arguments[1];", 
                    driver.find_element(By.ID, "form-start-date-search-coupons"), start_date)
                driver.execute_script("arguments[0].value = arguments[1];", 
                    driver.find_element(By.ID, "form-end-date-search-coupons"), end_date)
                driver.execute_script("arguments[0].value = arguments[1];", 
                    driver.find_element(By.XPATH, "//input[@ng-model='formData.startDateTime']"), start_time)
                driver.execute_script("arguments[0].value = arguments[1];", 
                    driver.find_element(By.XPATH, "//input[@ng-model='formData.endDateTime']"), end_time)
                time.sleep(1)
                continue  # Repete o loop
        except:
            pass  # OK, CNPJ está informado

        # Aguarda a tabela carregar
        try:
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, tabela_xpath))
            )
            print("✅ Tabela de resultados carregada com sucesso!")
            break
        except Exception as e:
            if tentativa == max_tentativas:
                raise RuntimeError("Falha ao carregar a tabela após múltiplas tentativas.")
            print(f"Tentativa {tentativa} falhou. Tentando novamente...")

    time.sleep(2)
    print("✅ Filtro aplicado com sucesso!")