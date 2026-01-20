# main.py

from coletar_chaves import coletar_todas_chaves_nfe  # ← nova função
from download import baixar_xmls_por_chaves
from filtro import aplicar_filtro_mfe
from login import realizar_login_sefaz

if __name__ == "__main__":
    driver = realizar_login_sefaz()
    try:
        aplicar_filtro_mfe(driver)
        chaves = coletar_todas_chaves_nfe(driver)  # ← coleta todas as páginas
        baixar_xmls_por_chaves(driver, chaves)
        input("\n>>> Processo concluído. Pressione ENTER para encerrar...\n")
    finally:
        driver.quit()
