import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QSize

class WandiGPTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wandi-GPT Professional")
        self.resize(1200, 800)
        self.init_ui()

    def init_ui(self):
        # Fundo da Janela (Cinza quase branco para dar contraste com o widget branco)
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; }")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 30)
        self.main_layout.setSpacing(15)

        # 1. MENU BAR SUPERIOR (Design Pílula)
        self.top_container = QWidget()
        self.top_layout = QHBoxLayout(self.top_container)
        self.btn_menu = QPushButton("MENU BAR")
        self.btn_menu.setFixedSize(180, 35)
        self.btn_menu.setObjectName("top_menu")
        self.top_layout.addWidget(self.btn_menu, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.top_container)

        # 2. CONTAINER PRINCIPAL (Chat + Sidebar) - Onde aplicamos a sombra
        self.content_card = QFrame()
        self.content_card.setObjectName("content_card")
        self.card_layout = QHBoxLayout(self.content_card)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(0)

        # Efeito de Sombra Profissional
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.content_card.setGraphicsEffect(shadow)

        # ÁREA DE CHAT
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setPlaceholderText("Como posso ajudar você hoje?")
        self.chat_area.setObjectName("chat_display")
        self.card_layout.addWidget(self.chat_area, stretch=5)

        # SIDEBAR (Colada conforme o desenho)
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setObjectName("sidebar_pro")
        self.side_layout = QVBoxLayout(self.sidebar)
        self.side_layout.setContentsMargins(0, 10, 0, 10)
        self.side_layout.setSpacing(5)

        for i in range(7):
            btn = QPushButton(f"  Histórico de Conversa {i+1}")
            btn.setFixedHeight(50)
            btn.setObjectName("side_btn")
            self.side_layout.addWidget(btn)
        
        self.side_layout.addStretch()
        self.card_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_card)

        # 3. ÁREA DE INPUT (Centralizada embaixo)
        self.input_section = QVBoxLayout()
        self.input_section.setContentsMargins(0, 10, 220, 0) # Alinhamento com o chat

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
        self.input_field.setPlaceholderText("Digite sua mensagem para o Wandi-GPT...")
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
                border: 1px solid #e3e3e3; 
                border-top-left-radius: 12px; 
                border-bottom-left-radius: 12px;
                border-right: none;
                padding: 20px;
                font-size: 14px;
                color: #1f1f1f;
            }

            #sidebar_pro { 
                background-color: #f8f9fa; 
                border: 1px solid #e3e3e3;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }

            /* Botões da Sidebar */
            #side_btn {
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 15px;
                color: #444746;
                font-size: 13px;
                border-radius: 0px;
            }
            #side_btn:hover { background-color: #eff1f3; color: #1a73e8; }

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
                background-color: #f0f4f9;
                border: none;
                border-radius: 30px;
                padding: 0 25px;
                font-size: 15px;
                color: #1f1f1f;
            }

            /* Top Menu Bar */
            #top_menu {
                background-color: #ffffff;
                border: 1px solid #c4c7c5;
                border-radius: 17px;
                color: #444746;
                font-size: 11px;
                font-weight: 600;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiGPTApp()
    window.show()
    sys.exit(app.exec())