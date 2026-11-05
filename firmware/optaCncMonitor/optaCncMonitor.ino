// Arduino Opta: IHM Q0.0..Q0.5 -> I1..I6; I7 livre, I8 reservada; USB por padrão.
#include "cncMonitor.h"

void setup() { cncSetup(); }

void loop() {
  cncLoop();
  // Comunicação em tarefa separada; aquisição não aguarda conexão USB/rede.
  delay(1);
}
