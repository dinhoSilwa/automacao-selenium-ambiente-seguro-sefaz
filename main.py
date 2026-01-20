# main.py

from login import realizar_login_sefaz
from filtro import aplicar_filtro_mfe
import os

if __name__ == "__main__":
    driver = None
    try:
        driver = realizar_login_sefaz()
        aplicar_filtro_mfe(driver)
        input("\n>>> Filtro aplicado. Pressione ENTER para encerrar...\n")
    except Exception as e:
        if driver:
            screenshot_path = os.path.join(os.getcwd(), "erro_screenshot.png")
            driver.save_screenshot(screenshot_path)
            print(f"\n❌ Erro! Screenshot salvo em: {screenshot_path}")
        raise
    finally:
        if driver:
            driver.quit()