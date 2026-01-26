import sys
import qtawesome as qta
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QFrame, QGraphicsDropShadowEffect, QLabel)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QPropertyAnimation

class HoverMenuBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("hover_menu_bar")
        self.setFixedSize(150, 40)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 15, 0)
        
        self.label_menu = QPushButton(" OPÇÕES")
        self.label_menu.setIcon(qta.icon('fa5s.bars', color='#70757a'))
        self.label_menu.setStyleSheet("border: none; font-weight: bold; color: #70757a; background: transparent;")
        self.layout.addWidget(self.label_menu)

        self.options_widget = QWidget()
        self.options_layout = QHBoxLayout(self.options_widget)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_clear_chat = QPushButton(qta.icon('fa5s.trash-alt', color='#d93025'), "")
        self.btn_help = QPushButton(qta.icon('fa5s.question-circle', color='#5f6368'), "")
        
        for btn in [self.btn_clear_chat, self.btn_help]:
            btn.setFixedSize(30, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { border: none; border-radius: 15px; background: transparent; } QPushButton:hover { background-color: #f1f3f4; }")
            self.options_layout.addWidget(btn)
            
        self.layout.addWidget(self.options_widget)
        self.options_widget.hide()
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(250)

    def enterEvent(self, event):
        self.animation.stop(); self.animation.setEndValue(220); self.animation.start()
        self.options_widget.show()

    def leaveEvent(self, event):
        self.animation.stop(); self.animation.setEndValue(150); self.animation.start()
        self.options_widget.hide()

class WandiGPTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wandi-GPT | Especialista em Robótica")
        screen = QApplication.primaryScreen().geometry()
        self.resize(int(screen.width() * 0.50), int(screen.height() * 0.80))
        
        self.is_connected = False
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; }")
        self.central_widget = QWidget(); self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget); self.main_layout.setContentsMargins(40, 20, 40, 40)

        # TOPO
        self.header_layout = QHBoxLayout()
        
        # Botão API
        self.btn_api = QPushButton(" API KEY")
        self.btn_api.setFixedSize(110, 40)
        self.btn_api.setObjectName("top_btn_pill")
        self.header_layout.addWidget(self.btn_api)

        # BOTÃO DE CONEXÃO AUTOMÁTICA (Substituiu o Dropdown)
        self.btn_connect = QPushButton()
        self.btn_connect.setFixedSize(40, 40)
        self.btn_connect.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_connect.setIcon(qta.icon('fa5s.plug', color='#5f6368'))
        self.btn_connect.setObjectName("connect_btn")
        self.btn_connect.setToolTip("Conexão Automática de Hardware")
        self.btn_connect.clicked.connect(self.auto_connect_hardware)
        self.header_layout.addWidget(self.btn_connect)
        
        self.header_layout.addStretch()

        # Menu de Opções
        self.horizontal_menu = HoverMenuBar()
        self.horizontal_menu.btn_clear_chat.clicked.connect(lambda: self.chat_area.clear())
        self.header_layout.addWidget(self.horizontal_menu)
        
        self.main_layout.addLayout(self.header_layout)

        # CARD PRINCIPAL
        self.content_card = QFrame(); self.content_card.setObjectName("content_card")
        self.card_layout = QVBoxLayout(self.content_card); self.card_layout.setContentsMargins(0, 0, 0, 0)
        shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(30); shadow.setYOffset(10); shadow.setColor(QColor(0, 0, 0, 20))
        self.content_card.setGraphicsEffect(shadow)

        self.chat_area = QTextEdit(); self.chat_area.setReadOnly(True); self.chat_area.setObjectName("chat_display")
        self.card_layout.addWidget(self.chat_area)

        self.main_layout.addWidget(self.content_card)

        # INPUT AREA
        self.input_section = QVBoxLayout(); self.input_section.setContentsMargins(0, 10, 0, 0)
        self.tab_layout = QHBoxLayout(); self.tab_layout.addStretch()
        
        self.btn_text = QPushButton(" Texto"); self.btn_voice = QPushButton(" Voz")
        self.btn_text.setObjectName("tab_active"); self.btn_voice.setObjectName("tab_inactive")
        
        self.input_field = QLineEdit(); self.input_field.setPlaceholderText("Escreva para o Wandi-GPT...")
        self.input_field.setFixedHeight(65); self.input_field.setObjectName("main_input")
        
        self.input_section.addLayout(self.tab_layout); self.input_section.addWidget(self.input_field)
        self.main_layout.addLayout(self.input_section)

        self.apply_styles()

    def auto_connect_hardware(self):
        """Lógica para busca e conexão automática"""
        # Aqui entra sua lógica original de varrer as portas futuramente
        if not self.is_connected:
            self.chat_area.append("<br><b style='color: #1a73e8;'>SISTEMA:</b> Buscando hardware automaticamente...")
            # Simulação de conexão:
            self.is_connected = True
            self.btn_connect.setIcon(qta.icon('fa5s.link', color='#1e8e3e')) # Verde para conectado
            self.btn_connect.setStyleSheet("background-color: #e6f4ea; border: 1px solid #1e8e3e;")
        else:
            self.is_connected = False
            self.btn_connect.setIcon(qta.icon('fa5s.plug', color='#5f6368'))
            self.btn_connect.setStyleSheet("")
            self.chat_area.append("<br><b style='color: #d93025;'>SISTEMA:</b> Hardware desconectado.")

    def apply_styles(self):
        self.setStyleSheet("""
            #content_card { background-color: white; border-radius: 20px; }
            #chat_display { background-color: white; border: 1px solid #e3e3e3; border-radius: 20px; padding: 30px; }
            #top_btn_pill { background-color: white; border: 1px solid #dadce0; border-radius: 20px; color: #444746; font-weight: 600; }
            #connect_btn { background-color: white; border: 1px solid #dadce0; border-radius: 20px; }
            #connect_btn:hover { background-color: #f8f9fa; }
            #hover_menu_bar { background-color: white; border: 1px solid #dadce0; border-radius: 20px; }
            #tab_active { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #1a73e8; border-radius: 19px; font-weight: bold; width: 110px; height: 38px; }
            #tab_inactive { background-color: #ffffff; border: 1px solid #dadce0; border-radius: 19px; color: #5f6368; width: 110px; height: 38px; }
            #main_input { background-color: #f0f4f9; border: none; border-radius: 32px; padding: 0 30px; font-size: 16px; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiGPTApp()
    window.show()
    sys.exit(app.exec())