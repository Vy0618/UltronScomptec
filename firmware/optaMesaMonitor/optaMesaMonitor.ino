// Arduino Opta WiFi: controle original da mesa + telemetria JSON HTTP ou USB SCOMPTEC.
#include "mesaControl.h"

void setup() { mesaSetup(); }

void loop() {
  mesaLoop();
  // A comunicação HTTP/USB roda em tarefa separada do controle da mesa.
  // Mantida a pausa de 1 ms existente no ZIP.
  // Os tempos de classificacao/atuacao continuam definidos em mesaControl.cpp.
  delay(1);
}
