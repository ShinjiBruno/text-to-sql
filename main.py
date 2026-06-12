import os
from openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

def mainLoop():
    prompt = ""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "Erro: OPENROUTER_API_KEY nao foi encontrada."
        )
        return

    with OpenRouter(api_key=api_key) as client:
        while True:
            print("\nDigite uma mensagem (ou '/exit' para sair): ")
            prompt = input()

            if prompt.strip() == "/exit":
                print("Saindo...")
                break

            response = client.chat.send(
                model="openrouter/owl-alpha",
                x_open_router_metadata="enabled",
                max_tokens=1000,
                stream=True,
                temperature=0.4,
                messages=[
                    {
                        "content": "Você é um Assistente text-to-sql que converte a linguagem natural do usuário em SQL. OBRIGATORIAMENTE deve responder somente às mensagens relacionadas às queries, caso contrário responda somente 'Assunto não relacionado às consultas. Reformule a mensagem por gentileza'",
                        "role": "system",
                    },
                    {"content": prompt, "role": "user"},
                ],
            )

            with response as event_stream:
                for event in event_stream:
                    print(event.choices[0].delta.content, end="", flush=True)
                print()


if __name__ == "__main__":
    mainLoop()
