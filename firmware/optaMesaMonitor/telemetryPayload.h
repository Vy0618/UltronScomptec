#pragma once
#include "telemetryCore.h"
// The Opta GCC 7 runtime has no complete <system_error>/<ostream> support.
// We serialize to fixed buffers and do not need iostream integration.
#define ARDUINOJSON_ENABLE_STD_STREAM 0
#include <ArduinoJson.h>

namespace ultron {
inline void writeSnapshot(JsonObject document, const MesaSnapshot& s) {
  document["machine_active"] = s.cycleActive;
  document["voltage_24v"] = nullptr;
  JsonObject digital = document["digital_signals"].to<JsonObject>();
  digital["ciclo"] = s.cycleActive;
  digital["alarme"] = s.fault;
  digital["altura_media_bloqueada"] = !(s.rawInputs & 2);
  digital["altura_pequena_bloqueada"] = !(s.rawInputs & 4);
  digital["altura_grande_bloqueada"] = !(s.rawInputs & 8);
  digital["metal_presente"] = bool(s.rawInputs & 16);
  digital["queda1_ocupada"] = bool(s.rawInputs & 32);
  digital["queda2_ocupada"] = bool(s.rawInputs & 64);
  digital["rampa1_cheia"] = s.ramp1Full;
  digital["rampa2_cheia"] = s.ramp2Full;
  document["analog_signals"].to<JsonObject>();
  JsonObject extra = document["extra_signals"].to<JsonObject>();
  extra["uptime_seconds"] = s.uptimeMs / 1000;
  JsonObject mesa = extra["mesa"].to<JsonObject>();
  mesa["estado"] = s.state;
  mesa["altura"] = s.height;
  mesa["metal_memorizado"] = s.metal;
  mesa["rampa1_cheia"] = s.ramp1Full;
  mesa["rampa2_cheia"] = s.ramp2Full;
  mesa["capturado_millis"] = s.capturedMs;
  JsonObject inputs = mesa["entradas_brutas"].to<JsonObject>();
  const char* inputNames[] = {"I1", "I2", "I3", "I4", "I5", "I6", "I7"};
  for (uint8_t i = 0; i < 7; ++i) inputs[inputNames[i]] = bool(s.rawInputs & (1U << i));
  JsonObject outputs = mesa["saidas_comandadas"].to<JsonObject>();
  outputs["O1"] = bool(s.commandedOutputs & 1);
  outputs["O2"] = bool(s.commandedOutputs & 2);
  outputs["O3"] = bool(s.commandedOutputs & 4);
  JsonObject counts = mesa["contadores"].to<JsonObject>();
  counts["total"] = s.total;
  counts["reto"] = s.straight;
  counts["queda1"] = s.drop1;
  counts["queda2"] = s.drop2;
  counts["falhas"] = s.faults;
}

inline bool serializeUsbReading(const Reading& reading, const char* firmware, uint64_t discarded,
                                char* output, size_t capacity) {
  JsonDocument document;
  document["protocol"] = 1;
  document["sequence"] = reading.sequence;
  document["uptime_ms"] = reading.snapshot.uptimeMs;
  document["firmware_version"] = firmware;
  JsonObject payload = document["payload"].to<JsonObject>();
  writeSnapshot(payload, reading.snapshot);
  payload["extra_signals"]["transport"] = "usb_serial";
  payload["extra_signals"]["amostras_descartadas"] = discarded;
  const size_t length = measureJson(document);
  if (document.overflowed() || length >= capacity) return false;
  return serializeJson(document, output, capacity) == length;
}

inline bool serializePending(PendingReading& pending, const char* bootId, uint64_t discarded) {
  // Only called once per reading. Retries send pending.body byte for byte.
  if (pending.body[0]) return true;
  JsonDocument document;
  writeSnapshot(document.to<JsonObject>(), pending.reading.snapshot);
  document["event_id"] = pending.eventId;
  document["timestamp"] = pending.timestamp;
  document["extra_signals"]["transport"] = "wifi_http";
  document["extra_signals"]["boot_id"] = bootId;
  document["extra_signals"]["amostras_descartadas"] = discarded;
  document["extra_signals"]["timestamp_source"] = "server_registration_estimate";
  const size_t length = measureJson(document);
  if (document.overflowed() || length >= sizeof(pending.body)) return false;
  return serializeJson(document, pending.body, sizeof(pending.body)) == length;
}

struct Registration {
  char deviceId[37] = {};
  char session[37] = {};
  uint64_t serverTime = 0;
};
inline bool parseRegistration(const char* body, Registration& result) {
  JsonDocument document;
  if (deserializeJson(document, body)) return false;
  // Read the nested device UUID, independent of whitespace/member order.
  const char* id = document["device"]["id"] | "";
  const char* session = document["telemetry_session_id"] | "";
  if (!isUuid(id) || !isUuid(session) || !document["server_time_unix"].is<uint64_t>()) return false;
  strcpy(result.deviceId, id);
  strcpy(result.session, session);
  result.serverTime = document["server_time_unix"].as<uint64_t>();
  return true;
}
}
