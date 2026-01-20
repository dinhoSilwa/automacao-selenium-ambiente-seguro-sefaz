# download.py

import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def baixar_xmls_por_chaves(driver, chaves, download_dir=None):
    """
    Para cada chave NFC-e:
      - Clica no link da chave (abre popup)
      - Clica em "Download XML"
      - Fecha o popup
    """
    wait = WebDriverWait(driver, 30)

    if not chaves:
        print("⚠️ Nenhuma chave para baixar.")
        return

    print(f"\nIniciando download de {len(chaves)} XMLs...")

    for i, chave in enumerate(chaves, 1):
        print(f"\n[{i}/{len(chaves)}] Processando chave: {chave}")

        try:
            # Localiza o link da chave (pode mudar de posição após paginação)
            link_chave = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[@ng-click][text()='{chave}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_chave)
            time.sleep(0.5)
            link_chave.click()

            # Aguarda popup abrir
            wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='modal-content']//h4[contains(text(), 'Detalhes')]"))
            )
            time.sleep(1)

            # Clica em "Download XML"
            btn_download = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='downloadXML()' and contains(text(), 'Download XML')]"))
            )
            btn_download.click()
            print(f"  → XML de {chave} solicitado.")

            # Aguarda download (ajuste conforme necessário)
            time.sleep(3)

            # Fecha o popup
            close_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-content']//button[@class='close'][@ng-click='$hide()']"))
            )
            close_btn.click()
            time.sleep(1)

        except Exception as e:
            print(f"  ❌ Erro ao processar chave {chave}: {e}")
            # Tenta fechar popup mesmo em erro
            try:
                driver.find_element(By.XPATH, "//button[@class='close'][@ng-click='$hide()']").click()
                time.sleep(1)
            except:
                pass

    print("\n✅ Todos os XMLs solicitados com sucesso!")