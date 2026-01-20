const int ledAzul = 2;
const int ledVermelho = 4;

void setup() {
  pinMode(ledAzul, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "AZUL_ON") digitalWrite(ledAzul, HIGH);
    else if (cmd == "AZUL_OFF") digitalWrite(ledAzul, LOW);
    else if (cmd == "VERMELHO_ON") digitalWrite(ledVermelho, HIGH);
    else if (cmd == "VERMELHO_OFF") digitalWrite(ledVermelho, LOW);

    Serial.println("OK"); // confirmação
  }
}
