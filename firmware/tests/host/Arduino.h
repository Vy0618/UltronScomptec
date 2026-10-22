#pragma once
#include <stdint.h>
#include <stddef.h>
#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define A0 0
#define A1 1
#define A2 2
#define A3 3
#define A4 4
#define A5 5
#define A6 6
#define D0 10
#define D1 11
#define D2 12
#define LED_D0 20
#define LED_D1 21
#define LED_D2 22
extern uint32_t hostMillis;
extern int hostPins[32];
inline unsigned long millis() { return hostMillis; }
inline int digitalRead(uint8_t pin) { return hostPins[pin]; }
inline void digitalWrite(uint8_t pin, int state) { hostPins[pin] = state; }
inline void pinMode(uint8_t, int) {}
inline void delay(uint32_t ms) { hostMillis += ms; }
struct HostSerial {
  void begin(int) {}
  template<class T> void print(const T&) {}
  template<class T> void println(const T&) {}
  void println() {}
};
extern HostSerial Serial;
