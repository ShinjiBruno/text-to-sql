import os
from dotenv import load_dotenv
import database
import llm

load_dotenv()

def print_formatted_table(columns, rows):
    if not rows:
        print("\nA consulta não retornou nenhum registro.")
        return
        
    col_widths = [len(str(col)) for col in columns]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    
    print(separator)
    header_str = " | ".join([f"{str(col).ljust(col_widths[i])}" for i, col in enumerate(columns)])
    print(f"| {header_str} |")
    print(separator)
    
    for row in rows:
        row_str = " | ".join([f"{str(val).ljust(col_widths[i])}" for i, val in enumerate(row)])
        print(f"| {row_str} |")
    print(separator)

def mainLoop():
    print("Inicializando Ferramenta Text-to-SQL")
    
    print("Mapeando tabelas e colunas do banco de dados...")
    schema = database.fetch_schema()
    
    if not schema:
        print("Interrompendo execução devido a falhas na comunicação com o banco de dados.")
        return
        
    print("\n--- Esquema do Banco de Dados Carregado ---")
    print(schema)
    print("-------------------------------------------")
    
    while True:
        print("\nDigite sua consulta em linguagem natural (ou '/exit' para sair):")
        prompt = input("> ").strip()
        
        if not prompt:
            continue
            
        if prompt.lower() == "/exit":
            print("Encerrando aplicação...")
            break
            
        print("\n[1/2] Traduzindo comando...")
        try:
            sql_query = llm.generate_sql(prompt, schema)
            
            if sql_query.upper() == "ERROR":
                print("Essa pergunta não pode ser respondida com as tabelas disponíveis.")
                continue
                
            print(f"SQL Gerado com sucesso:\n{sql_query}\n")
            
            print("[2/2] Executando comando no MySQL Docker...")
            columns, results = database.execute_query(sql_query)
            
            if columns is None:
                print(results)
            else:
                print("\nResultado da Consulta")
                print_formatted_table(columns, results)
                
        except Exception as e:
            print(f"Ocorreu um erro no processamento: {e}")

if __name__ == "__main__":
    mainLoop()