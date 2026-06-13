import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Cria e retorna uma conexão com o MySQL usando as variáveis do .env."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_schema():
    """
    Mapeia dinamicamente a lista de tabelas e campos do banco de dados
    para alimentar a System Message da LLM.
    """
    schema_info = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        if not tables:
            return "Nenhuma tabela encontrada no banco de dados."
            
        for (table_name,) in tables:
            schema_info.append(f"Tabela: {table_name}")
            
            cursor.execute(f"DESCRIBE `{table_name}`;")
            columns = cursor.fetchall()
            cols_desc = []
            for col in columns:
                col_name = col[0]
                col_type = col[1]
                cols_desc.append(f"{col_name} ({col_type})")
                
            schema_info.append("  Colunas: " + ", ".join(cols_desc))
        
        cursor.close()
        conn.close()
        return "\n".join(schema_info)
        
    except Error as e:
        print(f"\n[Erro de Conexão] Falha ao ler o esquema do MySQL: {e}")
        return None

def execute_query(sql_query):
    """Executa a query gerada pela IA e retorna (colunas, linhas_de_dados)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return columns, results
        else:
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            conn.close()
            return None, f"Comando executado com sucesso. Linhas afetadas: {rowcount}"
            
    except Error as e:
        return None, f"Erro de sintaxe/execução no MySQL: {e}"