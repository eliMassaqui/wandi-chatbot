import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QSize

class WandiGPTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wandi-GPT")
        self.resize(800, 800)
        self.init_ui()

    def init_ui(self):
        # Fundo da Janela (Cinza quase branco para dar contraste com o widget branco)
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; }")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 30)
        self.main_layout.setSpacing(15)

        # 2. CONTAINER PRINCIPAL (Chat)
        self.content_card = QFrame()
        self.content_card.setObjectName("content_card")
        self.card_layout = QHBoxLayout(self.content_card)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(0)

        # ÁREA DE CHAT
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("Como posso ajudar você hoje?")
        self.chat_area.setObjectName("chat_display")
        self.card_layout.addWidget(self.chat_area, stretch=5)
        self.main_layout.addWidget(self.content_card)

        # 3. ÁREA DE INPUT (Centralizada embaixo)
        self.input_section = QVBoxLayout()
        self.input_section.setContentsMargins(100, 10, 100, 0) # Alinhamento com o chat

        # Seletores Texto/Voz (Pílulas Pequenas)
        self.tab_layout = QHBoxLayout()
        self.tab_layout.addStretch()
        self.btn_text = QPushButton("Texto")
        self.btn_voice = QPushButton("Voz")
        self.btn_text.setFixedSize(80, 32)
        self.btn_voice.setFixedSize(80, 32)
        self.btn_text.setObjectName("tab_active")
        self.btn_voice.setObjectName("tab_inactive")
        self.tab_layout.addWidget(self.btn_text)
        self.tab_layout.addWidget(self.btn_voice)
        self.tab_layout.addStretch()

        # Campo de Input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Digite sua mensagem para o Wandi-GPT")
        self.input_field.setFixedHeight(60)
        self.input_field.setObjectName("main_input")

        self.input_section.addLayout(self.tab_layout)
        self.input_section.addWidget(self.input_field)
        self.main_layout.addLayout(self.input_section)

        self.apply_pro_styles()

    def apply_pro_styles(self):
        self.setStyleSheet("""
            /* Janela e Card */
            #content_card { 
                background-color: white; 
                border-radius: 12px; 
            }
            
            #chat_display { 
                background-color: white; 
                border: 2px #dadada; 
                border-radius: 12px; 
                padding: 20px;
                font-size: 14px;
                color: #1f1f1f;
            }

            /* Seletores Texto/Voz */
            #tab_active {
                background-color: #c2e7ff;
                color: #001d35;
                border: none;
                border-radius: 16px;
                font-weight: bold;
            }
            #tab_inactive {
                background-color: #ffffff;
                border: 1px solid #747775;
                border-radius: 16px;
                color: #444746;
            }
            #tab_inactive:hover { background-color: #f1f3f4; }

            /* Input Principal */
            #main_input {
                background-color: #ffffff;
                border: 1px solid #757575;
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                border-bottom-left-radius: 8px;
                padding: 0 25px;
                font-size: 15px;
                color: #171717;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiGPTApp()
    window.show()
    sys.exit(app.exec())