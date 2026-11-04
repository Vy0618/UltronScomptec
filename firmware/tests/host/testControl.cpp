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
  assert(observed.activeInputs == (INPUT_ACTIVE_LOW_MASK & ultron::DIGITAL_INPUT_MASK));
  for (uint8_t i = 0; i < 8; ++i) assert(hostModes[i] == INPUT);
  assert(hostModes[D0] == -1 && hostModes[D1] == -1 && hostModes[D2] == -1);
  assert(hostWrites == 0);
  for (uint8_t i = 0; i < 8; ++i) {
    memset(hostPins, 0, sizeof(hostPins));
    hostPins[i] = HIGH;
    ++hostMillis; cncLoop();
    const uint8_t expected = (1U << i) & ultron::DIGITAL_INPUT_MASK;
    assert(observed.rawInputs == expected);
    assert(observed.activeInputs == (expected ^ (INPUT_ACTIVE_LOW_MASK & ultron::DIGITAL_INPUT_MASK)));
  }
  for (uint8_t i = 0; i < 8; ++i) hostPins[i] = HIGH;
  ++hostMillis; cncLoop();
  assert(observed.activeInputs == (ultron::DIGITAL_INPUT_MASK ^ (INPUT_ACTIVE_LOW_MASK & ultron::DIGITAL_INPUT_MASK)));
  static_assert(ultron::CURRENT_INPUT_NUMBER == 8 && !ultron::CURRENT_PHYSICAL_ENABLED,
                "I8 must stay reserved with physical current disabled");
  assert(hostWrites == 0);
  puts("PASS monitor: six digital signals / I7-I8 ignored / I8 reserved / no output writes");

  InputMonitor filter;
  const uint32_t times[8] = {20, 0, 0, 0, 0, 0, 0, 0};
  filter.begin(0, 0, 0);
  assert(filter.update(1, 1, times) == 0);
  assert(filter.update(0, 10, times) == 0);
  assert(filter.update(1, 11, times) == 0);
  assert(filter.update(1, 30, times) == 0);
  assert(filter.update(1, 31, times) == 1);
  // Emergency passes immediately even while another input is filtered.
  assert(filter.update(8, 32, times) == 9);
  assert(filter.update(8, 52, times) == 8);
  filter.begin(0, 0, UINT32_MAX - 10);
  assert(filter.update(1, UINT32_MAX - 5, times) == 0);
  assert(filter.update(1, 14, times) == 1);
  filter.begin(0, 0x08, 0);
  assert(filter.update(0, 0, times) == 8);
  assert(filter.update(8, 1, times) == 0);
  puts("PASS monitor: configurable filter / bounce / immediate emergency / polarity / rollover");

  hostMillis = UINT32_MAX - 1;
  cncSetup();
  hostMillis = 3; cncLoop();
  assert(observed.uptimeMs == uint64_t(UINT32_MAX) + 4);
  puts("PASS monitor: monotonic uptime across millis rollover");
}
