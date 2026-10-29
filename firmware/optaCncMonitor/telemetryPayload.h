#pragma once
#include "telemetryCore.h"
// The Opta GCC 7 runtime has no complete <system_error>/<ostream> support.
// We serialize to fixed buffers and do not need iostream integration.
#define ARDUINOJSON_ENABLE_STD_STREAM 0
#include <ArduinoJson.h>

namespace ultron {
inline void writeSnapshot(JsonObject document, const CncSnapshot& s) {
  document["machine_active"] = bool(s.activeInputs & 1U);
  document["voltage_24v"] = nullptr;
  JsonObject digital = document["digital_signals"].to<JsonObject>();
  const char* names[] = {"em_execucao", "pausa", "parada", "emergencia",
                         "motor_ligado", "automatico", "manual", "alarme"};
  for (uint8_t i = 0; i < 8; ++i) digital[names[i]] = bool(s.activeInputs & (1U << i));
  document["analog_signals"].to<JsonObject>();
  JsonObject extra = document["extra_signals"].to<JsonObject>();
  extra["profile"] = "boolean_monitor_v1";
  extra["uptime_seconds"] = s.uptimeMs / 1000;
  extra["capturado_millis"] = s.capturedMs;
  JsonObject raw = extra["entradas_brutas"].to<JsonObject>();
  const char* inputs[] = {"I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"};
  for (uint8_t i = 0; i < 8; ++i) raw[inputs[i]] = bool(s.rawInputs & (1U << i));
  JsonObject clp = extra["clp_inputs"].to<JsonObject>();
  const char* addresses[] = {"D000", "D001", "D002", "D003", "D004", "D005", "D006", "D007"};
  for (uint8_t i = 0; i < 8; ++i) clp[addresses[i]] = bool(s.activeInputs & (1U << i));
}

inline bool serializeUsbReading(const Reading& reading, const char* firmware, uint64_t discarded,
                                char* output, size_t capacity, const char* machineId = "1") {
  JsonDocument document;
  document["protocol"] = 1;
  document["machine_id"] = machineId;
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
