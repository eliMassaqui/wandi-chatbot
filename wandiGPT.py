import sys
import qtawesome as qta
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QFrame, QGraphicsDropShadowEffect, QComboBox, 
                             QLabel, QDialog, QFormLayout, QDialogButtonBox)
from PyQt6.QtGui import QColor, QLinearGradient, QPalette, QBrush
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class NewProjectDialog(QDialog):
    """Card de Configuração com Design Profissional e Gradiente"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuração de Hardware")
        self.setFixedWidth(450)
        self.setMinimumHeight(350)
        
        # Layout Principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        # Título do Card
        self.title_label = QLabel("NOVO PROJETO")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a73e8; letter-spacing: 1px;")
        self.main_layout.addWidget(self.title_label)

        # Campos
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do Projeto (Ex: Rover Bluetooth)")
        self.name_input.setFixedHeight(45)
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Descreva os pinos e comandos...\nEx: Pino 10 -> Motor A\nComando 'S' -> Stop")
        self.desc_input.setMinimumHeight(120)
        
        self.main_layout.addWidget(QLabel("NOME DO PROJETO"))
        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(QLabel("ARQUITETURA DE HARDWARE E PINOS"))
        self.main_layout.addWidget(self.desc_input)

        # Botões
        self.button_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_save = QPushButton("Salvar Projeto")
        self.btn_save.setFixedWidth(150)
        self.btn_save.setFixedHeight(40)
        self.btn_cancel.setFixedHeight(40)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.btn_cancel)
        self.button_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(self.button_layout)

        self.apply_dialog_styles()

    def apply_dialog_styles(self):
        # Gradiente Azul para Branco Transparente
        self.setStyleSheet("""
            QDialog { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 rgba(232, 240, 254, 255), 
                            stop:1 rgba(255, 255, 255, 220));
                border-radius: 15px;
            }
            QLabel { 
                color: #5f6368; font-weight: bold; font-size: 10px; 
            }
            QLineEdit, QTextEdit { 
                background-color: rgba(255, 255, 255, 180);
                border: 1px solid #dadce0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #202124;
            }
            QLineEdit:focus, QTextEdit:focus { 
                border: 2px solid #1a73e8;
                background-color: white;
            }
            QPushButton { 
                border-radius: 8px; font-weight: bold; font-size: 13px; 
            }
            QPushButton#save_btn { 
                background-color: #1a73e8; color: white; border: none; 
            }
            QPushButton:hover { background-color: #f1f3f4; border: 1px solid #dadce0; }
        """)
        self.btn_save.setObjectName("save_btn")
        self.btn_save.setStyleSheet("background-color: #1a73e8; color: white; border: none;")

# --- MANTENDO A ESTRUTURA ORIGINAL DO WANDI GPT ABAIXO ---

class HoverMenuBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("hover_menu_bar")
        self.setFixedSize(180, 40)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 15, 0)
        
        self.label_menu = QPushButton(" PROJETOS")
        self.label_menu.setIcon(qta.icon('fa5s.robot', color='#70757a'))
        self.label_menu.setStyleSheet("border: none; font-weight: bold; color: #70757a; background: transparent;")
        self.layout.addWidget(self.label_menu)

        self.options_widget = QWidget()
        self.options_layout = QHBoxLayout(self.options_widget)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_new_project = QPushButton(qta.icon('fa5s.plus', color='#1a73e8'), "")
        self.btn_clear_chat = QPushButton(qta.icon('fa5s.trash-alt', color='#d93025'), "")
        self.btn_help = QPushButton(qta.icon('fa5s.question-circle', color='#5f6368'), "")
        
        for btn in [self.btn_new_project, self.btn_clear_chat, self.btn_help]:
            btn.setFixedSize(30, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("QPushButton { border: none; border-radius: 15px; background: transparent; } QPushButton:hover { background-color: #f1f3f4; }")
            self.options_layout.addWidget(btn)
            
        self.layout.addWidget(self.options_widget)
        self.options_widget.hide()
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(250)

    def enterEvent(self, event):
        self.animation.stop(); self.animation.setEndValue(380); self.animation.start()
        self.options_widget.show()

    def leaveEvent(self, event):
        self.animation.stop(); self.animation.setEndValue(180); self.animation.start()
        self.options_widget.hide()

class WandiGPTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wandi-GPT | Especialista em Robótica")
        screen = QApplication.primaryScreen().geometry()
        self.resize(int(screen.width() * 0.55), int(screen.height() * 0.85))
        
        self.active_project = None 
        self.project_buttons = {}

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; }")
        self.central_widget = QWidget(); self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget); self.main_layout.setContentsMargins(40, 20, 40, 40)

        # TOPO
        self.header_layout = QHBoxLayout()
        self.btn_api = QPushButton(" API KEY"); self.btn_api.setFixedSize(110, 40); self.btn_api.setObjectName("top_btn_pill")
        self.header_layout.addWidget(self.btn_api)

        self.combo_ports = QComboBox(); self.combo_ports.setFixedSize(130, 40); self.combo_ports.setObjectName("combo_square")
        self.combo_ports.addItem("CONEXÃO")
        self.header_layout.addWidget(self.combo_ports)
        self.header_layout.addStretch()

        self.horizontal_menu = HoverMenuBar()
        self.horizontal_menu.btn_new_project.clicked.connect(self.add_project_flow)
        self.horizontal_menu.btn_clear_chat.clicked.connect(lambda: self.chat_area.clear())
        self.header_layout.addWidget(self.horizontal_menu)
        self.header_layout.addStretch()
        self.main_layout.addLayout(self.header_layout)

        # CARD PRINCIPAL
        self.content_card = QFrame(); self.content_card.setObjectName("content_card")
        self.card_layout = QHBoxLayout(self.content_card); self.card_layout.setContentsMargins(0, 0, 0, 0)
        shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(30); shadow.setYOffset(10); shadow.setColor(QColor(0, 0, 0, 20))
        self.content_card.setGraphicsEffect(shadow)

        self.chat_area = QTextEdit(); self.chat_area.setReadOnly(True); self.chat_area.setObjectName("chat_display")
        self.card_layout.addWidget(self.chat_area, stretch=5)

        self.sidebar = QFrame(); self.sidebar.setFixedWidth(240); self.sidebar.setObjectName("sidebar_pro")
        self.side_layout = QVBoxLayout(self.sidebar)
        self.side_layout.addWidget(QLabel("  PROJETOS EM EXECUÇÃO"), alignment=Qt.AlignmentFlag.AlignTop)
        
        self.project_list_widget = QWidget(); self.project_list_layout = QVBoxLayout(self.project_list_widget)
        self.project_list_layout.setContentsMargins(0, 0, 0, 0); self.project_list_layout.setSpacing(5)
        self.side_layout.addWidget(self.project_list_widget)
        
        self.side_layout.addStretch(); self.card_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_card)

        # INPUT AREA
        self.input_section = QVBoxLayout(); self.input_section.setContentsMargins(0, 10, 240, 0)
        self.tab_layout = QHBoxLayout(); self.tab_layout.addStretch()
        self.btn_text = QPushButton(" Texto"); self.btn_voice = QPushButton(" Voz")
        self.btn_text.setObjectName("tab_active"); self.btn_voice.setObjectName("tab_inactive")
        self.input_field = QLineEdit(); self.input_field.setPlaceholderText("Escreva para o Wandi-GPT...")
        self.input_field.setFixedHeight(65); self.input_field.setObjectName("main_input")
        self.input_section.addLayout(self.tab_layout); self.input_section.addWidget(self.input_field)
        self.main_layout.addLayout(self.input_section)

        self.apply_styles()

    def add_project_flow(self):
        dialog = NewProjectDialog(self)
        if dialog.exec():
            name = dialog.name_input.text()
            desc = dialog.desc_input.toPlainText()
            if name and name not in self.project_buttons:
                btn = QPushButton(f"  {name}")
                btn.setFixedHeight(50); btn.setObjectName("side_btn")
                btn.clicked.connect(lambda: self.handle_project_selection(name, desc))
                self.project_list_layout.addWidget(btn)
                self.project_buttons[name] = btn

    def handle_project_selection(self, name, desc):
        target_btn = self.project_buttons[name]
        if self.active_project == name:
            self.active_project = None
            target_btn.setStyleSheet("")
            self.input_field.setPlaceholderText("Escreva para o Wandi-GPT...")
            self.chat_area.append(f"<br><b style='color: #d93025;'>SISTEMA:</b> Projeto '{name}' desativado.")
            return

        if self.active_project is not None:
            self.chat_area.append(f"<br><b style='color: #f29900;'>AVISO:</b> Desative o projeto '{self.active_project}' primeiro.")
            return

        self.active_project = name
        target_btn.setStyleSheet("background-color: #e8f0fe; color: #1a73e8; border-right: 4px solid #1a73e8;")
        self.input_field.setPlaceholderText(f"Falando com: {name}...")
        self.chat_area.append(f"<br><b style='color: #1a73e8;'>Wandi-GPT:</b> Projeto '{name}' conectado.")

    def apply_styles(self):
        self.setStyleSheet("""
            #content_card { background-color: white; border-radius: 20px; }
            #chat_display { background-color: white; border: 1px solid #e3e3e3; border-top-left-radius: 20px; border-bottom-left-radius: 20px; padding: 30px; border-right: none; }
            #sidebar_pro { background-color: #f8f9fa; border: 1px solid #e3e3e3; border-top-right-radius: 20px; border-bottom-right-radius: 20px; }
            #top_btn_pill { background-color: white; border: 1px solid #dadce0; border-radius: 20px; color: #444746; font-weight: 600; }
            #combo_square { background-color: white; border: 1px solid #dadce0; border-radius: 8px; color: #444746; font-weight: 600; padding-left: 10px; }
            #combo_square::drop-down { border: none; width: 0px; }
            #hover_menu_bar { background-color: white; border: 1px solid #dadce0; border-radius: 20px; }
            #side_btn { background-color: transparent; border: none; text-align: left; padding-left: 25px; color: #444746; font-weight: bold; }
            #tab_active { background-color: #e8f0fe; color: #1a73e8; border: 1px solid #1a73e8; border-radius: 19px; font-weight: bold; width: 110px; height: 38px; }
            #tab_inactive { background-color: #ffffff; border: 1px solid #dadce0; border-radius: 19px; color: #5f6368; width: 110px; height: 38px; }
            #main_input { background-color: #f0f4f9; border: none; border-radius: 32px; padding: 0 30px; font-size: 16px; }
            QLabel { color: #70757a; font-weight: bold; font-size: 9px; margin: 10px 0 5px 20px; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiGPTApp()
    window.show()
    sys.exit(app.exec())