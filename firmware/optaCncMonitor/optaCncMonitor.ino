// Arduino Opta: monitoramento booleano I1..I8; serial USB por padrão.
#include "cncMonitor.h"

void setup() { cncSetup(); }

void loop() {
  cncLoop();
  // Comunicação em tarefa separada; aquisição não aguarda conexão USB/rede.
  delay(1);
}
