import serial
import time
from openai import OpenAI

# Conexão GPT
client = OpenAI(api_key="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")

# Conexão Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# Prompt GPT atualizado: mais inteligente para usuário
prompt_base = """
Você é um assistente que conversa normalmente. 
Funcionalidades de LED disponíveis:
- AZUL_ON / AZUL_OFF
- VERMELHO_ON / VERMELHO_OFF
- ALL_ON (liga todos os LEDs)
- ALL_OFF (desliga todos os LEDs)
- BLINK <tempo_ms> (pisca todos os LEDs com intervalo em milissegundos)

Se o usuário pedir para acender, apagar ou piscar LEDs, responda APENAS com um dos comandos acima.
Para qualquer outra pergunta, converse normalmente.
"""

def enviar_arduino(cmd):
    """
    Envia comando para Arduino.
    Suporta comandos compostos como ALL_ON, ALL_OFF ou BLINK <tempo_ms>
    """
    if cmd == "ALL_ON":
        for c in ["AZUL_ON", "VERMELHO_ON"]:
            arduino.write((c + "\n").encode())
            arduino.readline()  # confirmação
        return "Todos os LEDs ligados."
    
    elif cmd == "ALL_OFF":
        for c in ["AZUL_OFF", "VERMELHO_OFF"]:
            arduino.write((c + "\n").encode())
            arduino.readline()
        return "Todos os LEDs desligados."
    
    elif cmd.startswith("BLINK"):
        try:
            intervalo = int(cmd.split()[1])
        except:
            intervalo = 500  # padrão 500ms
        for _ in range(5):  # pisca 5 vezes
            for c in ["AZUL_ON", "VERMELHO_ON"]:
                arduino.write((c + "\n").encode())
                arduino.readline()
            time.sleep(intervalo/1000)
            for c in ["AZUL_OFF", "VERMELHO_OFF"]:
                arduino.write((c + "\n").encode())
                arduino.readline()
            time.sleep(intervalo/1000)
        return f"LEDs piscando a cada {intervalo}ms."
    
    else:
        arduino.write((cmd + "\n").encode())
        arduino.readline()
        return f"LED atualizado ({cmd})"

# ------------------------
# Loop principal
# ------------------------
while True:
    user_input = input("Humano: ")
    if user_input.lower() in ["sair", "parar"]:
        break

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_base},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response.choices[0].message.content.strip()

    # Se for comando de hardware, envia para Arduino
    if any(reply.startswith(c) for c in ["AZUL", "VERMELHO", "ALL_ON", "ALL_OFF", "BLINK"]):
        resultado = enviar_arduino(reply)
        print(f"GPT: {resultado}")
    else:
        print(f"GPT: {reply}")
