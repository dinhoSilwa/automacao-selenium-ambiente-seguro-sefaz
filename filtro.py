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

    # --- Passo 3: Clicar no CGF ---
    cgf = os.getenv("CGF")
    if not cgf:
        raise ValueError("Variável CGF não definida no .env")

    print(f"Passo 3: Clicando no CGF '{cgf}'...")
    original_window = driver.current_window_handle  # 👈 Salva a aba original
    link_cgf = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='{cgf}']")))
    driver.execute_script("arguments[0].click();", link_cgf)  # Clique via JS para confiabilidade

    # --- ⏳ AGUARDA NOVA ABA ABRIR ---
    print("Aguardando nova aba do Portal MFE...")
    WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)

    # --- 🔁 MUDA O FOCO PARA A NOVA ABA ---
    all_windows = driver.window_handles
    new_window = None
    for handle in all_windows:
        if handle != original_window:
            new_window = handle
            break

    if new_window:
        driver.switch_to.window(new_window)
        print("✅ Foco alterado para a nova aba do Portal MFE.")
    else:
        raise RuntimeError("Nova aba não foi aberta após o clique no CGF.")

    # --- Aguarda carregamento da nova página ---
    print("Aguardando carregamento do Portal MFE...")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.mfe-migration-modal, .mainlevel"))
    )
    time.sleep(2)

    # --- ✅ FECHA POPUP DE MIGRAÇÃO (se existir) ---
    print("Verificando popup de migração 'ATENÇÃO!!!!!!'...")
    try:
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']"))
        )
        print("Popup detectado. Fechando...")
        close_btn.click()
        time.sleep(1)
    except Exception:
        print("Nenhum popup encontrado. Prosseguindo...")

    # --- Passo 4: Clicar em 'Consultar NFC-e' ---
    print("Passo 4: Clicando em 'Consultar NFC-e'...")
    link_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList']"))
    )
    link_consultar.click()
    time.sleep(2)

    # --- Passo 5: Preencher filtros ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")

    if not all([start_date, start_time, end_date, end_time]):
        raise ValueError("As variáveis START, TIMESTART, END e TIMEEND devem estar no .env")

    print("Passo 5: Preenchendo filtros de período...")

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

    # --- Passo 6: Clicar em 'Consultar' ---
    print("Passo 6: Clicando em 'Consultar'...")
    btn_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@ng-click, 'find()')]"))
    )
    btn_consultar.click()
    time.sleep(2)

    print("✅ Filtro aplicado com sucesso!")