#include <cassert>
#include <cstdio>
#include <fstream>
#include <string>
#include "../../optaCncMonitor/telemetryCore.h"
#include "../../optaCncMonitor/telemetryPayload.h"
#include "../../optaCncMonitor/httpResponse.h"

const char* DEVICE = "11111111-1111-4111-8111-111111111111";
const char* BOOT = "22222222-2222-4222-8222-222222222222";
const char* OTHER = "33333333-3333-4333-8333-333333333333";
constexpr uint64_t UNIX_TIME = 1792584000ULL;
CncSnapshot sample(uint32_t ms, uint8_t active = 0) {
  CncSnapshot s; s.capturedMs = ms; s.uptimeMs = ms;
  s.activeInputs = s.rawInputs = active; return s;
}
template<size_t N> void registerCore(ultron::TelemetryCore<N>& core, uint32_t now) {
  assert(core.registered(DEVICE, BOOT, UNIX_TIME, now, 0));
}
struct MemoryClient {
  std::string bytes; size_t position = 0; bool holdOpen = false;
  int available() { return position < bytes.size(); }
  int read() { return available() ? static_cast<unsigned char>(bytes[position++]) : -1; }
  bool connected() { return available() || holdOpen; }
};
bool parseHttp(const std::string& bytes, ultron::HttpResponse& response, bool hold = false) {
  MemoryClient client{bytes, 0, hold}; uint32_t now = 0;
  return ultron::readHttpResponse(client, [&]() { return now; }, [&]() { ++now; }, 100, response);
}

void assertBoolean(JsonVariantConst value, bool expected) {
  assert(value.is<bool>());
  assert(value.as<bool>() == expected);
}

void assertWiring(JsonVariantConst payload, uint8_t bits) {
  // Contract from the IHM wiring, deliberately independent of DIGITAL_SIGNAL_NAMES:
  // Q0.0..Q0.5 -> I1..I6 = active, stopped, emergency, motor, door, alarm.
  const auto states = payload["digital_signals"];
  assert(states.size() == 6);
  assertBoolean(states["ativo"], bool(bits & 0x01));
  assertBoolean(states["inativo"], bool(bits & 0x02));
  assertBoolean(states["emergencia"], bool(bits & 0x04));
  assertBoolean(states["motor_ligado"], bool(bits & 0x08));
  assertBoolean(states["porta_aberta"], bool(bits & 0x10));
  assertBoolean(states["alarme"], bool(bits & 0x20));
  assertBoolean(payload["machine_active"], bool(bits & 0x01) && !(bits & 0x02));
  assert(payload["voltage_24v"].isNull());
  assert(payload["analog_signals"].size() == 0);
  const auto extra = payload["extra_signals"];
  assert(extra["profile"] == "six_signals_current_reserved_v3");
  assert(extra["spare_input"] == "I7");
  assert(extra["current_input"]["input"] == "I8");
  assert(extra["current_input"]["unit"] == "A");
  assert(extra["current_input"]["source"] == "unavailable");
  assertBoolean(extra["current_input"]["physical_enabled"], false);
  const auto raw = extra["entradas_brutas"];
  assert(raw.size() == 6);
  for (unsigned i = 0; i < 6; ++i) {
    char pin[3] = {'I', char('1' + i), '\0'};
    assertBoolean(raw[pin], bool(bits & (1U << i)));
  }
  assert(raw["I7"].isNull() && raw["I8"].isNull());
  if (bits == 0x10) {
    assertBoolean(states["porta_aberta"], true);
    assertBoolean(states["alarme"], false);
  }
  if (bits == 0x20) {
    assertBoolean(states["porta_aberta"], false);
    assertBoolean(states["alarme"], true);
  }
  if ((bits & 0x03) == 0x03) {
    assertBoolean(states["ativo"], true);
    assertBoolean(states["inativo"], true);
    assertBoolean(payload["machine_active"], false);
  }
}

