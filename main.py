# main.py

from login import realizar_login_sefaz
from filtro import aplicar_filtro_mfe

if __name__ == "__main__":
    driver = realizar_login_sefaz()
    try:
        aplicar_filtro_mfe(driver)
        input("\n>>> Filtro aplicado. Pressione ENTER para encerrar e fechar o navegador...\n")
    finally:
        driver.quit()