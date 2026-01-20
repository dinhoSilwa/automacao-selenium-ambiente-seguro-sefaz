# Sistema de Automação Selenium - Ambiente Seguro SEFAZ Ceará

## Descrição do Projeto

Este projeto implementa uma solução de automação específica para interação com o sistema **Ambiente Seguro da SEFAZ Ceará**. A aplicação utiliza Selenium WebDriver para automatizar processos de login e aplicação de filtros no sistema de emissão de documentos fiscais eletrônicos.

**Atenção**: Esta solução foi desenvolvida especificamente para o portal da SEFAZ Ceará (https://www.sefaz.ce.gov.br/ambiente-seguro/). Para outros estados, pode ser necessário ajustar o código devido às diferenças no layout e estrutura dos sites das respectivas secretarias.

## Arquitetura do Projeto

### Estrutura de Arquivos
```
SELENIUM_AMBIENTE_SEGURO/
├── main.py              # Ponto de entrada principal
├── login.py            # Módulo de autenticação no Ambiente Seguro
├── filtro.py           # Módulo de aplicação de filtros para MFE
└── requirements.txt    # Dependências do projeto
```

### Fluxo de Execução
1. **Autenticação**: Login no Ambiente Seguro da SEFAZ Ceará através do módulo `login.py`
2. **Aplicação de Filtros**: Configuração de parâmetros específicos para MFE via `filtro.py`
3. **Gerenciamento de Sessão**: Controle seguro da navegação web
4. **Tratamento de Erros**: Captura de screenshots em caso de falhas

## Funcionalidades Principais

### Módulo de Login (`login.py`)
- Autenticação no Ambiente Seguro da SEFAZ Ceará
- Navegação controlada para páginas protegidas
- Gerenciamento de credenciais seguras através de variáveis de ambiente

### Módulo de Filtros (`filtro.py`)
- Aplicação de filtros específicos para MFE (Manifesto Fiscal Eletrônico)
- Configuração de parâmetros de busca e filtragem
- Manipulação de elementos de formulário web específicos do portal cearense

### Módulo Principal (`main.py`)
- Orquestração dos processos de automação
- Tratamento robusto de exceções e erros
- Captura automática de screenshots em caso de falhas
- Gerenciamento do ciclo de vida do WebDriver

## Pré-requisitos

### Dependências (requirements.txt)
```txt
selenium>=4.20.0          # Framework de automação web
webdriver-manager>=4.0.0  # Gerenciamento automático de drivers
python-dotenv>=1.0.0      # Gerenciamento de variáveis de ambiente
```

### Configuração do Ambiente
1. Python 3.8 ou superior
2. Conexão com internet para download dos drivers e acesso ao sistema
3. Credenciais válidas para acesso ao Ambiente Seguro da SEFAZ Ceará
4. Acesso autorizado ao sistema (certificado digital ou credenciais)

## Instalação e Execução

### Passo 1: Configuração do Ambiente
```bash
# Navegue até o diretório do projeto
cd c:\Projetcs\BACK\AUTO\SELENIUM_AMBIENTE_SEGURO

# Crie um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Configuração das Credenciais
```bash
# Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
USUARIO_SEFAZ=seu_usuario
SENHA_SEFAZ=sua_senha
# URL específica do Ambiente Seguro da SEFAZ Ceará
URL_SISTEMA=https://www.sefaz.ce.gov.br/ambiente-seguro/
```

### Passo 3: Execução
```bash
# Execute o sistema principal
python main.py
```

## Características Técnicas

### Gerenciamento de Drivers
- Uso de `webdriver-manager` para atualização automática dos drivers
- Suporte a múltiplos navegadores (configurável)
- Gerenciamento automático de versões de driver

### Tratamento de Erros
- Captura de screenshots em caso de exceções (salvo como `erro_screenshot.png`)
- Logs de erro detalhados no console
- Encerramento seguro dos recursos do WebDriver

### Segurança
- Variáveis sensíveis armazenadas em arquivo `.env`
- Sessões web devidamente finalizadas após cada execução
- Navegação isolada por execução

## Considerações Importantes

### Especificidade do Sistema
Esta solução foi desenvolvida exclusivamente para o **Ambiente Seguro da SEFAZ Ceará**. Para outros estados, o código pode não funcionar devido a:

1. Diferenças no layout e estrutura HTML
2. Variações nos fluxos de autenticação
3. Elementos de interface distintos
4. URLs e endpoints específicos de cada estado

### Codificação de Arquivos
Os arquivos `.py` devem utilizar codificação UTF-8. Caso encontre erros de decodificação (como `charmap codec can't decode byte`), verifique e ajuste a codificação dos arquivos.

### Requisitos do Ambiente Seguro
O sistema opera em ambiente com:
- Certificado digital ou autenticação forte
- Políticas de segurança específicas da SEFAZ
- Restrições de acesso por IP e horário
- Validações de segurança do navegador

### Responsabilidade de Uso
- Utilize apenas com credenciais próprias e autorizadas
- Mantenha as informações de acesso em arquivos seguros (.env)
- Respeite os termos de uso do Ambiente Seguro da SEFAZ Ceará
- Considere as implicações legais da automação em sistemas governamentais

## Possíveis Melhorias Futuras

1. **Configuração Modular**: Adicionar arquivo de configuração para ajustes específicos
2. **Logs Estruturados**: Implementar sistema de logging com diferentes níveis
3. **Suporte Multi-estado**: Modularizar para permitir adaptação a outros estados
4. **Interface de Configuração**: Adicionar CLI para configuração dinâmica
5. **Testes Automatizados**: Implementar testes unitários e de integração
6. **Monitoramento**: Adicionar métricas e alertas de execução

## Licença e Uso

Este projeto é destinado para uso interno e em ambientes controlados. Certifique-se de possuir autorização adequada para automatizar processos no Ambiente Seguro da SEFAZ Ceará e esteja ciente das políticas de uso do sistema.

**Aviso Legal**: O uso desta ferramenta deve estar em conformidade com os termos de serviço da SEFAZ Ceará. O desenvolvedor não se responsabiliza por uso indevido ou violação de termos de serviço.