int main(int argc, char** argv) {
  // Every port combination preserves six signals and never treats I8 as digital/current.
  ultron::TelemetryCore<2> monitorCore(1000, 15000);
  ultron::TelemetryCore<2> httpProfile(1000, 15000);
  registerCore(httpProfile, 0);
  for (unsigned bits = 0; bits < 256; ++bits) {
    CncSnapshot s;
    s.activeInputs = s.rawInputs = uint8_t(bits);
    s.capturedMs = bits; s.uptimeMs = bits;
    assert(monitorCore.enqueue(s));
    ultron::Reading reading;
    assert(monitorCore.takeUsb(bits, reading));
    char wire[ultron::PAYLOAD_BYTES];
    assert(ultron::serializeUsbReading(reading, "opta-monitor-usb-2.1.1", 0, wire, sizeof(wire)));
    JsonDocument json; assert(!deserializeJson(json, wire));
    auto payload = json["payload"];
    assert(json["machine_id"] == "1");
    assert(json["firmware_version"] == "opta-monitor-usb-2.1.1");
    assertWiring(payload, uint8_t(bits));
    assert(httpProfile.enqueue(s) && httpProfile.prepare(bits));
    assert(ultron::serializePending(httpProfile.pending(), httpProfile.bootId(), 0));
    JsonDocument httpJson;
    assert(!deserializeJson(httpJson, httpProfile.pending().body));
    assertWiring(httpJson.as<JsonVariantConst>(), uint8_t(bits));
    assert(httpJson["extra_signals"]["transport"] == "wifi_http");
    httpProfile.httpResult(201);
    if (bits == 255 && argc > 3) {
      std::ofstream output(argv[3]); assert(output.good());
      output << "CNC_JSON:" << wire << "\n";
    }
  }
  CncSnapshot unchanged;
  unchanged.activeInputs = unchanged.rawInputs = 255; unchanged.capturedMs = 500;
  assert(!monitorCore.enqueue(unchanged));
  unchanged.capturedMs = 1255;
  assert(monitorCore.enqueue(unchanged));
  puts("PASS IHM wiring: 256 combinations / I5 door / I6 alarm / activity conflicts / USB and HTTP contract");

  ultron::TelemetryCore<16> core(1000, 15000);
  assert(core.enqueue(sample(100)));
  assert(!core.enqueue(sample(200)));
  assert(core.enqueue(sample(220, 1)));
  auto alarm = sample(240, 0x20);
  assert(core.enqueue(alarm)); assert(core.queued() == 3);
  registerCore(core, 1000);
  assert(core.prepare(1000));
  assert(ultron::serializePending(core.pending(), core.bootId(), core.dropped()));
  const std::string original = core.pending().body;
  assert(original.find("\"timestamp\":") != std::string::npos);
  for (int status : {0, 408, 429, 500, 503}) { core.httpResult(status); assert(core.hasPending()); }
  core.disconnected(); assert(core.needsRegistration());
  assert(core.registered(DEVICE, OTHER, UNIX_TIME + 5, 6000, 30));
  assert(std::string(core.bootId()) == BOOT);
  assert(core.prepare(6000)); assert(ultron::serializePending(core.pending(), core.bootId(), 99));
  assert(original == core.pending().body);
  core.httpResult(404); assert(core.needsRegistration() && core.hasPending());
  assert(core.registered(OTHER, OTHER, UNIX_TIME + 6, 7000, 0));
  assert(core.prepare(7000) && original == core.pending().body);
  core.httpResult(201); assert(!core.hasPending() && core.confirmed() == 1);
  puts("PASS telemetry: retries/reconnect/404 preserve exact event/body/time/boot");

  ultron::TelemetryCore<2> bounded(1000, 15000);
  registerCore(bounded, 1000);
  bounded.enqueue(sample(1000)); bounded.enqueue(sample(2000)); bounded.enqueue(sample(3000));
  assert(bounded.queued() == 2 && bounded.dropped() == 1);
  assert(bounded.prepare(3000)); bounded.httpResult(401);
  assert(bounded.dropped() == 2 && !bounded.hasPending());
  assert(bounded.prepare(3000)); bounded.expire(18000);
  assert(!bounded.hasPending() && bounded.dropped() == 3);
  puts("PASS telemetry: bounded queue / overflow / expired and permanent errors counted");

  ultron::CaptureClock clock;
  assert(clock.sync(UNIX_TIME, UINT32_MAX - 100, 0));
  char start[25], after[25];
  assert(clock.format(UINT32_MAX - 100, UINT32_MAX - 100, start));
  assert(clock.format(899, 899, after));
  assert(std::string(start) != after);
  assert(std::string(after).substr(0, 19) == "2026-10-21T12:00:01");
  puts("PASS telemetry: capture UTC / millis rollover");

  ultron::Registration registration;
  const std::string body = std::string("{\n \"cnc\":{\"id\":\"") + OTHER + "\"}, \"server_time_unix\":1792584000, \"telemetry_session_id\":\"" + BOOT + "\",\"device\":{\"id\":\"" + DEVICE + "\"}}";
  assert(ultron::parseRegistration(body.c_str(), registration));
  assert(std::string(registration.deviceId) == DEVICE);
  assert(!ultron::parseRegistration("{\"device\":{\"id\":\"bad\"}}", registration));
  assert(!ultron::parseRegistration(body.substr(0, body.size() - 1).c_str(), registration));
  puts("PASS telemetry: structural registration parsing / reordered JSON / invalid response");

  ultron::HttpResponse response;
  assert(parseHttp("HTTP/1.1 201 Created\r\nContent-Length: 2\r\n\r\n{}", response));
  assert(response.status == 201 && std::string(response.body) == "{}");
  assert(parseHttp("HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n1\r\n{\r\n1\r\n}\r\n0\r\n\r\n", response));
  assert(std::string(response.body) == "{}");
  assert(parseHttp("HTTP/1.0 404 Gone\r\n\r\n{}", response));
  assert(response.status == 404);
  assert(!parseHttp("HTTP/1.1 201 Created\r\nContent-Length: 10\r\n\r\n{}", response));
  assert(!parseHttp("HTTP/1.1 200 OK\r\nContent-Length: 5000\r\n\r\n", response));
  assert(!parseHttp("HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\n", response, true));
  assert(!parseHttp("garbage\r\n\r\n{}", response));
  puts("PASS HTTP transport: lengths/chunks/close/errors/truncation/deadline/bounds");

  // USB consumes snapshots without network registration or a UTC anchor.
  ultron::TelemetryCore<2> usb(1000, 15000);
  ultron::Reading usbReading;
  assert(!usb.takeUsb(0, usbReading));
  assert(usb.enqueue(sample(0)));
  assert(!usb.enqueue(sample(20)));
  auto active = sample(30, 0x09);
  assert(usb.enqueue(active));
  assert(usb.takeUsb(30, usbReading) && usbReading.sequence == 1);
  assert(usb.takeUsb(30, usbReading) && usbReading.sequence == 2);
  char usbBody[ultron::PAYLOAD_BYTES];
  assert(ultron::serializeUsbReading(usbReading, "opta-monitor-usb-2.1.1", 3, usbBody, sizeof(usbBody)));
  JsonDocument usbJson; assert(!deserializeJson(usbJson, usbBody));
  assert(usbJson["protocol"] == 1 && usbJson["sequence"] == 2);
  assert(usbJson["payload"]["machine_active"] == true);
  assert(usbJson["payload"]["voltage_24v"].isNull());
  assert(usbJson["payload"]["analog_signals"].size() == 0);
  assert(usbJson["payload"]["digital_signals"]["motor_ligado"] == true);
  assert(usbJson["payload"]["extra_signals"]["amostras_descartadas"] == 3);
  assert(usbJson["payload"]["timestamp"].isNull());
  char tooSmall[8];
  assert(!ultron::serializeUsbReading(usbReading, "test", 0, tooSmall, sizeof(tooSmall)));
  if (argc > 2) {
    std::ofstream usbOutput(argv[2]); assert(usbOutput.good());
    usbOutput << "CNC_JSON:" << usbBody << "\n";
  }
  assert(usb.enqueue(sample(1000)));
  assert(!usb.takeUsb(16000, usbReading) && usb.dropped() == 1);
  puts("PASS USB: heartbeat / transitions / expiry / shared signals / bounded serialization");

  // Emit bytes produced by the actual firmware serializer for API/frontend tests.
  if (argc > 1) {
    std::ofstream output(argv[1]); assert(output.good()); output << "[";
    ultron::TelemetryCore<16> fixture(1000, 15000); registerCore(fixture, 0);
    // Preserve the fixture's functional order: stopped, active, stopped, emergency, alarm, door.
    const uint8_t signals[] = {0x02, 0x09, 0x02, 0x04, 0x20, 0x10};
    for (unsigned i = 0; i < 6; ++i) {
      auto s = sample(i * 1000, signals[i]);
      assert(fixture.enqueue(s) && fixture.prepare(s.capturedMs));
      assert(ultron::serializePending(fixture.pending(), fixture.bootId(), fixture.dropped()));
      if (i) output << ",";
      output << fixture.pending().body; fixture.httpResult(201);
    }
    output << "]\n";
    puts("PASS fixture: actual firmware JSON exported");
  }

  // Real USB frames for bridge -> API checks, independent of production signal order.
  if (argc > 4) {
    std::ofstream output(argv[4]); assert(output.good());
    ultron::TelemetryCore<2> ihmFixture(1000, 15000);
    const uint8_t inputs[] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x14, 0x24};
    for (unsigned i = 0; i < 8; ++i) {
      const auto s = sample(i * 1000, inputs[i]);
      assert(ihmFixture.enqueue(s));
      ultron::Reading reading;
      assert(ihmFixture.takeUsb(s.capturedMs, reading));
      assert(reading.sequence == i + 1);
      char wire[ultron::PAYLOAD_BYTES];
      assert(ultron::serializeUsbReading(reading, "opta-monitor-usb-2.1.1", 0, wire, sizeof(wire)));
      JsonDocument json; assert(!deserializeJson(json, wire));
      assertWiring(json["payload"], inputs[i]);
      output << "CNC_JSON:" << wire << "\n";
    }
    puts("PASS IHM fixture: I1-I6 one-hot / emergency+door / emergency+alarm / actual USB JSON exported");
  }
}
