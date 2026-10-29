#pragma once
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

namespace ultron {
struct HttpResponse { int status = 0; char body[4097] = {}; };

// Bounded HTTP framing shared by the real WiFiClient and host transport tests.
template<class Client, class Clock, class Idle>
bool readHttpResponse(Client& client, Clock now, Idle idle, uint32_t timeoutMs, HttpResponse& response) {
  response = HttpResponse();
  const uint32_t started = now();
  auto get = [&]() -> int {
    for (;;) {
      if (uint32_t(now() - started) >= timeoutMs) return -1;
      if (client.available()) return client.read();
      if (!client.connected()) return -1;
      idle();
    }
  };
  auto line = [&](char* output, size_t capacity) -> bool {
    size_t length = 0;
    for (;;) {
      const int byte = get();
      if (byte < 0) return false;
      if (byte == '\n') { output[length] = '\0'; return true; }
      if (byte != '\r') { if (length + 1 >= capacity) return false; output[length++] = char(byte); }
    }
  };
  char header[512];
  if (!line(header, sizeof(header)) || sscanf(header, "HTTP/%*d.%*d %d", &response.status) != 1) return false;
  long contentLength = -1;
  bool chunked = false;
  size_t headerBytes = strlen(header);
  for (;;) {
    if (!line(header, sizeof(header))) return false;
    headerBytes += strlen(header) + 2;
    if (headerBytes > 4096) return false;
    if (!header[0]) break;
    for (char* c = header; *c; ++c) *c = char(tolower(static_cast<unsigned char>(*c)));
    if (strncmp(header, "content-length:", 15) == 0) {
      char* end = nullptr;
      contentLength = strtol(header + 15, &end, 10);
      while (end && *end == ' ') ++end;
      if (end == header + 15 || (end && *end) || contentLength < 0 || contentLength > 4096) return false;
    }
    if (strncmp(header, "transfer-encoding:", 18) == 0 && strstr(header + 18, "chunked")) chunked = true;
  }
  size_t used = 0;
  auto append = [&](size_t count) -> bool {
    if (count > sizeof(response.body) - 1 - used) return false;
    for (size_t i = 0; i < count; ++i) { const int c = get(); if (c < 0) return false; response.body[used++] = char(c); }
    response.body[used] = '\0'; return true;
  };
  if (chunked) {
    for (;;) {
      if (!line(header, sizeof(header))) return false;
      char* end = nullptr;
      const unsigned long count = strtoul(header, &end, 16);
      if (end == header || (*end && *end != ';') || count > 4096) return false;
      if (!count) {
        size_t trailers = 0;
        do { if (!line(header, sizeof(header))) return false; trailers += strlen(header) + 2; if (trailers > 4096) return false; } while (header[0]);
        return true;
      }
      if (!append(count) || get() != '\r' || get() != '\n') return false;
    }
  }
  if (contentLength >= 0) return append(size_t(contentLength));
  while (uint32_t(now() - started) < timeoutMs) {
    if (client.available()) { if (!append(1)) return false; }
    else if (!client.connected()) return true;
    else idle();
  }
  return false;
}
}
