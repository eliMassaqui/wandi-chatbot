import sys
import serial
import time
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel, QFrame, QScrollArea, QMainWindow,
    QDockWidget, QSizePolicy
)
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt
from openai import OpenAI

# ------------------------
# Configurações GPT e Arduino
# ------------------------
client = OpenAI(api_key="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")
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

led_status = {"AZUL": False, "VERMELHO": False}

# ------------------------
# Funções Arduino
# ------------------------
def enviar_arduino(cmd):
    arduino.write((cmd + "\n").encode())
    while arduino.in_waiting == 0:
        pass
    return arduino.readline().decode().strip()

def piscar_led(led, vezes, tempo_ms):
    for _ in range(vezes):
        enviar_arduino(f"{led}_ON")
        led_status[led] = True
        update_led_indicators()
        time.sleep(tempo_ms / 1000)
        enviar_arduino(f"{led}_OFF")
        led_status[led] = False
        update_led_indicators()
        time.sleep(tempo_ms / 1000)

# ------------------------
# Interface principal
# ------------------------
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Wandi GPT")
window.resize(800, 600)
window.setStyleSheet("background-color: #121A2B; color: white;")

central_widget = QWidget()
window.setCentralWidget(central_widget)
main_layout = QVBoxLayout(central_widget)
main_layout.setContentsMargins(50, 20, 50, 20)  # centraliza a área de chat

# ------------------------
# Área de chat com scroll
# ------------------------
chat_area = QTextEdit()
chat_area.setReadOnly(True)
chat_area.setStyleSheet("""
    background-color: transparent;
    border: none;
    font-size: 14px;
""")
chat_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
main_layout.addWidget(chat_area)

# ------------------------
# Input no footer
# ------------------------
footer_layout = QHBoxLayout()
user_input = QLineEdit()
user_input.setPlaceholderText("Escreva sua mensagem aqui...")
user_input.setStyleSheet("""
    padding: 10px; border-radius: 10px; font-size: 14px; background-color: #1C263B; color: white;
""")
send_btn = QPushButton("Enviar")
send_btn.setStyleSheet("""
    background-color: #3B6EA5; border-radius: 10px; padding: 10px; font-weight: bold;
""")
footer_layout.addWidget(user_input)
footer_layout.addWidget(send_btn)
main_layout.addLayout(footer_layout)

# ------------------------
# Sidebar LED flutuante
# ------------------------
sidebar = QDockWidget("LEDs", window)
sidebar.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
sidebar_widget = QWidget()
sidebar_layout = QVBoxLayout(sidebar_widget)
sidebar_layout.setContentsMargins(10, 10, 10, 10)

led_azul = QLabel("LED AZUL")
led_vermelho = QLabel("LED VERMELHO")
for lbl in [led_azul, led_vermelho]:
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet("background-color: grey; padding: 10px; border-radius: 5px; font-weight: bold; color: white; margin-bottom: 10px;")
    sidebar_layout.addWidget(lbl)

sidebar.setWidget(sidebar_widget)
window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, sidebar)

# ------------------------
# Atualiza indicadores LED
# ------------------------
def update_led_indicators():
    led_azul.setStyleSheet(f"background-color: {'blue' if led_status['AZUL'] else 'grey'}; padding: 10px; border-radius: 5px; font-weight: bold; color: white; margin-bottom: 10px;")
    led_vermelho.setStyleSheet(f"background-color: {'red' if led_status['VERMELHO'] else 'grey'}; padding: 10px; border-radius: 5px; font-weight: bold; color: white; margin-bottom: 10px;")

# ------------------------
# Processamento do input
# ------------------------
def process_input():
    text = user_input.text().strip()
    if not text:
        return
    append_chat_card("Você", text, "#00B3FF")
    user_input.clear()

    # Chamada GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
Você é um assistente inteligente de hardware e chat.
Comandos de LED:
- AZUL_ON / AZUL_OFF
- VERMELHO_ON / VERMELHO_OFF
- BLINK <LED> <vezes> <tempo_ms>
Gere uma linha por LED quando precisar piscar múltiplos LEDs.
Responda apenas com comandos válidos ou respostas de chat.
"""},
            {"role": "user", "content": text}
        ]
    )

    reply = response.choices[0].message.content.strip()
    append_chat_card("GPT", reply, "#FF0099")

    # Processa cada linha
    for linha in reply.splitlines():
        linha = linha.strip()
        if linha.startswith("BLINK"):
            try:
                parts = linha.split()
                led = parts[1]
                vezes = int(parts[2])
                tempo_ms = int(parts[3])
                threading.Thread(target=piscar_led, args=(led, vezes, tempo_ms), daemon=True).start()
            except:
                append_chat_card("Erro", f"Comando BLINK inválido: {linha}", "red")
        elif linha in ["AZUL_ON", "AZUL_OFF", "VERMELHO_ON", "VERMELHO_OFF"]:
            enviar_arduino(linha)
            led_status[linha.split("_")[0]] = linha.endswith("ON")
            update_led_indicators()

# ------------------------
# Função para criar cards de chat
# ------------------------
def append_chat_card(sender, text, color):
    card = f"<div style='background-color:{color}; padding:10px; border-radius:10px; margin:5px 0; max-width:70%;'>{sender}: {text}</div>"
    chat_area.append(card)
    chat_area.moveCursor(QTextCursor.MoveOperation.End)

send_btn.clicked.connect(process_input)
user_input.returnPressed.connect(process_input)

window.show()
sys.exit(app.exec())
