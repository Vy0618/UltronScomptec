#include <cassert>
#include <cstdio>
#include <cstring>
#include "Arduino.h"
#include "../../optaCncMonitor/telemetry.h"
uint32_t hostMillis = 0;
int hostPins[32] = {};
int hostModes[32];
unsigned hostWrites = 0;
HostSerial Serial;
CncSnapshot observed;
void telemetryBegin() {}
void telemetryPublish(const CncSnapshot& snapshot) { observed = snapshot; }
#include "../../optaCncMonitor/cncMonitor.cpp"

int main() {
  memset(hostModes, -1, sizeof(hostModes));
  cncSetup();
  assert(observed.activeInputs == (INPUT_ACTIVE_LOW_MASK & 0x3F));
  for (uint8_t i = 0; i < 8; ++i) assert(hostModes[i] == INPUT);
  assert(hostModes[D0] == -1 && hostModes[D1] == -1 && hostModes[D2] == -1);
  assert(hostWrites == 0);
  // Independent hardware contract: I1..I6 are digital; I7/I8 are never sampled.
  // Include all combinations of the reserved inputs so a read of either is caught.
  for (unsigned bits = 0; bits < 256; ++bits) {
    for (uint8_t pin = 0; pin < 8; ++pin)
      hostPins[pin] = bits & (1U << pin) ? HIGH : LOW;
    ++hostMillis; cncLoop();
    const uint8_t expected = bits & 0x3F;
    assert(observed.rawInputs == expected);
    assert(observed.activeInputs == (expected ^ (INPUT_ACTIVE_LOW_MASK & 0x3F)));
    assert(hostWrites == 0);
  }
  for (uint8_t i = 0; i < 8; ++i) hostPins[i] = HIGH;
  ++hostMillis; cncLoop();
  assert(observed.activeInputs == (0x3F ^ (INPUT_ACTIVE_LOW_MASK & 0x3F)));
  static_assert(ultron::CURRENT_INPUT_NUMBER == 8 && !ultron::CURRENT_PHYSICAL_ENABLED,
                "I8 must stay reserved with physical current disabled");
  assert(hostWrites == 0);
  puts("PASS monitor: all 256 input combinations / six digital signals / I7-I8 ignored / no output writes");

  InputMonitor filter;
  const uint32_t times[8] = {20, 0, 0, 0, 0, 0, 0, 0};
  filter.begin(0, 0, 0);
  assert(filter.update(1, 1, times) == 0);
  assert(filter.update(0, 10, times) == 0);
  assert(filter.update(1, 11, times) == 0);
  assert(filter.update(1, 30, times) == 0);
  assert(filter.update(1, 31, times) == 1);
  // Emergency passes immediately even while another input is filtered.
  assert(filter.update(0x04, 32, times) == 0x05);
  assert(filter.update(0x04, 52, times) == 0x04);
  filter.begin(0, 0, UINT32_MAX - 10);
  assert(filter.update(1, UINT32_MAX - 5, times) == 0);
  assert(filter.update(1, 14, times) == 1);
  filter.begin(0, 0x04, 0);
  assert(filter.update(0, 0, times) == 0x04);
  assert(filter.update(0x04, 1, times) == 0);
  puts("PASS monitor: configurable filter / bounce / immediate emergency / polarity / rollover");

  hostMillis = UINT32_MAX - 1;
  cncSetup();
  hostMillis = 3; cncLoop();
  assert(observed.uptimeMs == uint64_t(UINT32_MAX) + 4);
  puts("PASS monitor: monotonic uptime across millis rollover");
}
