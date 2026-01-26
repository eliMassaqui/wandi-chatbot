import openai
import serial
import serial.tools.list_ports

class WandiBackend:
    def __init__(self):
        self.api_key = None
        self.client = None
        self.serial_inst = None
        self.chat_history = [
            {"role": "system", "content": "Você é o Wandi-GPT, um especialista em robótica e hardware."}
        ]

    # --- LÓGICA DE INTELIGÊNCIA ARTIFICIAL ---
    def set_api_key(self, key):
        self.api_key = key
        self.client = openai.OpenAI(api_key=self.api_key)

    def get_chat_response(self, user_input):
        if not self.client or not self.api_key:
            return "MODO DEMO: Olá! Sou o Wandi-GPT. (Configure uma API Key com créditos para respostas reais)."
        
        try:
            self.chat_history.append({"role": "user", "content": user_input})
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.chat_history
            )
            ai_message = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": ai_message})
            return ai_message
            
        except Exception as e:
            # Se der erro de cota (429), ele avisa mas não quebra o app
            if "insufficient_quota" in str(e):
                return "ERRO DE COTA: Sua chave API está sem créditos. Verifique em platform.openai.com/account/billing"
            return f"Erro na API: {str(e)}"

    # --- RESTANTE DAS FUNÇÕES (SERIAL) MANTIDAS IGUAIS ---
    def find_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def auto_connect_serial(self, baudrate=9600):
        ports = self.find_ports()
        if not ports:
            return False, "Nenhum hardware encontrado."
        try:
            self.serial_inst = serial.Serial(ports[0], baudrate, timeout=1)
            return True, f"Conectado em {ports[0]}"
        except Exception as e:
            return False, f"Falha ao conectar: {str(e)}"

    def disconnect_serial(self):
        if self.serial_inst and self.serial_inst.is_open:
            self.serial_inst.close()
        return "Hardware desconectado."