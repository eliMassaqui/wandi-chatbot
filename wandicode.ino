// Definição dos pinos baseada nas suas fotos
const int ledVerde = 2;
const int ledAzul = 3;
const int ledVermelho = 4;
const int ledAmarelo = 5;

void setup() {
  // Inicializa a comunicação serial a 9600 bps
  Serial.begin(9600);
  
  // Configura os pinos como saída
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAzul, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(ledAmarelo, OUTPUT);
  
  // Garante que tudo comece desligado
  digitalWrite(ledVerde, LOW);
  digitalWrite(ledAzul, LOW);
  digitalWrite(ledVermelho, LOW);
  digitalWrite(ledAmarelo, LOW);
}

void loop() {
  // Verifica se chegaram pelo menos 2 caracteres (Ex: G1, B0)
  if (Serial.available() >= 2) {
    char cor = Serial.read();    // Lê a letra (G, B, R, Y)
    char estado = Serial.read(); // Lê o estado (1 para ligado, 0 para desligado)
    
    int pinoAlvo = -1;

    // Lógica de seleção do LED
    switch (cor) {
      case 'G': pinoAlvo = ledVerde;    break; // Green
      case 'B': pinoAlvo = ledAzul;     break; // Blue
      case 'R': pinoAlvo = ledVermelho; break; // Red
      case 'Y': pinoAlvo = ledAmarelo;  break; // Yellow
    }

    // Se a cor for válida, aplica o estado
    if (pinoAlvo != -1) {
      if (estado == '1') {
        digitalWrite(pinoAlvo, HIGH);
      } else if (estado == '0') {
        digitalWrite(pinoAlvo, LOW);
      }
      
      // Envia confirmação para o Python
      Serial.print("K"); 
    }
  }
}