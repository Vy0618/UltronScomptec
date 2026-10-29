#include "telemetry.h"
#include "config.h"
#include "telemetryCore.h"
#include "telemetryPayload.h"
#if !ULTRON_TELEMETRY_USB
#include "httpResponse.h"
#include <WiFi.h>
#endif
#include <rtos/Mutex.h>
#include <rtos/Thread.h>

namespace {
constexpr uint32_t NETWORK_THREAD_STACK = 16384;
rtos::Mutex snapshotMutex;
rtos::Thread networkThread(osPriorityNormal, NETWORK_THREAD_STACK, nullptr, "opta-telemetry");
ultron::TelemetryCore<TELEMETRY_QUEUE_CAPACITY> telemetry(SEND_INTERVAL_MS, MAX_PENDING_MS);

#if ULTRON_TELEMETRY_USB
void networkTask() {
  char body[ultron::PAYLOAD_BYTES];
  for (;;) {
    // The Mbed USB driver may block a write. Never hold the snapshot mutex
    // during USB I/O; only this task writes to Serial in USB mode.
    const bool connected = bool(Serial);
    ultron::Reading reading;
    snapshotMutex.lock();
    const uint32_t now = millis();
    telemetry.expire(now);
    const bool ready = connected && telemetry.takeUsb(now, reading);
    const uint64_t dropped = telemetry.dropped();
    snapshotMutex.unlock();
    if (ready && ultron::serializeUsbReading(reading, FIRMWARE_VERSION, dropped, body, sizeof(body), MACHINE_ID)) {
      Serial.print("CNC_JSON:");
      Serial.println(body);
    }
    delay(20);
  }
}
#else
void diagnose(const char* action, int status) {
  Serial.print("[TELEMETRIA] "); Serial.print(action); Serial.print(" HTTP="); Serial.println(status);
}

bool httpPost(const String& path, const char* body, ultron::HttpResponse& response) {
  response = ultron::HttpResponse();
  WiFiClient client;
  client.setTimeout(HTTP_TIMEOUT_MS);
  client.setSocketTimeout(HTTP_TIMEOUT_MS);
  if (!client.connect(BACKEND_HOST, BACKEND_PORT)) return false;
  client.print("POST "); client.print(path); client.println(" HTTP/1.1");
  client.print("Host: "); client.print(BACKEND_HOST); client.print(":"); client.println(BACKEND_PORT);
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  if (DEVICE_API_KEY[0]) { client.print("X-Device-Key: "); client.println(DEVICE_API_KEY); }
  client.print("Content-Length: "); client.println(strlen(body)); client.println(); client.print(body);
  const bool complete = ultron::readHttpResponse(client, []() { return uint32_t(millis()); },
    []() { delay(5); }, HTTP_TIMEOUT_MS, response);
  client.stop();
  return complete;
}

bool registerDevice() {
  JsonDocument document;
  document["mac_address"] = WiFi.macAddress();
  document["ip_address"] = WiFi.localIP().toString();
  document["firmware_version"] = FIRMWARE_VERSION;
  char body[256];
  if (measureJson(document) >= sizeof(body)) return false;
  serializeJson(document, body, sizeof(body));
  ultron::HttpResponse response;
  const uint32_t started = millis();
  if (!httpPost(String(API_PREFIX) + "/devices/register", body, response) || response.status < 200 || response.status >= 300) {
    diagnose("cadastro falhou; confira rede, host e chave", response.status); return false;
  }
  ultron::Registration registration;
  if (!ultron::parseRegistration(response.body, registration) ||
      !telemetry.registered(registration.deviceId, registration.session, registration.serverTime,
        millis(), uint32_t(millis() - started))) {
    diagnose("resposta de cadastro invalida/incompleta", response.status); return false;
  }
  Serial.print("[TELEMETRIA] dispositivo="); Serial.print(telemetry.deviceId());
  Serial.print(" boot="); Serial.println(telemetry.bootId());
  return true;
}

void networkTask() {
  // Arduino Mbed Opta uses begin() directly; there is no WiFi.mode(WIFI_STA).
  WiFi.setTimeout(HTTP_TIMEOUT_MS);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  uint32_t lastWifiAttempt = millis();
  uint32_t lastRegistrationAttempt = millis() - WIFI_RETRY_INTERVAL_MS;
  uint32_t lastSendAttempt = millis() - HTTP_RETRY_INTERVAL_MS;
  uint64_t reportedDiscarded = 0;
  bool wasConnected = false;
  const bool hostConfigured = BACKEND_HOST[0] && strcmp(BACKEND_HOST, "IP_DO_NOTEBOOK_NO_HOTSPOT") != 0;
  if (!hostConfigured) Serial.println("[TELEMETRIA] Configure ULTRON_BACKEND_HOST em optaSecrets.h; aquisicao continua.");

  for (;;) {
    uint32_t now = millis();
    snapshotMutex.lock();
    now = millis();
    telemetry.expire(now);
    const uint64_t discarded = telemetry.dropped();
    snapshotMutex.unlock();
    if (discarded != reportedDiscarded) {
      reportedDiscarded = discarded;
      Serial.print("[TELEMETRIA] amostras descartadas (fila/idade/erro permanente)=");
      Serial.println(static_cast<unsigned long>(discarded));
    }

    if (WiFi.status() != WL_CONNECTED) {
      telemetry.disconnected();
      if (wasConnected) Serial.println("[TELEMETRIA] Wi-Fi perdido; eventos/boot pendentes preservados por ate 15 s.");
      wasConnected = false;
      if (uint32_t(now - lastWifiAttempt) >= WIFI_RETRY_INTERVAL_MS) {
        lastWifiAttempt = now;
        Serial.println("[TELEMETRIA] reconectando Wi-Fi...");
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      }
      delay(100); continue;
    }
    if (!wasConnected) { Serial.print("[TELEMETRIA] Wi-Fi conectado IP="); Serial.println(WiFi.localIP()); wasConnected = true; }
    if (!hostConfigured) { delay(250); continue; }

    if (telemetry.needsRegistration()) {
      if (uint32_t(now - lastRegistrationAttempt) >= WIFI_RETRY_INTERVAL_MS) {
        lastRegistrationAttempt = now;
        registerDevice();
      }
      delay(100); continue;
    }

    snapshotMutex.lock();
    now = millis();
    const bool pending = telemetry.prepare(now);
    const uint64_t dropped = telemetry.dropped();
    snapshotMutex.unlock();
    if (pending && uint32_t(now - lastSendAttempt) >= HTTP_RETRY_INTERVAL_MS) {
      lastSendAttempt = now;
      if (!ultron::serializePending(telemetry.pending(), telemetry.bootId(), dropped)) {
        snapshotMutex.lock(); telemetry.rejectPending(); snapshotMutex.unlock();
        diagnose("payload excedeu limite/memoria; leitura descartada", 0); continue;
      }
      ultron::HttpResponse response;
      const bool complete = httpPost(String(API_PREFIX) + "/devices/" + telemetry.deviceId() + "/telemetry",
        telemetry.pending().body, response);
      snapshotMutex.lock(); telemetry.httpResult(complete ? response.status : 0); snapshotMutex.unlock();
      if (complete && response.status >= 200 && response.status < 300) lastSendAttempt = millis() - HTTP_RETRY_INTERVAL_MS;
      if (!complete || response.status < 200 || response.status >= 300) {
        diagnose(!complete ? "resposta ausente/incompleta; retry do mesmo evento" : response.status == 404 ? "UUID removido; refazendo cadastro pelo MAC" : "envio falhou; retry limitado pela idade", response.status);
        if (complete && response.status == 404) lastRegistrationAttempt = millis() - WIFI_RETRY_INTERVAL_MS;
      }
    }
    delay(20);
  }
}
#endif
}

void telemetryBegin() {
  if (networkThread.start(networkTask) != osOK) Serial.println("[TELEMETRIA] ERRO ao iniciar telemetria; aquisicao continua.");
}

void telemetryPublish(const CncSnapshot& snapshot) {
  // Only bounded copies under the mutex; acquisition never performs I/O.
  snapshotMutex.lock(); telemetry.enqueue(snapshot); snapshotMutex.unlock();
}
