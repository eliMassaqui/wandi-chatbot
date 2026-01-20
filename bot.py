import serial
import time
from openai import OpenAI

# 1. Configuração da API OpenAI (Insira sua chave válida aqui)
client = OpenAI(api_key="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")

# 2. Configuração da Serial (Sua porta COM5)
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    print("Conexão estabelecida com o Arduino na COM5.")
except Exception as e:
    print(f"Erro de conexão: {e}")
    exit()

# Instrução Estruturada para a IA (System Prompt)
# Respeitando seus pinos: Verde=2(G), Azul=3(B), Vermelho=4(R), Amarelo=5(Y)
instrucao_ia = """
Você é um tradutor de linguagem humana para comandos Serial de Arduino.
Protocolo: Uma letra (G, B, R ou Y) seguida de 1 (ligar) ou 0 (desligar).

Exemplos:
- "Acender azul": responda apenas B1
- "Apagar vermelho": responda apenas R0
- "Ligar o verde": responda apenas G1

IMPORTANTE: Responda APENAS o código de 2 caracteres. Nada de texto extra.
"""

def enviar_arduino(comando):
    print(f"Enviando para hardware: {comando}")
    arduino.write(comando.encode())
    # Espera o 'K' de confirmação do seu código Arduino
    while arduino.in_waiting == 0:
        pass
    return arduino.read().decode()

print("\n--- Chatbot Hardware GPT Ativo ---")

while True:
    pergunta = input("\nHumano: ")
    if pergunta.lower() in ['sair', 'parar']: break

    try:
        # Chamada da IA
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Versão mais barata e rápida
            messages=[
                {"role": "system", "content": instrucao_ia},
                {"role": "user", "content": pergunta}
            ]
        )
        
        comando_gerado = response.choices[0].message.content.strip()
        
        # Validação simples: se a IA mandou o formato correto (ex: B1)
        if len(comando_gerado) == 2:
            enviar_arduino(comando_gerado)
            print("Status: LED alterado com sucesso.")
        else:
            print(f"IA gerou um comando inválido: {comando_gerado}")

    except Exception as e:
        print(f"Erro na API: {e}")

arduino.close()