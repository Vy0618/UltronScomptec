#pragma once
#include <Arduino.h>
#if __has_include("optaSecrets.h")
#include "optaSecrets.h"
#endif
#ifndef ULTRON_WIFI_SSID
#define ULTRON_WIFI_SSID "maker"
#endif
#ifndef ULTRON_WIFI_PASSWORD
#define ULTRON_WIFI_PASSWORD "12345678"
#endif
#ifndef ULTRON_BACKEND_HOST
#define ULTRON_BACKEND_HOST "IP_DO_NOTEBOOK_NO_HOTSPOT"
#endif
#ifndef ULTRON_DEVICE_API_KEY
#define ULTRON_DEVICE_API_KEY ""
#endif

// Select one transport at build time: 0 = Wi-Fi HTTP, 1 = USB serial bridge.
// The terminal selector takes precedence over the local optaSecrets.h setting.
#ifdef ULTRON_TELEMETRY_USB_OVERRIDE
#undef ULTRON_TELEMETRY_USB
#define ULTRON_TELEMETRY_USB ULTRON_TELEMETRY_USB_OVERRIDE
#endif
#ifndef ULTRON_TELEMETRY_USB
#define ULTRON_TELEMETRY_USB 0
#endif
#if ULTRON_TELEMETRY_USB != 0 && ULTRON_TELEMETRY_USB != 1
#error "ULTRON_TELEMETRY_USB must be 0 or 1"
#endif

// Configuração da conexão direta Opta WiFi -> API SCOMPTEC.
// BACKEND_HOST deve ser o IPv4 do notebook na rede Wi-Fi maker.
// Com um servidor hospedado, use o nome DNS e implemente HTTPS antes de produção.
constexpr char WIFI_SSID[] = ULTRON_WIFI_SSID;
constexpr char WIFI_PASSWORD[] = ULTRON_WIFI_PASSWORD;
constexpr char BACKEND_HOST[] = ULTRON_BACKEND_HOST;
constexpr uint16_t BACKEND_PORT = 8000;
constexpr char API_PREFIX[] = "/api";

// Deve ser igual a DEVICE_API_KEY no .env do backend. Vazio funciona quando o
// backend também está com DEVICE_API_KEY vazia (configuração atual do protótipo).
constexpr char DEVICE_API_KEY[] = ULTRON_DEVICE_API_KEY;

#if ULTRON_TELEMETRY_USB
constexpr char FIRMWARE_VERSION[] = "mesa-opta-usb-1.4.0";
#else
constexpr char FIRMWARE_VERSION[] = "mesa-opta-wifi-1.4.0";
#endif
constexpr uint32_t SEND_INTERVAL_MS = 1000;
constexpr uint32_t WIFI_RETRY_INTERVAL_MS = 5000;
constexpr uint32_t HTTP_TIMEOUT_MS = 4000;
constexpr uint32_t MAX_PENDING_MS = 15000;
constexpr uint32_t HTTP_RETRY_INTERVAL_MS = 1000;
constexpr size_t TELEMETRY_QUEUE_CAPACITY = 16;
