#pragma once
#include <stdint.h>

// Values copied from the local controller; pointers always refer to string literals.
struct MesaSnapshot {
  uint32_t capturedMs = 0;
  uint64_t uptimeMs = 0;
  uint8_t rawInputs = 0;
  uint8_t commandedOutputs = 0;
  const char* state = "aguardando_peca";
  const char* height = "invalida";
  bool cycleActive = false;
  bool fault = false;
  bool metal = false;
  bool ramp1Full = false;
  bool ramp2Full = false;
  uint32_t total = 0;
  uint32_t straight = 0;
  uint32_t drop1 = 0;
  uint32_t drop2 = 0;
  uint32_t faults = 0;
};
