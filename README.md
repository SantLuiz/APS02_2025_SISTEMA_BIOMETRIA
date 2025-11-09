![Linguagem](https://img.shields.io/badge/Linguagem-Python-green) ![Status](https://img.shields.io/badge/Status-Finalizado-green)

# APS02_2025_SISTEMA_BIOMETRIA

Sistema de identificação e autenticação biométrica (trabalho acadêmico)

Uma implementação simples de um sistema biométrico para identificação/autenticação por impressões digitais. O projeto inclui código para gerenciar usuários, realizar validação de impressões digitais e uma interface básica que pede o nome do usuário e um arquivo BMP contendo a impressão.

Documentação das classes (gerada com pdoc) está disponível em `docs/pdoc`.

Fonte dos dados de impressão (exemplo usado no dataset): https://www.kaggle.com/datasets/ruizgara/socofing

## Requisitos

- Python 3.8+
- pip
- Dependências do projeto listadas em `requirements.txt`

## Setup — instruções por sistema

Crie e ative um ambiente virtual e instale as dependências. Escolha o bloco correspondente ao seu sistema e shell.

### Linux

#### Bash

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

#### Fish

```fish
$ python3 -m venv .venv
$ source .venv/bin/activate.fish
$ pip install -r requirements.txt
```

### Windows

#### CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### PowerShell

```powershell
python -m venv .venv
# Se sua política de execução bloquear scripts, execute (temporariamente) esta linha em PowerShell com privilégios do usuário:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Notas:
- Em alguns sistemas o comando do Python pode ser `python` em vez de `python3` — use o que estiver disponível no seu PATH.
- Confirme que o diretório `biometrias/` existe e contém as pastas dos usuários com imagens BMP (o repositório já inclui exemplos).

## Executando a aplicação

Inicie a aplicação com:

```bash
$ python main.py
```

Comportamento esperado:
- A interface solicitará o nome do usuário.
- Em seguida, será pedido para selecionar um arquivo `.bmp` contendo a impressão digital a validar.
- O sistema fará a checagem/validação e mostrará o conteúdo com base no nível de acesso cadastrado.

## Estrutura do repositório (visão rápida)

- `main.py` — script principal que inicia a interface/fluxo.
- `config.py` — configurações do projeto.
- `sistema_biometrico/` — pacote principal com: `biometric_sys.py`, `user_manager.py`, `acessos.py`.
- `biometrias/` — exemplos de imagens de impressão organizadas por usuário.
- `docs/pdoc/` — documentação HTML gerada (pdoc).
