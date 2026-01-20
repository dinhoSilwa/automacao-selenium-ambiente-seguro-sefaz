# download.py

import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def aguardar_download_completo(pasta: Path, timeout: int = 60) -> Path:
    """
    Aguarda até que um arquivo .xml seja baixado completamente.
    Retorna o caminho do arquivo baixado.
    """
    inicio = time.time()
    while time.time() - inicio < timeout:
        arquivos = list(pasta.glob("*.xml"))
        crdownloads = list(pasta.glob("*.crdownload"))
        
        if crdownloads:
            time.sleep(1)
            continue
            
        if arquivos:
            # Retorna o arquivo mais recente
            return max(arquivos, key=os.path.getctime)
            
        time.sleep(1)
        
    raise TimeoutError(f"Download não concluído em {timeout} segundos")

def baixar_xmls_por_chaves(driver, chaves, download_dir="downloads"):
    """
    Para cada chave NFC-e:
      - Clica no link da chave (abre popup de DANFE)
      - Verifica se há "CNPJ: Não informado"
      - Clica em "Download XML"
      - Aguarda download
      - Fecha o popup
    """
    wait = WebDriverWait(driver, 30)
    download_path = Path(download_dir).resolve()
    
    if not chaves:
        print("⚠️ Nenhuma chave para baixar.")
        return

    print(f"\nIniciando download de {len(chaves)} XMLs...")

    for i, chave in enumerate(chaves, 1):
        print(f"\n[{i}/{len(chaves)}] Processando chave: {chave}")

        try:
            # Localiza e clica na chave
            link_chave = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[@ng-click][text()='{chave}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link_chave)
            time.sleep(0.5)
            link_chave.click()

            # Aguarda popup de DANFE abrir
            wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='modal-content']//h4[contains(text(), 'DANFE')]"))
            )
            time.sleep(1)

            # Verifica "CNPJ: Não informado"
            try:
                cnpj_nao_informado = driver.find_element(
                    By.XPATH, "//div[@class='modal-body']//div[contains(text(), 'CNPJ: Não informado')]"
                )
                if cnpj_nao_informado.is_displayed():
                    print(f"  ❌ CNPJ não informado para chave {chave}. Pulando...")
                    # Fecha popup e continua
                    close_btn = driver.find_element(By.XPATH, "//button[@class='close'][@ng-click='$hide()']")
                    close_btn.click()
                    time.sleep(1)
                    continue
            except:
                pass  # OK, CNPJ está informado

            # Snapshot dos arquivos antes do download
            arquivos_antes = set(download_path.glob("*.xml"))

            # Clica em "Download XML"
            btn_download = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='downloadXML()' and contains(text(), 'Download XML')]"))
            )
            btn_download.click()
            print(f"  → Download solicitado.")

            # Aguarda download completo
            arquivo_xml = aguardar_download_completo(download_path)
            nome_esperado = f"NFCe-{chave}.xml"
            novo_caminho = download_path / nome_esperado

            # Renomeia para padrão consistente
            if arquivo_xml.name != nome_esperado:
                arquivo_xml.rename(novo_caminho)
                print(f"  → Arquivo renomeado para: {nome_esperado}")
            else:
                novo_caminho = arquivo_xml

            # Fecha o popup
            close_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='close'][@ng-click='$hide()']"))
            )
            close_btn.click()
            time.sleep(1)

            print(f"  ✅ Download concluído: {nome_esperado}")

        except Exception as e:
            print(f"  ❌ Erro ao processar chave {chave}: {e}")
            # Tenta fechar popup mesmo em erro
            try:
                close_btn = driver.find_element(By.XPATH, "//button[@class='close'][@ng-click='$hide()']")
                close_btn.click()
                time.sleep(1)
            except:
                pass

    print(f"\n✅ Todos os XMLs foram salvos em: {download_path}")