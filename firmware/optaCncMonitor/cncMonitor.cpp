#include <Arduino.h>
#include "cncMonitor.h"
#include "telemetry.h"
#include "config.h"
#include "inputMonitor.h"

// This profile only reads inputs. It never configures or writes relay outputs.
namespace {
constexpr uint8_t INPUT_PINS[8] = {A0, A1, A2, A3, A4, A5, A6, A7};
InputMonitor monitor;
CncSnapshot latestSnapshot;  // Latest observed D000..D007, retained in RAM.
uint32_t previousMs = 0;
uint64_t uptimeMs = 0;

uint8_t readInputs() {
  uint8_t raw = 0;
  for (uint8_t i = 0; i < 8; ++i) {
    if (digitalRead(INPUT_PINS[i]) == HIGH) raw |= 1U << i;
  }
  return raw;
}

void publish(uint8_t raw, uint32_t now) {
  uptimeMs += uint32_t(now - previousMs);
  previousMs = now;
  CncSnapshot& sample = latestSnapshot;
  sample.capturedMs = now;
  sample.uptimeMs = uptimeMs;
  sample.rawInputs = raw;
  sample.activeInputs = monitor.update(raw, now, INPUT_FILTER_MS);
  telemetryPublish(sample);
}
}

void cncSetup() {
  Serial.begin(115200);
  for (uint8_t pin : INPUT_PINS) pinMode(pin, INPUT);
  const uint32_t now = millis();
  const uint8_t raw = readInputs();
  previousMs = now;
  uptimeMs = now;
  monitor.begin(raw, INPUT_ACTIVE_LOW_MASK, now);
  // Initial snapshot is available even before the USB host opens the port.
  publish(raw, now);
  telemetryBegin();
}

void cncLoop() {
  const uint8_t raw = readInputs();
  publish(raw, millis());
}
