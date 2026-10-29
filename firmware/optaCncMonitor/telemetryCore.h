#pragma once
#include "telemetryModel.h"
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

namespace ultron {
constexpr size_t PAYLOAD_BYTES = 2048;

inline bool isUuid(const char* value) {
  if (!value || strlen(value) != 36) return false;
  for (size_t i = 0; i < 36; ++i) {
    if (i == 8 || i == 13 || i == 18 || i == 23) { if (value[i] != '-') return false; }
    else if (!((value[i] >= '0' && value[i] <= '9') || (value[i] >= 'a' && value[i] <= 'f') || (value[i] >= 'A' && value[i] <= 'F'))) return false;
  }
  return true;
}

// Monotonic accumulation also handles millis() rollover, provided observe runs
// at least once per 49 days. UTC is an estimate from the registration response.
class CaptureClock {
 public:
  void observe(uint32_t now) { monotonicMs_ += uint32_t(now - lastMs_); lastMs_ = now; }
  bool sync(uint64_t unixSeconds, uint32_t now, uint32_t roundTripMs) {
    observe(now);
    if (unixSeconds < 1577836800ULL || unixSeconds > 4102444800ULL) return false;
    anchorMonotonicMs_ = monotonicMs_;
    anchorUnixMs_ = unixSeconds * 1000 + roundTripMs / 2;
    ready_ = true;
    return true;
  }
  bool format(uint32_t capturedMs, uint32_t now, char (&output)[25]) {
    observe(now);
    if (!ready_) return false;
    const uint64_t current = anchorUnixMs_ + monotonicMs_ - anchorMonotonicMs_;
    const uint64_t capture = current - uint32_t(now - capturedMs);
    const time_t seconds = time_t(capture / 1000);
    const struct tm* utc = gmtime(&seconds);
    if (!utc) return false;
    return snprintf(output, sizeof(output), "%04d-%02d-%02dT%02d:%02d:%02d.%03uZ",
      utc->tm_year + 1900, utc->tm_mon + 1, utc->tm_mday, utc->tm_hour,
      utc->tm_min, utc->tm_sec, unsigned(capture % 1000)) == 24;
  }
  bool ready() const { return ready_; }
 private:
  uint32_t lastMs_ = 0;
  uint64_t monotonicMs_ = 0;
  uint64_t anchorMonotonicMs_ = 0;
  uint64_t anchorUnixMs_ = 0;
  bool ready_ = false;
};

struct Reading { CncSnapshot snapshot; uint64_t sequence = 0; };
struct PendingReading {
  Reading reading;
  char eventId[60] = {};
  char timestamp[25] = {};
  char body[PAYLOAD_BYTES] = {};
};

// The caller protects this object with a short mutex. No I/O occurs here.
template<size_t Capacity> class TelemetryCore {
 public:
  TelemetryCore(uint32_t intervalMs, uint32_t maximumAgeMs)
    : intervalMs_(intervalMs), maximumAgeMs_(maximumAgeMs) { static_assert(Capacity > 0, "queue required"); }

  bool enqueue(const CncSnapshot& sample) {
    const bool transition = !hasPrevious_ || previous_.activeInputs != sample.activeInputs;
    if (!transition && uint32_t(sample.capturedMs - lastCaptureMs_) < intervalMs_) return false;
    previous_ = sample;
    hasPrevious_ = true;
    lastCaptureMs_ = sample.capturedMs;
    if (size_ == Capacity) { head_ = (head_ + 1) % Capacity; --size_; ++dropped_; }
    queue_[(head_ + size_) % Capacity] = {sample, ++sequence_};
    ++size_;
    return true;
  }

  void expire(uint32_t now) {
    clock_.observe(now);
    if (hasPending_ && uint32_t(now - pending_.reading.snapshot.capturedMs) >= maximumAgeMs_) {
      hasPending_ = false; ++dropped_;
    }
    while (size_ && uint32_t(now - queue_[head_].snapshot.capturedMs) >= maximumAgeMs_) {
      head_ = (head_ + 1) % Capacity; --size_; ++dropped_;
    }
  }

  // USB needs neither Wi-Fi registration nor a device-side UTC clock.
  bool takeUsb(uint32_t now, Reading& reading) {
    expire(now);
    if (!size_) return false;
    reading = queue_[head_];
    head_ = (head_ + 1) % Capacity; --size_;
    return true;
  }

  bool registered(const char* id, const char* session, uint64_t serverTime, uint32_t now, uint32_t roundTrip) {
    if (!isUuid(id) || !isUuid(session) || !clock_.sync(serverTime, now, roundTrip)) return false;
    strcpy(deviceId_, id);
    if (!bootId_[0]) strcpy(bootId_, session);
    return true;
  }
  // A reconnect may refresh IP/registration. It must never rename a boot/event.
  void disconnected() { deviceId_[0] = '\0'; }
  bool needsRegistration() const { return !deviceId_[0]; }
  const char* deviceId() const { return deviceId_; }
  const char* bootId() const { return bootId_; }

  bool prepare(uint32_t now) {
    expire(now);
    if (hasPending_) return true;
    if (!size_ || needsRegistration() || !clock_.ready()) return false;
    pending_ = PendingReading();
    pending_.reading = queue_[head_];
    head_ = (head_ + 1) % Capacity; --size_;
    if (!clock_.format(pending_.reading.snapshot.capturedMs, now, pending_.timestamp)) { ++dropped_; return false; }
    snprintf(pending_.eventId, sizeof(pending_.eventId), "%s:%llu", bootId_,
      static_cast<unsigned long long>(pending_.reading.sequence));
    hasPending_ = true;
    return true;
  }

  // 404 retains the exact pending body while the adapter re-registers the MAC.
  // Bad contract/auth events are discarded explicitly; 408/429/5xx retry.
  void httpResult(int status) {
    if (!hasPending_) return;
    if (status >= 200 && status < 300) { hasPending_ = false; ++confirmed_; }
    else if (status == 404) disconnected();
    else if (status >= 400 && status < 500 && status != 408 && status != 429) { hasPending_ = false; ++dropped_; }
  }
  void rejectPending() { if (hasPending_) { hasPending_ = false; ++dropped_; } }
  PendingReading& pending() { return pending_; }
  const PendingReading& pending() const { return pending_; }
  bool hasPending() const { return hasPending_; }
  uint64_t dropped() const { return dropped_; }
  uint64_t confirmed() const { return confirmed_; }
  size_t queued() const { return size_; }
 private:
  Reading queue_[Capacity];
  size_t head_ = 0, size_ = 0;
  uint64_t sequence_ = 0, dropped_ = 0, confirmed_ = 0;
  uint32_t intervalMs_, maximumAgeMs_, lastCaptureMs_ = 0;
  CncSnapshot previous_;
  bool hasPrevious_ = false, hasPending_ = false;
  char deviceId_[37] = {}, bootId_[37] = {};
  CaptureClock clock_;
  PendingReading pending_;
};
}
