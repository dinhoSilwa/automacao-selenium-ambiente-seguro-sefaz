# main.py

from login import realizar_login_sefaz
from filtro import aplicar_filtro_mfe
from coletar_chaves import coletar_chaves_nfe
from download import baixar_xmls_por_chaves

if __name__ == "__main__":
    driver = realizar_login_sefaz()
    try:
        aplicar_filtro_mfe(driver)
        chaves = coletar_chaves_nfe(driver)
        baixar_xmls_por_chaves(driver, chaves)
        input("\n>>> Processo concluído. Pressione ENTER para encerrar...\n")
    finally:
        driver.quit()
        