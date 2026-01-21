# setup.py

import os
import sys
import re
import json
import ssl
import requests
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import importlib.util

# ───────────────────────────────────────
# 1. CONSTANTES NO TOPO (clareza)
# ───────────────────────────────────────
MIN_PYTHON = (3, 8)
REQUIRED_PKGS = ["selenium", "webdriver_manager", "python_dotenv"]
ENV_VARS = ["SEFAZ_URL", "CPF", "SENHA", "CGF", "START", "END"]
CPF_PATTERN = r"\d{11}"
CGF_PATTERN = r"\d{8}"

def _validate(value: str, pattern: str) -> bool:
    """Validação genérica com regex."""
    return bool(re.fullmatch(pattern, value or ""))

def _print_status(ok: bool, msg_ok: str, msg_fail: str):
    """Helper unificado para mensagens."""
    if ok:
        print(f"✅ {msg_ok}")
    else:
        print(f"❌ {msg_fail}")
    return ok

# ───────────────────────────────────────
# 2. CHECKS OTIMIZADOS
# ───────────────────────────────────────
def check_python_version():
    return _print_status(
        sys.version_info >= MIN_PYTHON,
        f"Python {sys.version} — OK",
        f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ necessário"
    )

def check_dependencies():
    missing = [
        p for p in REQUIRED_PKGS
        if importlib.util.find_spec(p.replace("-", "_")) is None
    ]
    return _print_status(
        not missing,
        "Dependências OK",
        f"Ausentes: {', '.join(missing)}"
    )

def check_env_file():
    env_path = find_dotenv()
    if not env_path:
        return _print_status(False, "", "Arquivo .env não encontrado")
    
    load_dotenv(env_path)
    missing_vars = [var for var in ENV_VARS if not os.getenv(var)]
    if missing_vars:
        return _print_status(False, "", f"Variáveis ausentes: {', '.join(missing_vars)}")
    
    # Validação com regex
    cpf = os.getenv("CPF")
    cgf = os.getenv("CGF")
    if not _validate(cpf, CPF_PATTERN):
        return _print_status(False, "", "CPF inválido (deve ter 11 dígitos)")
    if not _validate(cgf, CGF_PATTERN):
        return _print_status(False, "", "CGF inválido (deve ter 8 dígitos)")
    
    # Segurança: não exibe senhas
    print("✅ .env configurado (CPF=***" + cpf[-3:] + ")")
    return True

def check_sefaz_connectivity():
    try:
        load_dotenv()
        url = os.getenv("SEFAZ_URL", "https://servicos.sefaz.ce.gov.br")
        # Usa requests com stream=True (mais rápido que urllib)
        response = requests.get(url, timeout=10, stream=True, verify=False)
        return _print_status(
            response.status_code == 200,
            "Conexão com SEFAZ-CE estabelecida",
            f"Erro HTTP {response.status_code}"
        )
    except Exception as e:
        # Alerta explícito sobre SSL
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            print("⚠️  Verificação SSL desabilitada (ambiente corporativo).")
        return _print_status(False, "", f"Falha de conexão: {e}")

def check_write_permissions():
    try:
        test_file = Path("temp_setup_test.txt")
        test_file.write_text("test")
        test_file.unlink()
        return _print_status(True, "Permissões de escrita OK", "")
    except Exception as e:
        return _print_status(False, "", f"Sem permissão de escrita: {e}")

def check_chromedriver():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Silencia logs do webdriver-manager
        os.environ["WDM_LOG"] = "0"
        
        print("⏳ Verificando ChromeDriver (pode levar alguns segundos)...")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.quit()
        return _print_status(True, "ChromeDriver compatível", "")
    except Exception as e:
        return _print_status(False, "", f"Problema com ChromeDriver: {e}")

# ───────────────────────────────────────
# 3. EXECUÇÃO PRINCIPAL
# ───────────────────────────────────────
def main():
    print("🚀 Executando pré-diagnóstico do sistema...\n")
    
    checks = [
        check_python_version,
        check_dependencies,
        check_env_file,
        check_sefaz_connectivity,
        check_write_permissions,
        check_chromedriver
    ]
    
    results = [check() for check in checks]
    
    # Saída JSON para CI/CD (opcional)
    if "--json" in sys.argv:
        output = {
            "status": "success" if all(results) else "fail",
            "checks": dict(zip([c.__name__ for c in checks], results))
        }
        print(json.dumps(output))
        return 0 if all(results) else 1
    
    # Saída humana
    if all(results):
        print("\n🎉 PRÉ-DIAGNÓSTICO CONCLUÍDO COM SUCESSO!")
        return 0
    else:
        print("\n❌ CORRIJA OS ERROS ACIMA ANTES DE EXECUTAR.")
        return 1

if __name__ == "__main__":
    sys.exit(main())