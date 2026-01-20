# coletar_chaves.py

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def coletar_chaves_nfe(driver, output_file="chaves_clicadas.txt"):
    """
    Coleta todas as chaves NFC-e da tabela após a consulta.
    Salva em um arquivo de texto (append mode).
    Retorna a lista de chaves.
    """
    wait = WebDriverWait(driver, 30)

    print("Verificando se há resultado na consulta...")
    
    # Verifica se aparece "CNPJ: Não informado"
    try:
        cnpj_nao_informado = driver.find_element(By.XPATH, "//div[contains(@class, 'ng-binding') and contains(text(), 'CNPJ: Não informado')]")
        if cnpj_nao_informado.is_displayed():
            print("❌ Erro crítico: 'CNPJ: Não informado' detectado. Encerrando imediatamente.")
            driver.quit()
            exit(1)
    except:
        pass  # OK, CNPJ está informado

    # Aguarda tabela carregar
    table_container = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@ng-show='tableParams' and contains(., 'RESULTADOS DE CONSULTA')]"))
    )

    # Verifica se há registros
    try:
        no_data = driver.find_element(By.XPATH, "//div[contains(@class, 'well well-lg') and contains(text(), 'Nenhum registro encontrado')]")
        if no_data.is_displayed():
            print("⚠️ Nenhum registro encontrado na consulta.")
            return []
    except:
        pass  # Há dados

    # Clica no botão "100" para exibir mais resultados por página
    try:
        btn_100 = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-default' and .//span[text()='100']]"))
        )
        print("Clicando em '100' para expandir a tabela...")
        btn_100.click()
        time.sleep(2)
    except Exception as e:
        print("⚠️ Botão '100' não encontrado ou já selecionado.")

    # Coleta todas as chaves NFC-e
    print("Extraindo chaves NFC-e da tabela...")
    chave_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//td[@data-title-text='Chave NFCe']/a[@ng-click]"))
    )

    chaves = []
    for elem in chave_elements:
        chave = elem.text.strip()
        if chave and len(chave) == 44:  # Chave NFC-e tem 44 dígitos
            chaves.append(chave)
            print(f"  → {chave}")

    # Salva em arquivo (modo append)
    mode = "a" if os.path.exists(output_file) else "w"
    with open(output_file, mode, encoding="utf-8") as f:
        for chave in chaves:
            f.write(chave + "\n")

    print(f"\n✅ {len(chaves)} chaves coletadas e salvas em '{output_file}'.")
    return chaves