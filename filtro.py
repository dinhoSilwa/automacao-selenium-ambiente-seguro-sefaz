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

    # --- FECHA POPUP DE MIGRAÇÃO (mfe-migration-modal) ---
    print("Fechando popup de migração (se presente)...")
    try:
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']"))
        )
        close_btn.click()
        time.sleep(1)
    except:
        print("Nenhum popup de migração encontrado.")

    # --- Aguarda carregamento da página de consulta NFC-e ---
    print("Aguardando carregamento da página de consulta NFC-e...")
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList']"))
    )
    time.sleep(1)

    # --- Clica em 'Consultar NFC-e' ---
    print("Passo 4: Clicando em 'Consultar NFC-e'...")
    link_consultar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@ui-sref='taxpayers.fiscalCouponsNfceList']"))
    )
    link_consultar.click()
    time.sleep(2)

    # --- Preenche filtros ---
    start_date = os.getenv("START")
    start_time = os.getenv("TIMESTART")
    end_date = os.getenv("END")
    end_time = os.getenv("TIMEEND")

    if not all([start_date, start_time, end_date, end_time]):
        raise ValueError("As variáveis START, TIMESTART, END e TIMEEND devem estar no .env")

    print("Preenchendo filtros de período...")

    # Usa ng-model (mais estável que ID)
    def set_angular_input(el, value):
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, el, value)

    start_date_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-model='formData.startDate']")))
    end_date_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-model='formData.endDate']")))
    start_time_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-model='formData.startDateTime']")))
    end_time_el = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-model='formData.endDateTime']")))

    set_angular_input(start_date_el, start_date)
    set_angular_input(end_date_el, end_date)
    set_angular_input(start_time_el, start_time)
    set_angular_input(end_time_el, end_time)
    time.sleep(1)

    # --- Define status como "Autorizada" ---
    print("Definindo status como 'Autorizada'...")
    try:
        # Clica no toggle do dropdown
        toggle = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='btn btn-default form-control ui-select-toggle']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
        time.sleep(0.5)
        toggle.click()
        time.sleep(0.5)

        # Clica na opção "Autorizada"
        opcao_autorizada = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Autorizada']"))
        )
        driver.execute_script("arguments[0].click();", opcao_autorizada)
        print("  → Status definido como 'Autorizada'.")
    except Exception as e:
        print(f"  ⚠️ Não foi possível definir o status: {e}")
        # Continua mesmo assim (o sistema pode aceitar vazio = "Autorizada")

    time.sleep(1)

    # --- Clica em 'Consultar' com retry ---
    max_tentativas = 3
    tabela_xpath = '//*[@id="conteudo_central"]/div/div/div/div[3]/div[2]'
    for tentativa in range(1, max_tentativas + 1):
        print(f"\nTentativa {tentativa}: clicando em 'Consultar'...")

        # Fecha popup de migração (pode reaparecer!)
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "div.mfe-migration-modal button.close[ng-click='$hide()']")
            if close_btn.is_displayed():
                close_btn.click()
                time.sleep(1)
        except:
            pass

        # Clica em Consultar
        btn_consultar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='find()' and contains(text(), 'Consultar')]"))
        )
        btn_consultar.click()
        time.sleep(2)

        # Verifica se o popup de DANFE com "CNPJ: Não informado" apareceu
        try:
            cnpj_nao_informado = driver.find_element(
                By.XPATH, "//div[@class='modal-body']//div[contains(text(), 'CNPJ: Não informado')]"
            )
            if cnpj_nao_informado.is_displayed():
                print("⚠️ Detectado 'CNPJ: Não informado'. Recarregando página...")
                driver.refresh()
                time.sleep(3)
                continue
        except:
            pass

        # Aguarda tabela ou mensagem de "nenhum registro"
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='table-search-coupons'] | //div[contains(text(), 'Nenhum registro encontrado')]"))
            )
            print("✅ Tabela de resultados carregada com sucesso!")
            break
        except Exception as e:
            if tentativa == max_tentativas:
                raise RuntimeError("Falha ao carregar a tabela após múltiplas tentativas.")
            time.sleep(2)

    time.sleep(2)
    print("✅ Filtro aplicado com sucesso!")