# coletar_chaves.py

import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def coletar_todas_chaves_nfe(driver, output_file="chaves_clicadas.txt"):
    """
    Coleta TODAS as chaves NFC-e de TODAS as páginas da tabela de resultados.
    Usa seletores resilientes e verifica explicitamente a presença de elementos.
    """
    wait = WebDriverWait(driver, 30)
    todas_chaves = set()
    pagina_atual = 1

    print("🔍 Iniciando coleta de chaves em todas as páginas...")

    while True:
        print(f"\n➡️  Processando página {pagina_atual}...")

        # Verifica se há mensagem de "Nenhum registro encontrado"
        try:
            no_data = driver.find_element(
                By.XPATH, "//div[contains(@class, 'well well-lg') and contains(text(), 'Nenhum registro encontrado')]"
            )
            if no_data.is_displayed():
                print("⚠️ Nenhum registro encontrado na consulta.")
                break
        except:
            pass  # OK, há dados

        # Clica no botão "100" (se existir e não estiver ativo)
        try:
            btn_100 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='100']]")))
            # Verifica se já está ativo
            if "active" not in btn_100.get_attribute("class"): # type: ignore
                print("  → Clicando em '100' para expandir a tabela...")
                driver.execute_script("arguments[0].click();", btn_100)
                time.sleep(2)
        except Exception as e:
            print(f"  ⚠️ Botão '100' não encontrado ou já ativo: {e}")

        # Coleta chaves da página atual
        try:
            chave_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//td[@data-title-text='Chave NFCe']//a[@ng-click and @href='' and text()]")
                )
            )
            chaves_pagina = []
            for elem in chave_elements:
                chave = elem.text.strip()
                if len(chave) == 44 and chave.isdigit():
                    chaves_pagina.append(chave)
            print(f"  → Encontradas {len(chaves_pagina)} chaves válidas nesta página.")
            todas_chaves.update(chaves_pagina)
        except Exception as e:
            print(f"  ⚠️ Erro ao coletar chaves: {e}")
            break

        # Verifica se existe próxima página
        try:
            next_button = driver.find_element(
                By.XPATH,
                "//ul[contains(@class, 'pagination') and contains(@class, 'ng-table-pagination')]//li[not(contains(@class, 'disabled'))]//a[text()='»']",
            )
            if next_button.is_displayed() and next_button.is_enabled():
                print("  → Indo para a próxima página...")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
                pagina_atual += 1
                continue
            else:
                print("  → Última página (botão '»' desabilitado).")
                break
        except Exception as e:
            print("  → Nenhuma próxima página encontrada (fim da paginação).")
            break

    # Salva todas as chaves
    chaves_lista = sorted(list(todas_chaves))
    mode = "a" if os.path.exists(output_file) else "w"
    with open(output_file, mode, encoding="utf-8") as f:
        for chave in chaves_lista:
            f.write(chave + "\n")

    print(f"\n✅ Total de {len(chaves_lista)} chaves coletadas e salvas em '{output_file}'.")
    return chaves_lista
