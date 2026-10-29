#pragma once
#include <stdint.h>

// A single observation of the eight CNC signals, copied without I/O.
struct CncSnapshot {
  uint32_t capturedMs = 0;
  uint64_t uptimeMs = 0;
  uint8_t rawInputs = 0;
  uint8_t activeInputs = 0;
};
