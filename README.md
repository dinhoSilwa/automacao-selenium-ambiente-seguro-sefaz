# Sistema de Automação Selenium - Ambiente Seguro SEFAZ Ceará

## Descrição do Projeto

Este projeto implementa uma solução de automação específica para interação com o sistema **Ambiente Seguro da SEFAZ Ceará**. A aplicação utiliza Selenium WebDriver para automatizar processos de login e aplicação de filtros no sistema de emissão de documentos fiscais eletrônicos.

**Atenção**: Esta solução foi desenvolvida especificamente para o portal da SEFAZ Ceará (https://servicos.sefaz.ce.gov.br/internet/acessoseguro/servicosenha/logarusuario/login.asp). Para outros estados, pode ser necessário ajustar o código devido às diferenças no layout e estrutura dos sites das respectivas secretarias.

## Arquitetura do Projeto

### Estrutura de Arquivos
```
SELENIUM_AMBIENTE_SEGURO/
├── main.py              # Ponto de entrada principal
├── login.py            # Módulo de autenticação no Ambiente Seguro
├── filtro.py           # Módulo de aplicação de filtros para MFE
├── requirements.txt    # Dependências do projeto
└── .env.exemplo       # Template de configuração
```

### Fluxo de Execução
1. **Autenticação**: Login no Ambiente Seguro da SEFAZ Ceará através do módulo `login.py`
2. **Aplicação de Filtros**: Configuração de parâmetros específicos para MFE via `filtro.py`
3. **Gerenciamento de Sessão**: Controle seguro da navegação web
4. **Tratamento de Erros**: Captura de screenshots em caso de falhas

## Configuração do Ambiente

### Arquivo .env.exemplo
Renomeie o arquivo `.env.exemplo` para `.env` e configure com suas informações:

```env
# === Autenticação SEFAZ ===
SEFAZ_URL=https://servicos.sefaz.ce.gov.br/internet/acessoseguro/servicosenha/logarusuario/login.asp
CPF=00000000000
SENHA=SUASENHA_AQUI

# === Variáveis de Filtro ===
CGF=00000000
START=01/08/2025
TIMESTART=05:00
END=31/08/2025
TIMEEND=23:00
```

### Explicação das Variáveis:

#### **Autenticação SEFAZ:**
- `SEFAZ_URL`: URL específica do login do Ambiente Seguro da SEFAZ Ceará
- `CPF`: CPF do usuário autorizado (apenas números, sem pontos ou traços)
- `SENHA`: Senha de acesso ao sistema

#### **Variáveis de Filtro:**
- `CGF`: **Código Estadual da Empresa** - Identificador único da empresa no estado do Ceará
- `START`: Data inicial para filtro (formato DD/MM/YYYY)
- `TIMESTART`: Hora inicial para filtro (formato HH:MM)
- `END`: Data final para filtro (formato DD/MM/YYYY)
- `TIMEEND`: Hora final para filtro (formato HH:MM)

**Nota sobre CGF**: O Código Estadual da Empresa (CGF) é um identificador único atribuído pela SEFAZ Ceará para cada empresa cadastrada no estado. Este código é utilizado para filtrar as operações específicas da empresa no sistema.

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
4. Acesso autorizado ao sistema com CPF e senha cadastrados
5. CGF (Código Estadual da Empresa) válido para consulta

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
# Copie o arquivo de exemplo
copy .env.exemplo .env

# Edite o arquivo .env com suas informações:
# - Substitua 00000000000 pelo seu CPF
# - Substitua SUASENHA_AQUI pela sua senha
# - Substitua 00000000 pelo CGF da empresa
# - Ajuste as datas e horários conforme necessário
```

### Passo 3: Execução
```bash
# Execute o sistema principal
python main.py
```

## Funcionalidades Principais

### Módulo de Login (`login.py`)
- Autenticação no Ambiente Seguro da SEFAZ Ceará utilizando CPF e senha
- Navegação controlada para páginas protegidas
- Gerenciamento de sessão web com credenciais do arquivo .env

### Módulo de Filtros (`filtro.py`)
- Aplicação de filtros específicos para MFE (Manifesto Fiscal Eletrônico)
- Configuração automática de datas e horários baseados no arquivo .env
- Filtragem por CGF (Código Estadual da Empresa) específico
- Manipulação de elementos de formulário web específicos do portal cearense

### Módulo Principal (`main.py`)
- Orquestração dos processos de automação
- Tratamento robusto de exceções e erros
- Captura automática de screenshots em caso de falhas (salvo como `erro_screenshot.png`)
- Gerenciamento do ciclo de vida do WebDriver

## Características Técnicas

### Gerenciamento de Drivers
- Uso de `webdriver-manager` para atualização automática dos drivers
- Suporte a múltiplos navegadores (configurável)
- Gerenciamento automático de versões de driver

### Tratamento de Erros
- Captura de screenshots em caso de exceções
- Logs de erro detalhados no console
- Encerramento seguro dos recursos do WebDriver

### Segurança
- Variáveis sensíveis armazenadas em arquivo `.env` (não versionado)
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
- Autenticação por CPF e senha específicos do Ceará
- Políticas de segurança específicas da SEFAZ Ceará
- Restrições de acesso por IP e horário
- Validações de segurança do navegador

### Sobre o CGF (Código Estadual da Empresa)
- Cada empresa possui um CGF único no estado do Ceará
- Este código é utilizado para identificar a empresa em todas as operações fiscais
- O CGF deve ser obtido através do cadastro na SEFAZ Ceará
- Não confundir com CNPJ - são identificadores diferentes

### Responsabilidade de Uso
- Utilize apenas com credenciais próprias e autorizadas
- Mantenha as informações de acesso em arquivo .env seguro (não compartilhe)
- Respeite os termos de uso do Ambiente Seguro da SEFAZ Ceará
- Considere as implicações legais da automação em sistemas governamentais
- Use apenas para fins legítimos e autorizados

## Possíveis Melhorias Futuras

1. **Validação de Datas**: Adicionar verificação automática de formato de datas
2. **Logs Estruturados**: Implementar sistema de logging com diferentes níveis
3. **Suporte Multi-estado**: Modularizar para permitir adaptação a outros estados
4. **Interface de Configuração**: Adicionar CLI para configuração dinâmica
5. **Testes Automatizados**: Implementar testes unitários e de integração
6. **Monitoramento**: Adicionar métricas e alertas de execução
7. **Backup de Configuração**: Sistema de backup automático de configurações

## Solução de Problemas

### Erros Comuns:

1. **Erro de decodificação CP1252**:
   ```bash
   # Converta os arquivos para UTF-8
   python -c "open('arquivo.py', 'r', encoding='utf-8').write(open('arquivo.py', 'r', encoding='cp1252', errors='ignore').read())"
   ```

2. **Credenciais inválidas**:
   - Verifique se o CPF e senha estão corretos no arquivo .env
   - Confirme se possui acesso ao Ambiente Seguro da SEFAZ Ceará

3. **CGF não encontrado**:
   - Verifique se o Código Estadual da Empresa está correto
   - Confirme se a empresa está ativa no cadastro da SEFAZ Ceará

## Licença e Uso

Este projeto é destinado para uso interno e em ambientes controlados. Certifique-se de possuir autorização adequada para automatizar processos no Ambiente Seguro da SEFAZ Ceará e esteja ciente das políticas de uso do sistema.

**Aviso Legal**: O uso desta ferramenta deve estar em conformidade com os termos de serviço da SEFAZ Ceará. O desenvolvedor não se responsabiliza por uso indevido ou violação de termos de serviço. Mantenha suas credenciais em segurança e não as compartilhe.