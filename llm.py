import os
from openrouter import OpenRouter
from ollama import Client

def generate_sql(user_prompt, database_schema):
    """Envia o esquema e o pedido do usuário para obter estritamente uma query SQL."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("A chave OPENROUTER_API_KEY não foi definida no arquivo .env.")
        
    system_instruction = f"""Você é um tradutor especializado em converter linguagem natural em consultas SQL válidas para o MySQL.
    
Aqui está o esquema atual do banco de dados (tabelas e colunas disponíveis):
{database_schema}

REGRAS CRÍTICAS E OBRIGATÓRIAS:
1. Responda APENAS com o código SQL puro e limpo, pronto para ser executado diretamente pelo driver do MySQL.
2. NÃO adicione explicações textuais, introduções, saudações ou comentários.
3. NÃO envolva a resposta em blocos de marcação Markdown (É PROIBIDO usar ```sql ou ```).
4. Se o pedido do usuário não puder ser transformado em uma query válida usando o esquema fornecido, responda estritamente com a palavra: ERROR
"""

    with OpenRouter(api_key=api_key) as client:
        response = client.chat.send(
            model="openrouter/owl-alpha",
            max_tokens=1000,
            stream=False,                
            temperature=0.4,              
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        sql_result = response.choices[0].message.content.strip()
        
        if sql_result.startswith("```"):
            sql_result = sql_result.replace("```sql", "").replace("```", "").strip()
            
        return sql_result


def generate_sql_ollama(user_prompt, database_schema):
    client = Client(host='http://localhost:11434')
    system_instruction =  f"""Você é um tradutor especializado em converter linguagem natural em consultas SQL válidas para o MySQL. 
Aqui está o esquema atual do banco de dados (tabelas e colunas disponíveis):
{database_schema}

REGRAS CRÍTICAS E OBRIGATÓRIAS:
1. Responda APENAS com o código SQL puro e limpo, pronto para ser executado diretamente pelo driver do MySQL.
2. NÃO adicione explicações textuais, introduções, saudações ou comentários.
3. NÃO envolva a resposta em blocos de marcação Markdown (É PROIBIDO usar ```sql ou ```).
4. Se o pedido do usuário não puder ser transformado em uma query válida usando o esquema fornecido, responda estritamente com a palavra: ERROR
"""

    response = client.chat(
        model='qwen2.5-coder:3b',
        messages=[
            {"role":"system", "content": system_instruction},
            {"role":"user", "content": user_prompt}
        ]
    )
    sql_result = response['message']['content'].strip()
    return sql_result

