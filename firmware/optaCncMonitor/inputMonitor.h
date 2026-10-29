#pragma once
#include <stdint.h>

// Pure input normalization/filtering, independent of GPIO and transport.
class InputMonitor {
 public:
  void begin(uint8_t raw, uint8_t activeLow, uint32_t now) {
    activeLow_ = activeLow;
    stable_ = candidate_ = raw ^ activeLow_;
    for (uint8_t i = 0; i < 8; ++i) changedAt_[i] = now;
  }
  uint8_t update(uint8_t raw, uint32_t now, const uint32_t (&filterMs)[8]) {
    const uint8_t normalized = raw ^ activeLow_;
    for (uint8_t i = 0; i < 8; ++i) {
      const uint8_t mask = uint8_t(1U << i);
      if ((normalized ^ candidate_) & mask) {
        candidate_ ^= mask;
        changedAt_[i] = now;
      }
      if (((candidate_ ^ stable_) & mask) && uint32_t(now - changedAt_[i]) >= filterMs[i]) {
        stable_ ^= mask;
      }
    }
    return stable_;
  }
 private:
  uint8_t activeLow_ = 0, stable_ = 0, candidate_ = 0;
  uint32_t changedAt_[8] = {};
};
