# Text-to-SQL

Ferramenta de linha de comando que traduz consultas em linguagem natural para SQL usando LLM local (via Ollama) e executa no MySQL.

## Como funciona

1. O script mapeia automaticamente o esquema do banco (tabelas e colunas).
2. Envia o esquema + sua pergunta em linguagem natural para a LLM.
3. A LLM gera a query SQL correspondente.
4. A query é executada no MySQL e o resultado é exibido no terminal.

## Pré-requisitos

- **Python 3.10+**
- **MySQL** rodando e acessível (local ou remoto)
- **Ollama** instalado e rodando

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/ShinjiBruno/text-to-sql.git
cd text-to-sql
```

### 2. Criar e ativar o ambiente virtual

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar e rodar o Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

**macOS / Windows:** baixe em [ollama.com](https://ollama.com) e abra o aplicativo.

Com o Ollama rodando, baixe o modelo usado pelo projeto:

```bash
ollama pull qwen2.5-coder:3b
```

### 5. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha com os dados do seu banco:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
```

> **Nota:** o Ollama roda localmente em `http://localhost:11434` por padrão. Não precisa de chave API nem configuração extra — o projeto já aponta para lá automaticamente.

## Uso

Com o ambiente virtual ativado e o Ollama rodando:

```bash
python main.py
```

O programa vai carregar o esquema do banco e entrar no modo interativo. Digite suas perguntas em linguagem natural. Ex.:

```
> Quantos clientes fizeram pedido em 2024?

[1/2] Traduzindo comando...
SQL Gerado com sucesso:
SELECT COUNT(DISTINCT c.id) FROM clientes c JOIN pedidos p ON c.id = p.cliente_id WHERE YEAR(p.data) = 2024

[2/2] Executando comando no MySQL Docker...

Resultado da Consulta
+-------+
| count |
+-------+
|   42  |
+-------+
```

Para sair, digite `/exit`.

## Alternativa: Ollama via Docker

Se preferir rodar o Ollama em container (sem instalar localmente):

```bash
docker compose up -d
```

Isso sobe o Ollama na porta `11434` e já faz o pull do modelo `qwen2.5-coder:3b` automaticamente. Os dados do modelo ficam persistidos em `./ollama_data/`.

## Trocar o modelo LLM

Edite `llm.py` e altere o valor de `model` na função `generate_sql_ollama`:

```python
model='qwen2.5-coder:3b'
```


